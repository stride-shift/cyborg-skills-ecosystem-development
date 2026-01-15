# Content Creation Pipeline Specification ("Scream Machine")

## Purpose

Create a systematic, AI-powered content production pipeline that transforms raw conversations and ideas into multiple content formats efficiently. Named "Scream Machine" internally, this pipeline:
1. Extracts thought leadership from conversations
2. Transforms single inputs into multiple outputs
3. Maintains consistent voice and quality
4. Scales content production without linear effort increase
5. Feeds all ecosystem content channels

## The Core Concept

**Input**: Conversations, meetings, brainstorms, interviews
**Output**: Blog posts, videos, social content, podcast scripts, infographics, newsletters

> "The output of one process becomes the input for another"

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAW INPUT SOURCES                           │
├─────────────────────────────────────────────────────────────────┤
│  Scream Sessions  │  Client Meetings  │  Expert Interviews  │   │
│  Team Discussions │  Brainstorms      │  Existing Content   │   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSCRIPTION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Gemini Notes  │  Otter.ai  │  Manual Recording  │  Existing    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTRACTION ENGINE                            │
├─────────────────────────────────────────────────────────────────┤
│  Key Insights  │  Quotable Moments  │  Story Seeds  │  Data     │
│  Frameworks    │  Definitions       │  Examples     │  Analogies│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CONTENT TRANSFORMATION                         │
├──────────────────┬──────────────────┬──────────────────────────┤
│   WRITTEN        │    VISUAL        │       AUDIO/VIDEO        │
├──────────────────┼──────────────────┼──────────────────────────┤
│ Blog Posts       │ Infographics     │ Podcast Scripts          │
│ LinkedIn Posts   │ Social Graphics  │ Video Scripts            │
│ Newsletter       │ Slide Decks      │ Audio Clips              │
│ Book Chapters    │ Diagrams         │ Avatar Videos            │
│ Email Sequences  │ Quote Cards      │ Explainer Videos         │
└──────────────────┴──────────────────┴──────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY & BRAND LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  Voice Consistency  │  Brand Guidelines  │  Human Review        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTION CHANNELS                        │
├─────────────────────────────────────────────────────────────────┤
│  Website  │  LinkedIn  │  Email  │  YouTube  │  Podcast Feeds   │
└─────────────────────────────────────────────────────────────────┘
```

## Scream Sessions

### What is a Scream Session?
Dedicated recording sessions specifically for content extraction:
- 30-60 minutes of focused discussion
- Structured topic agenda
- Recording for transcription
- Designed to generate maximum extractable content

### Session Types

#### Type 1: Thought Leadership Extraction
- **Participants**: Justin + interviewer (Kiyasha)
- **Format**: Interview style, probing questions
- **Topics**: Philosophy, frameworks, vision, predictions
- **Output**: 3-5 blog posts, LinkedIn content, book material

#### Type 2: Skill Deep Dive
- **Participants**: Practitioner demonstrating skill
- **Format**: Walkthrough with explanation
- **Topics**: Specific cyborg skills in action
- **Output**: 52 Skills video scripts, tutorials

#### Type 3: Client Story Mining
- **Participants**: Team member who worked with client
- **Format**: Case study interview
- **Topics**: Problem, approach, results, learnings
- **Output**: Case studies, testimonials, examples

#### Type 4: Future Visioning
- **Participants**: Team brainstorm
- **Format**: "Black Mirror style" scenario exploration
- **Topics**: Future possibilities, implications, opportunities
- **Output**: Micro-stories, provocative content, book material

### Session Agenda Template
```
Scream Session: [Topic]
Date: [Date]
Participants: [Names]

1. Opening Hook (5 min)
   - What's the surprising insight we're exploring?
   - Why does this matter now?

2. Core Content (20-30 min)
   - Main concepts/frameworks
   - Examples and stories
   - Contrarian takes
   - Practical applications

3. Quotable Moments (10 min)
   - Deliberately craft soundbites
   - Memorable phrases
   - Tweetable insights

4. Audience Application (10 min)
   - What should people DO with this?
   - Common mistakes to avoid
   - First steps

5. Future Implications (5 min)
   - Where is this going?
   - What changes if people adopt this?
```

## Extraction Engine

### Tool Stack
- **NotebookLM**: Organize transcripts, generate summaries
- **Claude**: Deep extraction, content transformation
- **Custom Prompts**: Standardized extraction templates

### Extraction Prompts

#### Key Insights Extraction
```
Analyze this transcript and extract:
1. Main arguments/theses (numbered)
2. Supporting evidence or examples for each
3. Novel frameworks or models introduced
4. Contrarian or surprising claims
5. Practical applications mentioned
```

#### Quotable Moments
```
Find 10-15 quotable moments from this transcript that:
- Are self-contained (make sense without context)
- Express a strong point of view
- Would work as social media posts
- Are memorable and shareable
Format: "Quote" - brief context
```

#### Story Seeds
```
Identify potential stories or narratives in this transcript:
- Client examples (even if incomplete)
- Analogies that could be expanded
- "Before/after" transformations
- "What if" scenarios mentioned
List each with enough detail to expand later.
```

## Content Transformation

### Written Content

#### Blog Posts (600 words max)
**Input**: 1-2 key insights from transcript
**Process**:
1. Extract core insight
2. Add hook and context
3. Include example/story
4. End with action item
5. Tone check: quirky but professional

**Prompt Template**:
```
Write a 600-word blog post based on this insight: [INSIGHT]

Requirements:
- Hook in first sentence
- Explain the concept clearly
- Include one concrete example
- End with actionable takeaway
- Tone: Confident but not preachy, slightly irreverent
- No jargon without explanation
```

#### LinkedIn Posts
**Input**: Quotable moment + context
**Process**:
1. Start with hook/claim
2. Brief explanation
3. Single example
4. Call to engage (question or CTA)
5. 150-200 words max

**Format Options**:
- Hot take + reasoning
- Story + lesson
- Framework breakdown
- Myth busting

#### Newsletter Sections
**Input**: Week's worth of content
**Process**:
1. Lead story from best blog post
2. Quick hits from other content
3. Skill of the week feature
4. Community/product updates

### Visual Content

#### Infographics
**Input**: Blog post or framework
**Process**:
1. Identify visual structure (list, process, comparison)
2. Extract key points (5-7 max)
3. Generate with Nano Banana or Canva
4. Brand consistency check

#### Social Graphics
**Input**: Quote + context
**Process**:
1. Select impactful quote
2. Choose visual template
3. Generate/design graphic
4. Size for platform (LinkedIn, Twitter)

#### Quote Cards
**Input**: Quotable moments
**Process**:
1. Format quote cleanly
2. Add attribution
3. Apply brand template
4. Generate multiple options

### Audio/Video Content

#### Podcast Scripts
**Input**: Scream session transcript
**Process**:
1. Edit for conversational flow
2. Add intro/outro
3. Insert transitions
4. Mark emphasis points
5. Note music/sound cues

#### Video Scripts (52 Skills)
**Input**: Skill deep dive session
**Process**:
1. Structure into 5-min format
2. Write hook
3. Script demo narration
4. Add summary and CTA
5. Note visual requirements

#### Avatar Video Generation
**Input**: Script
**Process**:
1. Generate voice (11 Labs)
2. Create avatar video (HeyGen)
3. Combine with screen recordings
4. Edit in Canva
5. Add captions

## Quality & Brand Layer

### Voice Guidelines
- **Tone**: Confident, slightly irreverent, accessible
- **Avoid**: Jargon without explanation, hype words, passive voice
- **Include**: Concrete examples, actionable advice, surprising insights
- **Personality**: Smart friend explaining, not professor lecturing

### Brand Consistency
- Visual templates maintained
- Color palette enforced
- Typography standards
- Logo usage rules

### Human Review Points
1. **Extraction**: Verify accuracy of pulled quotes/insights
2. **Transformation**: Check tone and accuracy
3. **Final**: Quality and brand check before publish

## Workflow Implementation

### Weekly Content Rhythm

#### Monday: Scream Session
- 1-hour focused recording
- Topic prepared in advance
- Recording and transcription

#### Tuesday: Extraction
- Process transcript through extraction prompts
- Identify content pieces
- Assign to formats

#### Wednesday-Thursday: Transformation
- Write/generate content pieces
- Create visuals
- Produce audio/video

#### Friday: Review & Schedule
- Quality review
- Brand check
- Schedule for publication

### Content Calendar Integration
| Day | Platform | Content Type |
|-----|----------|--------------|
| Monday | LinkedIn | Insight post |
| Tuesday | Blog | Long-form article |
| Wednesday | LinkedIn | Quote/graphic |
| Thursday | Newsletter | Weekly roundup |
| Friday | LinkedIn | Engagement post |
| Weekend | Buffer | Scheduled reposts |

## Tools & Technology

### Recording & Transcription
- **Gemini Notes**: Meeting transcription
- **Otter.ai**: Alternative transcription
- **Manual upload**: For existing recordings

### Content Processing
- **NotebookLM**: Transcript organization and initial processing
- **Claude**: Deep extraction and transformation
- **Claude Code Skills**: Standardized prompt templates

### Content Creation
- **Nano Banana**: Image generation (~R2/image)
- **Canva**: Design and video editing
- **11 Labs**: Voice generation
- **HeyGen**: Avatar video creation

### Distribution
- **Mailgun/Resend**: Email delivery
- **YouTube**: Video hosting
- **LinkedIn**: Primary social platform
- **Website CMS**: Blog publishing

## Success Metrics

### Production Metrics
- Pieces of content per Scream Session
- Time from session to publication
- Cost per content piece

### Engagement Metrics
- Views/reads per piece
- Engagement rate (likes, comments, shares)
- Click-through to website/products

### Business Metrics
- Leads generated from content
- Pipeline influenced
- Brand awareness growth

## Timeline for Implementation

### Phase 1: Foundation (Weeks 1-2)
- Establish extraction prompts
- Create transformation templates
- Set up tool stack
- First Scream Session

### Phase 2: Rhythm (Weeks 3-6)
- Weekly Scream Sessions
- Full pipeline execution
- Refine based on results
- Build content backlog

### Phase 3: Scale (Weeks 7+)
- Increase session frequency
- Add content types
- Automate where possible
- Train team members

## Dependencies

- NotebookLM access
- Claude API or interface
- Nano Banana access
- 11 Labs account
- HeyGen account
- Canva Pro
- Recording setup

## Open Questions

1. **Session Frequency**: Weekly? Bi-weekly? Multiple per week?
2. **Participants**: Who leads sessions? Rotate interviewers?
3. **Automation Level**: How much human review vs auto-publish?
4. **Content Volume**: How many pieces per session is sustainable?
5. **Guest Content**: External expert sessions?

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Quality inconsistency | Brand damage | Human review gates, style guides |
| Session quality varies | Wasted time | Structured agendas, preparation |
| Extraction misses nuance | Inaccurate content | Human verification of key claims |
| Bottleneck at review | Publishing delays | Clear review SLAs, multiple reviewers |
| Tool dependency | Production stops | Backup tools, documented processes |

---

## Appendix: Sample Extraction

### Input (Transcript Excerpt)
> "The problem isn't knowledge asymmetry anymore. Everyone can access information. It's awareness asymmetry. People just don't know what's possible. They can't imagine using AI for things they've never seen done. That's the real competitive advantage right now—just knowing what's possible."

### Extracted Outputs

**Key Insight**:
The competitive advantage has shifted from knowledge (what you know) to awareness (knowing what's possible with AI).

**Quotable Moment**:
"It's not about knowledge asymmetry anymore—it's awareness asymmetry."

**Blog Post Seed**:
Title: "The New Competitive Advantage Isn't What You Know"
Hook: Knowledge used to be power. Now it's free. So what's the new edge?

**LinkedIn Post**:
Hot take: Your competitive advantage isn't what you know anymore.

Information is essentially free. Everyone has access to the same knowledge.

The new edge? Awareness asymmetry.

Most people don't know what AI can actually do. They can't imagine it because they've never seen it.

The advantage goes to those who are simply aware of what's possible.

This is why "Damascus moments" matter so much—those sudden realizations about AI's potential that change how you work forever.

What's something AI can do that most people in your industry don't realize yet?

**Quote Card**:
"It's not about knowledge asymmetry anymore—it's awareness asymmetry."
— Justin Germishuys

