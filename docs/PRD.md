# Product Requirements Document (PRD)
## Fart Generator

**Version:** 2.0
**Last Updated:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal
**Status:** Draft - Revised for Web Application

---

## 1. Executive Summary

The Fart Generator is an AI-powered web application that generates realistic, customizable flatulence sound effects based on natural language prompts. Users describe the fart sound they want ("a long, rumbling fart" or "quick squeaky toot"), and the system uses AI to interpret the prompt and synthesize authentic audio in real-time. The platform includes a full studio experience with user accounts, generation history, favorites, and sound sharing capabilities.

## 2. Background & Motivation

### Problem Statement
Current fart sound effect solutions are limited by:
- Poor audio quality and unrealistic sounds
- Lack of variety and randomization
- No natural language interface for describing desired sounds
- Limited customization options
- No way to save, organize, or share generated sounds
- Require technical knowledge to use (command-line tools, audio software)

### Opportunity
Create an AI-powered web platform that makes generating realistic fart sounds as easy as describing what you want in plain English. Combine the power of LLM-based prompt interpretation with sophisticated audio synthesis to deliver authentic, varied sounds that users can save, organize, and share.

## 3. Goals & Objectives

### Primary Goals
1. **Realism First**: Generate highly realistic, authentic-sounding fart noises (priority #1)
2. **AI-Powered Prompts**: Allow users to describe desired sounds in natural language
3. **Real-Time Generation**: Stream audio generation progress via WebSocket for immediate feedback
4. **Full Studio Experience**: Provide comprehensive tools for saving, organizing, and sharing sounds
5. **User Accounts**: Enable persistent storage of generation history and favorites

### Secondary Goals
1. Allow fine-tuned customization alongside natural language prompts
2. Support multiple audio formats (WAV, MP3, OGG)
3. Build a community sharing platform for popular generations
4. Provide analytics on generation patterns and popular prompts
5. Enable sound collections and playlists

### Non-Goals (Out of Scope for v1.0)
- Native mobile applications (web-responsive only)
- Video generation or animation
- Social media features (likes, comments, follows)
- Monetization or premium tiers
- Third-party API access for developers

## 4. Target Users

### Primary Users
- **Pranksters & Jokesters**: Individuals looking for realistic fart sounds for pranks and entertainment
- **Content Creators**: YouTubers, TikTok creators, streamers who need sound effects for comedy content
- **Casual Users**: Anyone who wants to have fun generating and sharing humorous sounds

### Secondary Users
- **Sound Designers**: Professionals needing quick access to varied flatulence SFX for media projects
- **Educators**: Teaching sound design, audio synthesis, or AI concepts
- **Party Hosts**: Using the app for entertainment at gatherings and events

## 5. User Stories

### Epic 1: AI-Powered Sound Generation
- As a user, I want to describe the fart sound I want in natural language
- As a user, I want to see the AI interpret my prompt and generate audio in real-time
- As a user, I want to play the generated sound immediately in my browser
- As a user, I want to download the sound to my device
- As a user, I want to regenerate with the same prompt if I'm not satisfied

### Epic 2: User Accounts & Authentication
- As a user, I want to create an account with email/password
- As a user, I want to log in and access my saved sounds
- As a user, I want to stay logged in across sessions
- As a user, I want to reset my password if I forget it
- As a user, I want to update my profile settings

### Epic 3: Generation History & Management
- As a user, I want to see all sounds I've previously generated
- As a user, I want to search my history by prompt text
- As a user, I want to filter my history by date or characteristics
- As a user, I want to delete sounds from my history
- As a user, I want to mark sounds as favorites

### Epic 4: Sound Sharing & Discovery
- As a user, I want to share a generated sound via a public link
- As a user, I want to browse sounds shared by other users
- As a user, I want to see the prompt used for shared sounds
- As a user, I want to remix/regenerate from someone else's prompt
- As a user, I want to see trending/popular generations

### Epic 5: Advanced Customization
- As a user, I want to fine-tune parameters (duration, wetness, pitch) after AI interpretation
- As a user, I want to save custom presets for my favorite settings
- As a user, I want to combine multiple prompts for complex sounds
- As a user, I want to apply effects to generated sounds (reverb, echo, etc.)

### Epic 6: Collections & Organization
- As a user, I want to create collections/playlists of my favorite sounds
- As a user, I want to organize sounds with tags and labels
- As a user, I want to export collections as ZIP files
- As a user, I want to share entire collections with others

## 6. Functional Requirements

### 6.1 Frontend UI/UX
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-UI-001 | Provide a text input for natural language prompts | P0 |
| FR-UI-002 | Display real-time generation progress indicator | P0 |
| FR-UI-003 | Show audio waveform visualization during playback | P1 |
| FR-UI-004 | Provide play/pause/download controls for generated sounds | P0 |
| FR-UI-005 | Display generation history in reverse chronological order | P0 |
| FR-UI-006 | Support search and filter on history page | P1 |
| FR-UI-007 | Show favorites/starred sounds in dedicated view | P1 |
| FR-UI-008 | Provide parameter sliders for fine-tuning (duration, wetness, pitch) | P1 |
| FR-UI-009 | Display shared sounds feed/discovery page | P2 |
| FR-UI-010 | Mobile-responsive design for all pages | P0 |
| FR-UI-011 | Dark/light theme toggle | P2 |
| FR-UI-012 | Show AI interpretation of prompt before generation | P1 |

### 6.2 Backend API (WebSocket & REST)
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-API-001 | WebSocket endpoint for real-time audio generation streaming | P0 |
| FR-API-002 | REST endpoint for prompt submission and queuing | P0 |
| FR-API-003 | REST endpoint for fetching user generation history | P0 |
| FR-API-004 | REST endpoint for saving/updating favorites | P1 |
| FR-API-005 | REST endpoint for downloading audio files | P0 |
| FR-API-006 | REST endpoint for sharing sounds (public link generation) | P1 |
| FR-API-007 | REST endpoint for browsing shared/public sounds | P2 |
| FR-API-008 | REST endpoint for collections management (CRUD) | P2 |
| FR-API-009 | Support pagination for all list endpoints | P1 |
| FR-API-010 | Rate limiting per user (e.g., 50 generations/hour) | P1 |

### 6.3 AI/LLM Integration
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-AI-001 | Integrate Claude API for prompt interpretation | P0 |
| FR-AI-002 | Parse LLM output to extract audio parameters (duration, pitch, wetness, type) | P0 |
| FR-AI-003 | Handle ambiguous prompts with sensible defaults | P0 |
| FR-AI-004 | Provide fallback for AI API failures | P1 |
| FR-AI-005 | Cache common prompt interpretations to reduce API calls | P1 |
| FR-AI-006 | Support multi-step prompts (e.g., "like the previous one, but wetter") | P2 |
| FR-AI-007 | Log AI responses for debugging and improvement | P1 |

### 6.4 Authentication & User Management
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-AUTH-001 | Support email/password registration | P0 |
| FR-AUTH-002 | Support email/password login | P0 |
| FR-AUTH-003 | Implement JWT-based authentication | P0 |
| FR-AUTH-004 | Support password reset via email | P1 |
| FR-AUTH-005 | Support OAuth providers (Google, GitHub) | P2 |
| FR-AUTH-006 | Session management with refresh tokens | P0 |
| FR-AUTH-007 | Email verification for new accounts | P2 |
| FR-AUTH-008 | User profile management (update email, password) | P1 |

### 6.5 Database & Storage
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-DB-001 | Store user account information securely (hashed passwords) | P0 |
| FR-DB-002 | Store generation history (prompt, parameters, timestamp) | P0 |
| FR-DB-003 | Store audio files in cloud storage (S3 or equivalent) | P0 |
| FR-DB-004 | Store favorites/starred sounds per user | P1 |
| FR-DB-005 | Store shared sound metadata and access links | P1 |
| FR-DB-006 | Store collections and their associated sounds | P2 |
| FR-DB-007 | Implement soft deletion for user data | P1 |
| FR-DB-008 | Index database for fast queries on history and search | P1 |

### 6.6 Audio Generation Engine
| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| FR-AUDIO-001 | Procedural synthesis using sine waves, noise, and filters | P0 |
| FR-AUDIO-002 | Hybrid approach with pre-made sound samples | P0 |
| FR-AUDIO-003 | Generate sounds with randomization for uniqueness | P0 |
| FR-AUDIO-004 | Support duration range of 0.5-10 seconds | P0 |
| FR-AUDIO-005 | Support wetness parameter (0-10 scale, affects bubbling/liquid) | P0 |
| FR-AUDIO-006 | Support pitch parameter (0-10 scale, affects fundamental frequency) | P0 |
| FR-AUDIO-007 | Output at 44.1kHz sample rate minimum | P1 |
| FR-AUDIO-008 | Normalize audio to prevent clipping | P1 |
| FR-AUDIO-009 | Export to WAV format (primary) | P0 |
| FR-AUDIO-010 | Export to MP3 format (optional) | P2 |
| FR-AUDIO-011 | Support preset sound types (squeaker, rumbler, stutterer, classic, wet) | P1 |

## 7. Non-Functional Requirements

### 7.1 Performance
- **Generation Speed**: Audio generation should complete in < 3 seconds (90th percentile)
- **API Response Time**: REST endpoints should respond in < 200ms (excluding generation)
- **WebSocket Latency**: Real-time updates should stream with < 100ms delay
- **Page Load Time**: Frontend should achieve First Contentful Paint in < 1.5s
- **Concurrent Users**: Support at least 100 concurrent audio generations
- **Database Queries**: All queries should execute in < 100ms

### 7.2 Quality & Realism
- **Primary Goal**: Audio output should be highly realistic and authentic
- **Blind Test Target**: 70%+ of listeners should rate sounds as "very realistic" (7/10 or higher)
- **Variety**: No two consecutive generations should be > 75% similar (audio fingerprinting)
- **AI Accuracy**: LLM should correctly interpret 90%+ of common prompts

### 7.3 Usability
- **Intuitive UI**: New users should be able to generate their first sound within 30 seconds
- **Error Messages**: All errors should have clear, actionable messages
- **Accessibility**: Support keyboard navigation and screen readers (WCAG 2.1 Level AA)
- **Mobile Experience**: Full functionality on mobile devices (responsive design)

### 7.4 Scalability
- **Horizontal Scaling**: Backend should scale horizontally to handle traffic spikes
- **Storage**: Support up to 10,000 users with 100 generations each (1M total sounds)
- **CDN**: Audio files should be served via CDN for fast global delivery
- **Database**: Use connection pooling and read replicas for scalability

### 7.5 Security
- **Authentication**: Secure password hashing (bcrypt/argon2) and JWT tokens
- **Data Protection**: All user data encrypted at rest and in transit (HTTPS)
- **Rate Limiting**: Prevent abuse with per-user and per-IP rate limits
- **Input Validation**: Sanitize all user inputs to prevent XSS, SQLi, etc.
- **API Security**: Implement CORS policies and API authentication

### 7.6 Reliability & Availability
- **Uptime**: Target 99.5% uptime (< 3.65 hours downtime/month)
- **Error Rate**: < 1% error rate for all API requests
- **Data Backup**: Daily automated backups of database
- **Monitoring**: Real-time alerts for errors and performance degradation

### 7.7 Compatibility
- **Browsers**: Support Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Devices**: Support desktop, tablet, and mobile devices
- **Screen Sizes**: Responsive design from 320px to 4K displays
- **Audio Formats**: Playback compatible with all modern browsers

## 8. Success Metrics

### Launch Criteria (v1.0)
- [ ] All P0 functional requirements implemented and tested
- [ ] User registration and authentication working end-to-end
- [ ] Natural language prompt interpretation via Claude API functional
- [ ] Real-time audio generation via WebSocket operational
- [ ] Frontend deployed and accessible from public URL
- [ ] Backend API deployed with monitoring and logging
- [ ] Database with proper migrations and backups configured
- [ ] At least 5 preset sound types available
- [ ] Security audit passed (basic OWASP checks)
- [ ] Mobile-responsive UI tested on iOS and Android

### Success Metrics (Post-Launch)

**Engagement Metrics (First 3 Months)**
- **User Signups**: 1,000+ registered users
- **Active Users**: 30% monthly active user rate
- **Generations**: 10,000+ sounds generated
- **Retention**: 40%+ users return within 7 days
- **Session Duration**: Average 5+ minutes per session

**Quality Metrics**
- **Realism Score**: 70%+ users rate sounds as "very realistic" (user surveys)
- **Prompt Success**: 85%+ of generations match user intent (feedback surveys)
- **Error Rate**: < 2% failed generations
- **AI Interpretation**: 90%+ accuracy on common prompts

**Performance Metrics**
- **Generation Time**: 90th percentile < 3 seconds
- **Page Load**: First Contentful Paint < 1.5s
- **API Latency**: p95 < 300ms for non-generation endpoints
- **Uptime**: 99.5% availability

**Social/Sharing Metrics**
- **Shares**: 20%+ of generated sounds are shared
- **Public Discovery**: 500+ sounds shared publicly
- **Community**: Users browse shared sounds (10%+ engagement rate)

## 9. Technical Considerations

### Technology Stack (Selected)

**Frontend**
- **Framework**: React 18+ with TypeScript
- **State Management**: React Context API or Zustand (lightweight)
- **UI Components**: Tailwind CSS with shadcn/ui or Material-UI
- **Audio Playback**: Web Audio API for playback and visualization
- **WebSocket Client**: native WebSocket API or socket.io-client
- **Build Tool**: Vite for fast development and optimized production builds

**Backend**
- **Framework**: FastAPI (Python 3.11+)
- **WebSocket**: FastAPI WebSocket support with async/await
- **Audio Processing**: NumPy, SciPy for signal processing; pydub for format conversion
- **AI Integration**: Anthropic Claude API (official Python SDK)
- **Authentication**: FastAPI JWT middleware with passlib for password hashing
- **Database ORM**: SQLAlchemy 2.0 with async support
- **Task Queue**: Celery with Redis (for async audio generation if needed)

**Database & Storage**
- **Primary Database**: PostgreSQL 15+ (user data, history, metadata)
- **Cache Layer**: Redis (prompt caching, session storage, rate limiting)
- **File Storage**: AWS S3 or compatible (MinIO for development)
- **CDN**: CloudFront or similar for audio file delivery

**Infrastructure**
- **Hosting**: AWS (EC2/ECS for backend, S3 for frontend, RDS for database)
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Sentry for error tracking, Prometheus + Grafana for metrics
- **Logging**: Structured logging with ELK stack or CloudWatch

### Audio Generation Approach

**Hybrid Synthesis + Samples**
- **Base Sounds**: Library of 10-20 high-quality recorded samples
- **Procedural Modification**: Apply filters, pitch shifting, time stretching
- **Synthesis Components**: Generate noise, bubbling, rumbling with DSP
- **Randomization**: Vary parameters to ensure uniqueness
- **Real-time Streaming**: Generate audio in chunks and stream via WebSocket

**LLM Prompt Interpretation**
- Use Claude API to parse natural language prompts
- Extract parameters: `{duration: 2.5, wetness: 7, pitch: 4, type: "rumbler"}`
- Provide system prompt with audio parameter schema
- Implement fallback rules for common phrases

*(Detailed technical architecture will be documented in Technical RFCs)*

## 10. Dependencies & Assumptions

### External Dependencies
- **Anthropic Claude API**: For natural language prompt interpretation (critical path)
- **AWS Services**: S3 for storage, RDS for database, CloudFront for CDN (or alternatives)
- **Email Service**: SendGrid or AWS SES for password resets and notifications
- **Domain & SSL**: Domain name and SSL certificate for production deployment

### Technical Dependencies
- Python 3.11+ runtime environment
- PostgreSQL 15+ database server
- Redis server for caching and rate limiting
- Node.js 18+ for frontend build process

### Assumptions
- Users have modern web browsers with JavaScript enabled
- Users have stable internet connection for real-time generation
- Users have audio playback capability (speakers/headphones)
- Claude API has sufficient rate limits for expected traffic
- Cost of Claude API calls is acceptable (estimate $0.01-0.05 per generation)

## 11. Timeline & Phasing

### Phase 1: Foundation & Core Generation (v0.1 - MVP)
**Scope:**
- Audio generation engine (hybrid synthesis + samples)
- Claude API integration for prompt interpretation
- Basic FastAPI backend with WebSocket
- Simple React frontend (single generation page)
- No user accounts (generate and download only)
- Local development environment

**Deliverables:**
- Users can enter prompts and generate sounds
- Real-time audio streaming works
- Basic audio parameters (duration, wetness, pitch) functional

### Phase 2: User Accounts & History (v0.5)
**Scope:**
- User registration and authentication (email/password)
- JWT-based session management
- Generation history storage
- PostgreSQL database integration
- User profile page
- Download and replay past generations

**Deliverables:**
- Full authentication flow
- History page with search/filter
- Persistent storage of user data

### Phase 3: Full Studio Experience (v1.0 - Launch)
**Scope:**
- Favorites/starred sounds
- Collections and organization
- Sound sharing with public links
- Discovery feed for shared sounds
- Mobile-responsive UI polish
- Production deployment (AWS)
- Monitoring and analytics

**Deliverables:**
- Complete studio features
- Public sharing functionality
- Production-ready deployment
- Launch-ready product

### Phase 4: Community & Advanced Features (v1.5+)
**Scope:**
- Sound effects (reverb, echo, distortion)
- Custom preset saving
- Multi-step prompts ("like previous, but wetter")
- Analytics dashboard
- OAuth providers (Google, GitHub)
- API rate limit tiers
- Performance optimizations

**Deliverables:**
- Enhanced customization
- Community features
- Scale improvements

## 12. Open Questions

1. **Sample Sourcing**: Where will we get the 10-20 base sound samples? Record ourselves, purchase royalty-free, or use creative commons?
2. **Licensing**: What license for the project? MIT for code? What about audio samples?
3. **Content Moderation**: Do we need moderation for shared sounds? Age restrictions?
4. **Monetization Strategy**: Will this remain free forever? Freemium model? Ads?
5. **Prompt Filtering**: Should we filter offensive prompts or descriptions in shares?
6. **Storage Limits**: How long do we keep generated sounds? Delete after 30 days? Per-user limits?
7. **LLM Costs**: What's our budget for Claude API calls? Can we afford 10K+ generations?
8. **Hosting Costs**: What's acceptable monthly cost for AWS infrastructure?
9. **Domain Name**: What domain should we use? fartgenerator.com? toothoot.io? other?
10. **Privacy Policy & Terms**: Do we need legal review for GDPR, privacy policy, terms of service?

## 13. Appendix

### Glossary
- **Wetness**: The liquid/bubbling quality of the sound (0-10 scale)
- **Pitch**: The fundamental frequency of the sound (0-10 scale)
- **Preset**: A pre-configured set of parameters for a specific fart type (squeaker, rumbler, etc.)
- **Synthesis**: Procedural generation of audio from mathematical functions
- **LLM**: Large Language Model (Claude API) used for interpreting natural language prompts
- **WebSocket**: Real-time bidirectional communication protocol for audio streaming
- **JWT**: JSON Web Token for stateless authentication
- **P0/P1/P2**: Priority levels (P0 = critical, P1 = important, P2 = nice-to-have)

### References
- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [FastAPI WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [React TypeScript Best Practices](https://react-typescript-cheatsheet.netlify.app/)
- [Audio Synthesis Techniques](https://en.wikipedia.org/wiki/Synthesizer)
- [Python Audio Processing with NumPy/SciPy](https://wiki.python.org/moin/Audio/)
- Prior art: Various mobile apps and web-based sound generators

### Wireframes & Design
*(To be created in Technical RFCs and design documents)*

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | Gurneet Sandhu | Initial draft (CLI-focused) |
| 2.0 | 2026-01-09 | Gurneet Sandhu | Major revision: Web app with AI prompts, full studio features |
