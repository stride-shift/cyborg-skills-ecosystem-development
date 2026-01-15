# B2C Platform Specification (cyborgskills.com)

## Purpose

Create a consumer-facing platform where individuals can purchase and access the Cyborg Skills ecosystem products directly, without requiring enterprise/B2B engagement. This platform serves as both:
1. A marketplace for ecosystem products
2. The delivery platform for consumer Cyborg Habits and 52 Skills content

## Target Audience

- **Young professionals** concerned about future relevance in AI-driven world
- **Self-directed learners** wanting to develop AI collaboration skills
- **Individuals** whose organizations haven't adopted Cyborg Habits yet
- **Career transitioners** seeking competitive advantage
- **Knowledge workers** wanting to enhance productivity

## Core Features

### 1. User Registration & Authentication
- Self-service sign-up (distinct from B2B cohort enrollment)
- Email/password authentication
- Social login options (Google, LinkedIn)
- Magic link login for reduced friction
- Account management dashboard

### 2. Payment & Subscription System
- **Stripe integration** for payment processing
- Pricing tiers:
  - Individual Cyborg Habits program (~600 Rand / ~$35 USD)
  - 52 Skills subscription (monthly/annual)
  - Bundle pricing (Habits + Skills)
  - Individual product purchases (book, cards, etc.)
- Payment receipts and history
- Subscription management (pause, cancel, upgrade)

### 3. Cyborg Habits Program (Consumer Version)
- Same 7 habits framework as B2B
- Daily challenges optimized for individual use
- Self-paced with automated email nudges
- Progress tracking (Evidence Map)
- Completion certificates
- **Difference from B2B**: No cohort structure, admin dashboards, or organizational reporting

### 4. 52 Skills Content Library
- Weekly skill videos (5 minutes each)
- Organized by category
- Progressive unlock or full access (subscription dependent)
- Search and filtering
- Bookmarking/favorites
- Progress tracking across skills

### 5. Marketplace
Products available for purchase:
- Cyborg Habits Book (digital)
- Challenge Card Deck (physical, shipped)
- Additional courses/micro-courses
- Premium content bundles
- Future: Games, 3D environments

### 6. Thought Leadership Hub
- Blog content (600-word posts)
- Infographics
- Podcast episodes (embedded player)
- Video content
- Newsletter signup
- **Purpose**: SEO, discovery, value demonstration

### 7. User Dashboard
- Current program progress
- Purchased products access
- Subscription status
- Certificate downloads
- Reflection history
- Skill completion tracking

## Content Requirements

### From Existing Transcripts
- 7 habits explanations and examples
- Damascus moment stories
- Philosophical framework content (Extended Mind, Transparent Equipment)
- Use cases and applications

### New Content Needed
- Consumer-focused challenge sets (not work-specific)
- 52 Skills video scripts and production
- Blog post library
- Marketing copy and landing pages
- Email sequences for consumer journey

## Technical Requirements

### Frontend
- React TypeScript with Vite (consistent with B2B)
- Mobile-responsive design
- Fast page loads
- SEO optimization
- Accessibility compliance

### Backend
- Superbase (PostgreSQL) - can share infrastructure with B2B
- Row-level security for user data isolation
- API endpoints for:
  - User management
  - Payment processing
  - Content delivery
  - Progress tracking

### Payment Integration
- Stripe Checkout for purchases
- Stripe Billing for subscriptions
- Webhook handling for payment events
- Tax handling (international)

### Email System
- Mailgun or Resend (consistent with B2B)
- Consumer-specific sequences:
  - Welcome series
  - Daily challenge reminders
  - Re-engagement campaigns
  - Product announcements
  - Newsletter delivery

### Hosting
- Cloud deployment (consider: Vercel, Netlify, or dedicated cloud)
- CDN for static assets
- Video hosting (YouTube private/unlisted or dedicated solution)

## Integration Points

### With B2B Platform
- Shared content library where applicable
- Shared video assets
- Common design system
- Potentially shared backend infrastructure with isolation

### With Other Ecosystem Components
- **52 Skills Videos**: Primary delivery mechanism
- **Book**: Digital delivery and access
- **Podcast**: Embedded player, RSS feed
- **Newsletter**: Signup integration, subscriber management
- **Card Deck**: E-commerce checkout, shipping integration

## User Journeys

### Journey 1: Discovery → Purchase → Completion
1. Find via search/social media
2. Land on thought leadership content
3. Explore Cyborg Habits offering
4. Purchase individual program
5. Complete 15-17 day program
6. Receive certificate
7. Upsell to 52 Skills subscription

### Journey 2: Subscription User
1. Subscribe to 52 Skills
2. Receive weekly new skill video
3. Access full skill library
4. Track progress across skills
5. Engage with community content

### Journey 3: Product Purchaser
1. Purchase book or card deck
2. Immediate digital access (book) or shipping confirmation (cards)
3. Nurture sequence for additional products
4. Potential upgrade to full program

## Success Metrics

### Acquisition
- Monthly new registrations
- Conversion rate (visitor → signup)
- Cost per acquisition
- Traffic sources

### Revenue
- Monthly recurring revenue (subscriptions)
- One-time purchase revenue
- Average revenue per user
- Lifetime value

### Engagement
- Program completion rate (target: 75%+)
- Daily active users
- Skill video completion rates
- Time on platform

### Retention
- Subscription churn rate
- Repeat purchase rate
- Newsletter engagement

## Timeline

### Phase 1: MVP (4-6 weeks)
- User registration and authentication
- Stripe payment integration
- Consumer Cyborg Habits program delivery
- Basic dashboard
- Landing page and checkout flow

### Phase 2: Content Expansion (6-8 weeks)
- 52 Skills video library (first 12 skills)
- Thought leadership hub
- Newsletter integration
- Email automation sequences

### Phase 3: Marketplace (8-12 weeks)
- Product catalog
- Digital product delivery
- Physical product shipping integration
- Bundle pricing

### Phase 4: Optimization (Ongoing)
- A/B testing
- Conversion optimization
- Additional payment options
- Mobile app consideration

## Dependencies

- **52 Skills Video Series**: Content needed for subscription value
- **Content Pipeline**: Ongoing content production for thought leadership
- **Book**: Digital product for marketplace
- **Stripe Account**: Payment processing setup
- **Domain**: cyborgskills.com configuration

## Open Questions

1. **Pricing Strategy**: What's the right price point for consumer market? Test 600 Rand vs lower entry point?

2. **Content Differentiation**: How much overlap with B2B challenges? Create distinct "personal life" challenges?

3. **Free Tier**: Offer any free content? Free trial? Freemium model?

4. **Physical Products**: Handle shipping in-house or use fulfillment service?

5. **International**: Multi-currency support from day 1? Which markets to target?

6. **Community**: Add community features (forums, discussion)? Or keep simple?

7. **Mobile App**: Native app needed or PWA sufficient?

8. **Video Hosting**: YouTube (free, some limitations) vs dedicated platform (cost, control)?

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low conversion rate | Revenue miss | Strong value proposition, social proof, money-back guarantee |
| Content not ready | Launch delay | MVP with Cyborg Habits only, add 52 Skills post-launch |
| Payment integration issues | Revenue loss | Thorough testing, fallback payment options |
| Support burden | Cost increase | Self-service help center, automated FAQs |
| B2B cannibalization | Revenue mix | Clear differentiation, different pricing, enterprise features |

---

## Appendix: Competitive Positioning

The B2C platform positions Cyborg Skills as:
- **Not a course**: Behavior change, not learning
- **Not AI training**: Habit formation for human-AI collaboration
- **Not productivity tools**: Cognitive enhancement through AI partnership
- **Unique value**: "Transparent equipment" - AI becomes invisible extension of thinking

