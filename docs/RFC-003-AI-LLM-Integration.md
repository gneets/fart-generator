# RFC-003: AI/LLM Integration

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal
**Related:** [RFC-001](./RFC-001-System-Architecture.md), [RFC-002](./RFC-002-Audio-Generation-Engine.md)

---

## 1. Overview

This RFC defines how we integrate Anthropic's Claude API to interpret natural language prompts and extract audio generation parameters. Claude will serve as the "brain" that translates user intent into structured parameters for the audio engine.

## 2. Goals

- **High Accuracy**: 90%+ correct interpretation of common prompts
- **Low Latency**: < 1 second for prompt interpretation
- **Cost Efficiency**: Minimize API costs through caching and optimization
- **User-Friendly**: Handle ambiguous, creative, and conversational prompts
- **Fallback Handling**: Gracefully handle API failures or rate limits

## 3. Why Claude API?

**Advantages:**
- Superior natural language understanding
- Structured output support (JSON mode)
- Conversational context (multi-turn interactions)
- Lower hallucination rate vs competitors
- Good balance of cost and performance

**Anthropic Pricing (as of 2026):**
- Claude 3.5 Sonnet: ~$3/MTok input, ~$15/MTok output
- Estimated cost per generation: $0.001-0.005 (assuming 300-500 tokens total)
- For 10K generations: $10-50/month

## 4. Prompt Engineering Strategy

### 4.1 System Prompt Template

```python
SYSTEM_PROMPT = """You are an expert audio parameter extractor for a fart sound generator.

Your job is to interpret user descriptions of fart sounds and extract precise audio generation parameters.

**Output Format (JSON):**
{
  "duration": <float between 0.5 and 10.0>,
  "wetness": <int between 0 and 10>,
  "pitch": <int between 0 and 10>,
  "type": <"squeaker" | "rumbler" | "stutterer" | "classic" | "wet">,
  "confidence": <float between 0.0 and 1.0>
}

**Parameter Definitions:**
- duration: Length of sound in seconds (0.5=very short, 10=very long)
- wetness: Liquid/bubbling quality (0=completely dry, 10=very wet/sloppy)
- pitch: Fundamental frequency (0=very low/bass, 5=medium, 10=very high/squeaky)
- type: Overall character
  * "squeaker": High-pitched, short, sharp
  * "rumbler": Low-pitched, long, rolling
  * "stutterer": Multiple bursts in quick succession
  * "classic": Balanced, medium duration and pitch
  * "wet": Emphasizes liquid/bubbling characteristics
- confidence: Your confidence in the interpretation (0.0=very uncertain, 1.0=very certain)

**Guidelines:**
1. Be creative but realistic with interpretations
2. Use sensible defaults when prompt is vague
3. Favor variety - add randomization suggestions when appropriate
4. If completely nonsensical, return classic preset with low confidence
5. Consider context from previous generations (if provided)

**Examples:**

User: "a long, rumbling fart"
Response: {"duration": 4.5, "wetness": 3, "pitch": 2, "type": "rumbler", "confidence": 0.95}

User: "quick toot"
Response: {"duration": 0.8, "wetness": 1, "pitch": 7, "type": "squeaker", "confidence": 0.9}

User: "wet and sloppy"
Response: {"duration": 3.0, "wetness": 9, "pitch": 4, "type": "wet", "confidence": 0.92}

User: "like a machine gun"
Response: {"duration": 2.5, "wetness": 2, "pitch": 6, "type": "stutterer", "confidence": 0.88}

User: "the loudest fart ever"
Response: {"duration": 5.0, "wetness": 4, "pitch": 3, "type": "rumbler", "confidence": 0.85}

User: "rainbow unicorn"
Response: {"duration": 2.0, "wetness": 5, "pitch": 5, "type": "classic", "confidence": 0.2}
"""
```

### 4.2 User Message Format

```python
def create_user_message(prompt: str, context: Optional[dict] = None) -> str:
    """Create user message with optional context"""

    message = f"User prompt: \"{prompt}\""

    if context and context.get("previous_generation"):
        prev = context["previous_generation"]
        message += f"\n\nPrevious generation:\n"
        message += f"- Prompt: \"{prev['prompt']}\"\n"
        message += f"- Parameters: duration={prev['duration']}, wetness={prev['wetness']}, pitch={prev['pitch']}, type={prev['type']}"

    return message
```

## 5. API Integration Implementation

### 5.1 Claude Service Class

```python
import anthropic
import json
from typing import Dict, Optional
from pydantic import BaseModel
import redis
import hashlib


class PromptInterpretation(BaseModel):
    """Structured output from Claude"""
    duration: float
    wetness: int
    pitch: int
    type: str
    confidence: float


class ClaudeService:
    """Service for Claude API integration"""

    def __init__(
        self,
        api_key: str,
        redis_client: redis.Redis,
        cache_ttl: int = 86400  # 24 hours
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.redis = redis_client
        self.cache_ttl = cache_ttl
        self.model = "claude-3-5-sonnet-20241022"  # Latest Sonnet

    async def interpret_prompt(
        self,
        prompt: str,
        context: Optional[dict] = None
    ) -> PromptInterpretation:
        """
        Interpret user prompt and extract audio parameters

        Args:
            prompt: User's natural language description
            context: Optional context from previous generations

        Returns:
            PromptInterpretation with extracted parameters

        Raises:
            ClaudeAPIError: If API call fails
        """

        # Check cache first
        cache_key = self._get_cache_key(prompt, context)
        cached = await self._get_from_cache(cache_key)
        if cached:
            return PromptInterpretation(**cached)

        # Prepare messages
        user_message = create_user_message(prompt, context)

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,  # Some creativity, but consistent
            )

            # Parse response
            content = response.content[0].text
            parameters = self._parse_response(content)

            # Validate parameters
            interpretation = PromptInterpretation(**parameters)

            # Cache result
            await self._save_to_cache(cache_key, interpretation.dict())

            return interpretation

        except anthropic.APIError as e:
            # Handle API errors
            raise ClaudeAPIError(f"Claude API error: {e}")
        except Exception as e:
            # Fallback to default on parse errors
            return self._get_fallback_interpretation(prompt)

    def _parse_response(self, content: str) -> dict:
        """Parse JSON from Claude's response"""
        try:
            # Try to extract JSON from markdown code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Failed to parse Claude response: {e}")

    def _get_cache_key(self, prompt: str, context: Optional[dict]) -> str:
        """Generate cache key from prompt and context"""
        cache_str = f"{prompt}:{json.dumps(context) if context else ''}"
        return f"claude:prompt:{hashlib.md5(cache_str.encode()).hexdigest()}"

    async def _get_from_cache(self, key: str) -> Optional[dict]:
        """Get cached interpretation"""
        try:
            cached = self.redis.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        return None

    async def _save_to_cache(self, key: str, data: dict):
        """Save interpretation to cache"""
        try:
            self.redis.setex(
                key,
                self.cache_ttl,
                json.dumps(data)
            )
        except Exception:
            pass  # Fail silently if caching fails

    def _get_fallback_interpretation(self, prompt: str) -> PromptInterpretation:
        """Return sensible defaults if AI fails"""
        return PromptInterpretation(
            duration=2.0,
            wetness=5,
            pitch=5,
            type="classic",
            confidence=0.3
        )


class ClaudeAPIError(Exception):
    """Custom exception for Claude API errors"""
    pass
```

### 5.2 Integration in WebSocket Handler

```python
from fastapi import WebSocket
from app.services.claude_service import ClaudeService
from app.services.audio_engine import AudioGenerationEngine

class GenerationWebSocketHandler:
    """WebSocket handler for real-time generation"""

    def __init__(
        self,
        claude_service: ClaudeService,
        audio_engine: AudioGenerationEngine
    ):
        self.claude = claude_service
        self.audio = audio_engine

    async def handle_generation(self, websocket: WebSocket, request: dict):
        """Handle generation request via WebSocket"""

        prompt = request.get("prompt")
        context = request.get("context")  # Previous generation info

        try:
            # Step 1: Send status update
            await websocket.send_json({
                "status": "interpreting",
                "message": "Interpreting your prompt..."
            })

            # Step 2: Call Claude API
            interpretation = await self.claude.interpret_prompt(prompt, context)

            # Step 3: Send interpretation to user
            await websocket.send_json({
                "status": "interpreted",
                "interpretation": interpretation.dict(),
                "message": f"Generating {interpretation.type} sound..."
            })

            # Step 4: Generate audio
            await websocket.send_json({
                "status": "generating",
                "progress": 0
            })

            audio_data, sample_rate = self.audio.generate(
                AudioParameters(**interpretation.dict())
            )

            # Step 5: Save to S3 and get URL
            audio_url = await self._save_and_upload(audio_data, sample_rate)

            # Step 6: Send completion
            await websocket.send_json({
                "status": "complete",
                "audio_url": audio_url,
                "parameters": interpretation.dict()
            })

        except ClaudeAPIError as e:
            await websocket.send_json({
                "status": "error",
                "message": "Failed to interpret prompt. Please try again."
            })
        except Exception as e:
            await websocket.send_json({
                "status": "error",
                "message": "Generation failed. Please try again."
            })
```

## 6. Optimization Strategies

### 6.1 Caching

**Cache Key Strategy:**
```
Key: "claude:prompt:<md5(prompt + context)>"
Value: JSON string of parameters
TTL: 24 hours
```

**Cache Hit Expectations:**
- Common prompts ("long fart", "quick toot"): 60-70% hit rate
- Unique creative prompts: < 10% hit rate
- Average hit rate: ~30-40%
- Cost savings: ~35% reduction in Claude API calls

### 6.2 Batching (Future)

For batch generations, send multiple prompts in single API call:
```python
async def interpret_prompts_batch(prompts: List[str]) -> List[PromptInterpretation]:
    """Batch interpret multiple prompts"""
    # Format as single request with multiple prompts
    # Parse multiple JSON objects from response
    # ~30% cost reduction vs individual calls
```

### 6.3 Model Selection

**Current: Claude 3.5 Sonnet**
- Best balance of cost and quality
- Fast response times (< 1s)
- High accuracy

**Alternatives:**
- **Claude 3 Haiku**: Cheaper ($0.80/MTok), faster, but less accurate
- **Claude 3 Opus**: More expensive ($60/MTok), highest quality
- **Future**: Fine-tuned lightweight model for production

## 7. Error Handling & Fallbacks

### 7.1 Error Types

**API Errors:**
- Rate limit exceeded → Retry with exponential backoff
- Invalid API key → Alert administrators
- Network timeout → Retry once, then fallback

**Parse Errors:**
- Invalid JSON → Use regex extraction
- Missing fields → Fill with sensible defaults
- Out-of-range values → Clamp to valid range

### 7.2 Fallback Strategy

```python
def get_fallback_parameters(prompt: str) -> AudioParameters:
    """Rule-based fallback when Claude fails"""

    # Simple keyword matching
    if any(word in prompt.lower() for word in ["long", "huge", "massive"]):
        duration = 5.0
    elif any(word in prompt.lower() for word in ["quick", "short", "brief"]):
        duration = 1.0
    else:
        duration = 2.5

    if any(word in prompt.lower() for word in ["wet", "sloppy", "liquid"]):
        wetness = 8
        type_ = "wet"
    elif any(word in prompt.lower() for word in ["squeaky", "high", "sharp"]):
        wetness = 2
        pitch = 8
        type_ = "squeaker"
    elif any(word in prompt.lower() for word in ["low", "deep", "rumble"]):
        wetness = 3
        pitch = 2
        type_ = "rumbler"
    else:
        wetness = 5
        pitch = 5
        type_ = "classic"

    return AudioParameters(
        duration=duration,
        wetness=wetness,
        pitch=pitch,
        type=type_
    )
```

## 8. Testing Strategy

### 8.1 Unit Tests

```python
def test_interpret_simple_prompt():
    """Test basic prompt interpretation"""
    service = ClaudeService(api_key="test")
    result = await service.interpret_prompt("long rumbling fart")

    assert result.duration > 3.0
    assert result.type in ["rumbler", "classic"]
    assert result.pitch < 5
    assert result.confidence > 0.7


def test_cache_hit():
    """Test caching works"""
    service = ClaudeService(api_key="test", redis_client=redis_mock)

    # First call - miss
    result1 = await service.interpret_prompt("test prompt")

    # Second call - hit (should be instant)
    result2 = await service.interpret_prompt("test prompt")

    assert result1.dict() == result2.dict()
    assert redis_mock.get.called
```

### 8.2 Integration Tests

Test end-to-end flow with real Claude API (dev environment):
- Send 100 diverse prompts
- Verify parameters are in valid ranges
- Measure latency distribution
- Check confidence scores

### 8.3 Evaluation Dataset

Create test dataset with expected outputs:
```json
[
  {
    "prompt": "a long, rumbling fart",
    "expected": {
      "duration_range": [3.0, 7.0],
      "wetness_range": [2, 6],
      "pitch_range": [0, 4],
      "type": ["rumbler", "classic"]
    }
  },
  ...
]
```

Run periodically to detect regressions.

## 9. Monitoring & Analytics

### 9.1 Metrics to Track

- **API Call Volume**: Requests per minute/hour/day
- **Cache Hit Rate**: % of requests served from cache
- **Latency**: p50, p95, p99 for Claude API calls
- **Cost**: Total spending on Claude API per day/month
- **Confidence Distribution**: Average confidence scores
- **Error Rate**: % of failed interpretations
- **Fallback Rate**: % using rule-based fallback

### 9.2 Alerts

- Cache hit rate drops below 20%
- Average latency exceeds 2 seconds
- Daily API cost exceeds budget ($10/day)
- Error rate exceeds 5%

## 10. Future Enhancements

### 10.1 Conversational Context (Phase 2)

Support multi-turn conversations:
```
User: "generate a long rumbler"
AI: [generates]
User: "make it wetter"
AI: [generates with increased wetness, same duration/pitch]
```

Store conversation history per session.

### 10.2 Fine-tuning (Phase 3)

Fine-tune a smaller model on prompt→parameters dataset:
- Collect 10K+ user generations
- Fine-tune Haiku or open-source model
- Deploy for production (lower cost, latency)

### 10.3 Prompt Suggestions

Use Claude to suggest creative prompts:
```
User: (clicks "surprise me")
AI: "How about: 'a majestic trumpet fanfare of flatulence'?"
```

## 11. Open Questions

1. **Model Version**: Stay on Sonnet or try Opus for higher quality?
2. **Temperature**: 0.7 for balance, or lower (0.3) for consistency?
3. **Max Tokens**: 500 sufficient, or increase for complex prompts?
4. **Retry Logic**: How many retries before fallback?
5. **Prompt Evolution**: A/B test different system prompts?

## 12. References

- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Claude 3.5 Sonnet Announcement](https://www.anthropic.com/news/claude-3-5-sonnet)

---

**Next Steps:**
1. Obtain Anthropic API key
2. Implement ClaudeService class
3. Test with diverse prompts
4. Optimize system prompt through iteration
5. Set up caching infrastructure
6. Monitor costs and performance
