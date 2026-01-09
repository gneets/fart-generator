# RFC-002: Audio Generation Engine

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal
**Related:** [RFC-001-System-Architecture.md](./RFC-001-System-Architecture.md)

---

## 1. Overview

This RFC defines the audio generation engine responsible for synthesizing realistic fart sounds based on parameters extracted from natural language prompts. The engine uses a hybrid approach combining pre-recorded samples with procedural synthesis to achieve high-quality, varied output.

## 2. Goals

- **Realism**: Generate sounds that are perceived as authentic (70%+ user satisfaction)
- **Variety**: Ensure no two consecutive generations are too similar (< 75% similarity)
- **Performance**: Generate audio in < 3 seconds (90th percentile)
- **Flexibility**: Support wide range of parameters (duration, wetness, pitch, type)
- **Real-time**: Stream generation progress via WebSocket

## 3. Audio Generation Approach

### 3.1 Hybrid Strategy

**Why Hybrid?**
- Pure synthesis lacks realism and authenticity
- Pure samples lack variety and flexibility
- Hybrid combines best of both worlds

**Components:**
1. **Base Sample Library**: 10-20 high-quality recorded samples
2. **Procedural Synthesis**: Generated components (noise, rumbling, bubbling)
3. **Signal Processing**: Filters, effects, pitch shifting, time stretching
4. **Mixer**: Combines multiple layers with randomization

### 3.2 Audio Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│              Audio Generation Pipeline                           │
└─────────────────────────────────────────────────────────────────┘

Input Parameters
├── duration: float (0.5-10.0 seconds)
├── wetness: int (0-10 scale)
├── pitch: int (0-10 scale)
├── type: str ("squeaker", "rumbler", "stutterer", "classic", "wet")
└── randomness_seed: int (for reproducibility)

        │
        ▼
┌────────────────────────────────────────┐
│  Step 1: Sample Selection              │
│  - Choose 1-3 base samples based on    │
│    type parameter                      │
│  - Load samples into memory            │
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 2: Synthesis Generation          │
│  - Generate noise layer (white/pink)   │
│  - Generate rumble layer (low freq)    │
│  - Generate bubbling layer (if wet)    │
│  - Each layer: numpy array @ 44.1kHz   │
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 3: Parameter Mapping             │
│  - Map wetness (0-10) → filter params  │
│  - Map pitch (0-10) → pitch shift      │
│  - Map duration → time stretch factor  │
│  - Add randomization (±10%)            │
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 4: Signal Processing             │
│  - Pitch shifting (librosa/soundfile)  │
│  - Time stretching (match duration)    │
│  - Apply filters (lowpass, bandpass)   │
│  - Add effects (distortion, saturation)│
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 5: Layer Mixing                  │
│  - Combine samples + synthesis layers  │
│  - Apply amplitude envelopes (ADSR)    │
│  - Mix with randomized weights         │
│  - Ensure smooth transitions           │
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 6: Post-Processing               │
│  - Normalize amplitude (prevent clip)  │
│  - Apply limiter/compressor            │
│  - Add subtle reverb (optional)        │
│  - Fade in/out (50ms)                  │
└────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Step 7: Export                        │
│  - Convert to WAV (primary)            │
│  - Optional: Convert to MP3 (pydub)    │
│  - Save to temporary file              │
│  - Upload to S3                        │
│  - Return file URL + metadata          │
└────────────────────────────────────────┘
```

## 4. Technical Implementation

### 4.1 Core Libraries

**NumPy** (array operations)
- Audio data representation as 1D/2D arrays
- Fast mathematical operations
- Memory-efficient

**SciPy** (signal processing)
- Filtering (butter, lfilter, sosfilt)
- Resampling
- FFT for spectral analysis
- Window functions

**Librosa** (audio processing)
- Pitch shifting
- Time stretching
- Feature extraction
- STFT/ISTFT operations

**Pydub** (format conversion)
- WAV to MP3 conversion
- Audio segment manipulation
- Export with different bitrates

**Soundfile** (I/O)
- Read/write WAV files
- Fast and reliable
- NumPy integration

### 4.2 Audio Parameters

```python
from pydantic import BaseModel, Field
from typing import Literal

class AudioParameters(BaseModel):
    """Parameters for audio generation"""

    # Core parameters (from Claude API)
    duration: float = Field(ge=0.5, le=10.0, description="Duration in seconds")
    wetness: int = Field(ge=0, le=10, description="Liquid/bubbling quality")
    pitch: int = Field(ge=0, le=10, description="Fundamental frequency (0=low, 10=high)")
    type: Literal["squeaker", "rumbler", "stutterer", "classic", "wet"] = "classic"

    # Optional advanced parameters
    reverb_amount: float = Field(default=0.0, ge=0.0, le=1.0)
    distortion: float = Field(default=0.0, ge=0.0, le=1.0)

    # Internal parameters
    randomness_seed: int = Field(default_factory=lambda: int(time.time() * 1000))
    sample_rate: int = Field(default=44100, description="Output sample rate in Hz")
```

### 4.3 Sample Library Structure

```python
# Sample library organization
SAMPLE_LIBRARY = {
    "squeaker": [
        "samples/squeaker_01.wav",  # High-pitched, short
        "samples/squeaker_02.wav",
        "samples/squeaker_03.wav",
    ],
    "rumbler": [
        "samples/rumbler_01.wav",   # Low-pitched, long
        "samples/rumbler_02.wav",
        "samples/rumbler_03.wav",
    ],
    "stutterer": [
        "samples/stutterer_01.wav", # Multiple bursts
        "samples/stutterer_02.wav",
    ],
    "classic": [
        "samples/classic_01.wav",   # Balanced, medium
        "samples/classic_02.wav",
        "samples/classic_03.wav",
        "samples/classic_04.wav",
    ],
    "wet": [
        "samples/wet_01.wav",       # Liquid, bubbling
        "samples/wet_02.wav",
    ],
}
```

**Sample Requirements:**
- Format: WAV, 44.1kHz, mono or stereo
- Duration: 0.5-5 seconds each
- Quality: Professional recordings or high-quality synthesis
- Licensing: Royalty-free or created by team
- Storage: Committed to repo in `assets/samples/`

### 4.4 Core Audio Engine Class

```python
import numpy as np
from scipy import signal
from scipy.io import wavfile
import librosa
import soundfile as sf
from typing import Tuple
import random

class AudioGenerationEngine:
    """Core audio generation engine"""

    def __init__(self, sample_library_path: str = "assets/samples"):
        self.sample_library_path = sample_library_path
        self.sample_cache = {}  # Cache loaded samples
        self._load_samples()

    def _load_samples(self):
        """Preload all samples into memory"""
        for fart_type, sample_paths in SAMPLE_LIBRARY.items():
            self.sample_cache[fart_type] = []
            for path in sample_paths:
                audio, sr = sf.read(path)
                self.sample_cache[fart_type].append((audio, sr))

    def generate(self, params: AudioParameters) -> Tuple[np.ndarray, int]:
        """
        Generate audio based on parameters

        Returns:
            (audio_data, sample_rate) - numpy array and sample rate
        """
        # Set random seed for reproducibility
        np.random.seed(params.randomness_seed)
        random.seed(params.randomness_seed)

        # 1. Select base sample(s)
        base_audio = self._select_and_load_samples(params.type)

        # 2. Generate synthesis layers
        synthesis_layers = self._generate_synthesis_layers(params)

        # 3. Apply parameter transformations
        base_audio = self._apply_transformations(base_audio, params)

        # 4. Mix layers
        mixed_audio = self._mix_layers(base_audio, synthesis_layers, params)

        # 5. Post-process
        final_audio = self._post_process(mixed_audio, params)

        return final_audio, params.sample_rate

    def _select_and_load_samples(self, fart_type: str) -> np.ndarray:
        """Select and load 1-3 random samples of the given type"""
        samples = self.sample_cache[fart_type]
        num_samples = random.randint(1, min(3, len(samples)))
        selected = random.sample(samples, num_samples)

        # If multiple samples, concatenate or overlap
        if len(selected) == 1:
            audio, sr = selected[0]
            return audio
        else:
            # Overlap multiple samples for complexity
            return self._overlap_samples(selected)

    def _generate_synthesis_layers(self, params: AudioParameters) -> dict:
        """Generate procedural synthesis layers"""
        sr = params.sample_rate
        duration_samples = int(params.duration * sr)

        layers = {}

        # Noise layer (always present)
        noise_type = "pink" if params.wetness > 5 else "white"
        layers["noise"] = self._generate_noise(
            duration_samples, sr, noise_type
        )

        # Rumble layer (low frequency oscillations)
        rumble_freq = self._pitch_to_freq(params.pitch)
        layers["rumble"] = self._generate_rumble(
            duration_samples, sr, rumble_freq
        )

        # Bubbling layer (if wet)
        if params.wetness > 5:
            layers["bubbling"] = self._generate_bubbling(
                duration_samples, sr, params.wetness
            )

        return layers

    def _apply_transformations(self, audio: np.ndarray, params: AudioParameters) -> np.ndarray:
        """Apply pitch shifting, time stretching, filters"""

        # Time stretch to match target duration
        current_duration = len(audio) / params.sample_rate
        stretch_factor = params.duration / current_duration
        audio = librosa.effects.time_stretch(audio, rate=stretch_factor)

        # Pitch shift based on pitch parameter
        pitch_shift_semitones = (params.pitch - 5) * 2  # -10 to +10 semitones
        audio = librosa.effects.pitch_shift(
            audio, sr=params.sample_rate, n_steps=pitch_shift_semitones
        )

        # Apply wetness filter
        if params.wetness > 5:
            # More wetness = more low-pass filtering + bubbling
            cutoff_freq = 800 + (10 - params.wetness) * 200
            audio = self._apply_lowpass_filter(audio, cutoff_freq, params.sample_rate)

        return audio

    def _mix_layers(self, base: np.ndarray, layers: dict, params: AudioParameters) -> np.ndarray:
        """Mix base sample with synthesis layers"""

        # Ensure all layers are same length
        target_length = len(base)
        for key in layers:
            layers[key] = self._resize_audio(layers[key], target_length)

        # Mix with weights
        mixed = base * 0.6  # Base sample: 60%
        mixed += layers["noise"] * 0.15  # Noise: 15%
        mixed += layers["rumble"] * 0.20  # Rumble: 20%

        if "bubbling" in layers:
            mixed += layers["bubbling"] * 0.15  # Bubbling: 15%
            mixed *= 0.8  # Reduce overall to prevent clipping

        return mixed

    def _post_process(self, audio: np.ndarray, params: AudioParameters) -> np.ndarray:
        """Normalize, limit, fade in/out"""

        # Normalize to prevent clipping
        audio = self._normalize(audio, target_peak=0.95)

        # Apply soft limiter
        audio = np.tanh(audio * 1.2) * 0.9

        # Fade in/out (50ms)
        fade_samples = int(0.05 * params.sample_rate)
        audio = self._apply_fade(audio, fade_samples)

        # Optional reverb
        if params.reverb_amount > 0:
            audio = self._apply_reverb(audio, params.reverb_amount, params.sample_rate)

        return audio

    # Helper methods (implementations below)
    def _generate_noise(self, length: int, sr: int, noise_type: str) -> np.ndarray:
        """Generate white or pink noise"""
        if noise_type == "white":
            return np.random.normal(0, 0.1, length)
        else:  # pink noise
            white = np.random.normal(0, 1, length)
            # Simple pink noise via FFT
            fft = np.fft.fft(white)
            freqs = np.fft.fftfreq(length, 1/sr)
            # 1/f spectrum
            fft = fft / np.sqrt(np.abs(freqs) + 1)
            pink = np.fft.ifft(fft).real
            return pink * 0.1

    def _generate_rumble(self, length: int, sr: int, base_freq: float) -> np.ndarray:
        """Generate low-frequency rumbling"""
        t = np.linspace(0, length/sr, length)

        # Multiple sine waves with slight detuning
        rumble = np.zeros(length)
        for i in range(3):
            freq = base_freq * (0.95 + i * 0.05)  # Slight detuning
            phase = np.random.uniform(0, 2*np.pi)
            rumble += np.sin(2 * np.pi * freq * t + phase) / 3

        # Amplitude modulation for more natural sound
        mod_freq = random.uniform(5, 15)  # 5-15 Hz modulation
        modulator = 0.5 + 0.5 * np.sin(2 * np.pi * mod_freq * t)
        rumble *= modulator

        return rumble * 0.3

    def _generate_bubbling(self, length: int, sr: int, wetness: int) -> np.ndarray:
        """Generate bubbling sounds for wet farts"""
        # Create burst of short sine pops
        audio = np.zeros(length)
        num_bubbles = int(wetness * 5)  # More bubbles for higher wetness

        for _ in range(num_bubbles):
            # Random bubble position
            pos = random.randint(0, length - 1000)
            bubble_length = random.randint(100, 500)
            freq = random.uniform(300, 1000)

            t = np.linspace(0, bubble_length/sr, bubble_length)
            bubble = np.sin(2 * np.pi * freq * t)

            # Envelope
            envelope = np.exp(-t * 50)  # Quick decay
            bubble *= envelope

            # Add to audio
            end_pos = min(pos + bubble_length, length)
            audio[pos:end_pos] += bubble[:end_pos-pos] * 0.1

        return audio

    def _pitch_to_freq(self, pitch: int) -> float:
        """Map pitch parameter (0-10) to frequency (Hz)"""
        # 0 = 40 Hz, 5 = 80 Hz, 10 = 160 Hz
        return 40 * (2 ** (pitch / 5))

    def _apply_lowpass_filter(self, audio: np.ndarray, cutoff: float, sr: int) -> np.ndarray:
        """Apply Butterworth lowpass filter"""
        nyquist = sr / 2
        normalized_cutoff = cutoff / nyquist
        sos = signal.butter(4, normalized_cutoff, btype='low', output='sos')
        return signal.sosfilt(sos, audio)

    def _normalize(self, audio: np.ndarray, target_peak: float = 0.95) -> np.ndarray:
        """Normalize audio to target peak amplitude"""
        peak = np.abs(audio).max()
        if peak > 0:
            return audio * (target_peak / peak)
        return audio

    def _apply_fade(self, audio: np.ndarray, fade_samples: int) -> np.ndarray:
        """Apply fade in/out"""
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)

        audio[:fade_samples] *= fade_in
        audio[-fade_samples:] *= fade_out

        return audio

    def _resize_audio(self, audio: np.ndarray, target_length: int) -> np.ndarray:
        """Resize audio to target length (simple resampling)"""
        if len(audio) == target_length:
            return audio
        elif len(audio) < target_length:
            # Pad with zeros
            return np.pad(audio, (0, target_length - len(audio)))
        else:
            # Truncate
            return audio[:target_length]

    def _apply_reverb(self, audio: np.ndarray, amount: float, sr: int) -> np.ndarray:
        """Simple convolution reverb"""
        # Create simple impulse response
        ir_length = int(0.5 * sr)  # 500ms reverb
        ir = np.random.normal(0, 1, ir_length)
        ir *= np.exp(-np.arange(ir_length) / (sr * 0.2))  # Exponential decay

        # Convolve
        reverb = signal.convolve(audio, ir, mode='same') * amount

        # Mix dry + wet
        return audio * (1 - amount) + reverb * amount
```

## 5. Performance Optimization

### 5.1 Caching
- **Sample Cache**: Load all samples into memory at startup (< 100MB total)
- **Parameter Cache**: Cache generated audio for identical parameters (Redis)

### 5.2 Parallel Processing
- Use NumPy vectorized operations (inherently parallel)
- Consider multiprocessing for batch generations (future)

### 5.3 Profiling Targets
- Sample loading: < 10ms (cached)
- Synthesis generation: < 500ms
- Signal processing: < 1000ms
- Mixing & post-processing: < 500ms
- **Total: < 2.5 seconds**

## 6. Quality Assurance

### 6.1 Automated Tests
- **Unit Tests**: Test each generation step independently
- **Integration Tests**: Test full pipeline with various parameters
- **Regression Tests**: Ensure consistency across code changes

### 6.2 Human Evaluation
- **Blind Tests**: Users rate realism on 1-10 scale
- **A/B Testing**: Compare different synthesis approaches
- **Feedback Loop**: Collect user ratings to improve algorithm

### 6.3 Metrics
- **Audio Quality**: SNR, THD, spectral analysis
- **Variety**: Audio fingerprinting, similarity scores
- **Consistency**: Standard deviation of user ratings

## 7. Future Enhancements

### 7.1 Advanced Synthesis
- **Physical Modeling**: Simulate actual acoustic phenomena
- **Granular Synthesis**: More control over texture
- **Wavetable Synthesis**: Predefined waveforms for specific sounds

### 7.2 Machine Learning (Phase 2)
- **VAE/GAN**: Learn latent representations from samples
- **Neural Audio Synthesis**: End-to-end learning
- **Style Transfer**: Apply characteristics from one sound to another

### 7.3 Real-time Parameter Modulation
- WebSocket streaming of parameter changes
- Live editing of generation in progress

## 8. Open Questions

1. **Sample Sourcing**: Record our own or use royalty-free?
2. **MP3 Encoding**: Use pydub (simple) or ffmpeg (better quality)?
3. **Stereo vs Mono**: Generate stereo for richer sound?
4. **Computational Budget**: Is 3 seconds acceptable for complex sounds?
5. **Quality vs Speed**: Trade-off between realism and generation time?

## 9. References

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Librosa Audio Processing](https://librosa.org/)
- [Audio Synthesis Fundamentals](https://ccrma.stanford.edu/~jos/pasp/)
- [Digital Signal Processing (DSP) Guide](http://www.dspguide.com/)

---

**Next Steps:**
1. Implement core AudioGenerationEngine class
2. Source or record sample library
3. Test with various parameter combinations
4. Optimize for performance
5. Conduct blind tests with users
