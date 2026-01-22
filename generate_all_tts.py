#!/usr/bin/env python3
"""
Batch generate TTS for all 12 Cyborg Skills scripts
Rate limited: 5 concurrent requests per minute (free tier)
"""

import os
import wave
import time
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_TRIAL")

# Style prompt for all scripts
STYLE_PROMPT = """Speak with genuine interest and natural expressiveness. Engaging but grounded, not theatrical or salesy.
South African international accent - warm and clear.
Vary your pace and emphasis to keep it interesting - slow down on key insights, let important points land.
Sound like someone who actually finds this useful and wants to share it, not someone performing excitement."""

# All 12 scripts - cleaned up for genuine delivery
SCRIPTS = {
    "01_meeting_to_summary": """
What if your meeting notes wrote themselves and actually captured what mattered?

Most people leave meetings with scattered notes, or worse, no notes at all. The information starts fading within hours. Back-to-back meetings, trying to remember who said what, what you actually decided.

With this skill, you turn any meeting transcript into a structured, actionable summary. About sixty seconds of work.

A typical meeting transcript is messy. Long. People talking over each other, tangents, off-topic discussions.

Here's the prompt:

"Summarize this meeting with key decisions, action items with owners, open questions, and next steps."

Paste your transcript, add that prompt, and you get clean sections. Decisions clearly stated. Action items with actual names attached. Open questions flagged so nothing falls through the cracks.

You can refine it further. Try: "Add deadlines mentioned and highlight any risks discussed."

Now you've got a document that's more thorough than what you'd write manually. About thirty seconds of work.

Something useful: you can adapt this for different audiences instantly.

Same transcript, new prompt: "Create a two-sentence version for Slack."

Executive summary for your boss, detailed version for the team, Slack update for stakeholders. Same meeting, three formats, couple minutes total.

People who use this consistently become the person who sends the clear follow-up. The one with organized notes.

Meeting to Summary is a step toward Meeting to Execution. Start with summaries, then move to having AI draft the actual deliverables discussed.

Try this with your next meeting transcript. That one prompt. Next week, we go beyond summaries to actual outputs.
""",

    "02_meeting_to_execution": """
The deliverable from your meeting could be drafted before you leave the room.

Last week we covered Meeting to Summary. Useful, but a summary is still just documentation. It's not the actual work.

Meeting to Execution flips that. Instead of summarizing what happened, you create what was discussed. Proposals, project plans, briefs, generated from the conversation itself.

Say you just finished a client kickoff meeting. Forty-five minutes of discussion about goals, timelines, concerns, ideas.

Old approach: take notes, schedule time to write the proposal, takes a few days.

New approach: paste that transcript and use this prompt: "Based on this meeting, create a draft project proposal that addresses the key points discussed, including scope, timeline, and budget considerations mentioned."

What comes back isn't perfect on the first pass, but it's most of the way there. It captured the client's stated goals, referenced specific timelines they mentioned, flagged their budget concerns.

Your first draft. In about thirty seconds.

Your human judgment comes in when you review it. Adjust the tone. Add your expertise. But you're editing, not creating from scratch. That's a real difference.

Another variation: strategy session about a new product feature. The prompt shifts: "Based on this discussion, create a product requirements document with user stories, acceptance criteria, and technical considerations mentioned."

Same principle, different output. The meeting generates its own artifacts.

The mindset shift: stop thinking of meetings as time spent talking. Start thinking of them as content creation sessions. Every meeting is a draft waiting to happen.

Your clients and colleagues notice you're fast. You are. You're just not doing it the old way.

Meeting to Execution means the discussion becomes the first draft. You're refining what already exists.

Pick your next important meeting. Have the transcript ready. Create something real from it.
""",

    "03_blog_to_infographic": """
That blog post you spent hours writing could become a visual that gets more engagement.

What most content creators miss: they write something, hit publish, and that's it. One format. One chance to connect.

The same ideas, restructured visually? That's a LinkedIn carousel. An Instagram post. A presentation slide. The work is already done. You're reshaping it.

Say you have a blog post. Two thousand words about productivity habits. Good content, decent traffic. But it's a wall of text that most people skim.

Here's the transformation prompt: "Extract the five to seven key points from this blog post and structure them for an infographic with clear visual hierarchy. For each point, provide a headline, a one-sentence explanation, and a suggested icon or visual element."

You get back the blueprint. Point one: headline, explanation, suggested icon. Point two: same structure. All the way through.

Now you can hand this to a designer. Or take it into Canva yourself. The extraction and structuring is done.

Take it further. Same content, new prompt: "Create three variations. A five-point version for LinkedIn carousel, a three-point version for Instagram, and a single key insight for Twitter."

One blog post becomes four pieces of visual content. Consistent messaging because they came from the same source.

Most prolific content creators aren't writing more. They're transforming more. Same ideas, multiple formats.

The visual version often outperforms the original because people process visuals faster than text. Your infographic might reach people who never would have read the blog.

Blog to Infographic is multiplication. One piece of deep work becomes many pieces of reach.

Take your best performing blog post. Run it through this process. See what visual assets you've been sitting on.
""",

    "04_ui_on_command": """
You could describe an interface and have the layout materialize in front of you.

You have complex information to present. A dashboard. A report. A settings page. You know what you want to communicate, but turning that into a usable interface is where things get stuck.

UI on Command means you describe what you need in plain language and get a structured, usable interface back. Not pretty pictures. Actual layouts you can build.

Say I need a dashboard for a sales team. They need to see pipeline, performance, and priorities.

Here's the prompt: "Design a dashboard layout for a sales team that shows key metrics at a glance, pipeline status, individual performance, and priority actions. Use progressive disclosure so the most important information is immediately visible but details are accessible. Describe each section, its purpose, and the hierarchy of information."

What comes back: top section has today's numbers. Pipeline status with visual progress bars. Performance showing personal metrics with comparison to team average. Priority actions showing what needs attention.

Notice the hierarchy. Most important stuff first. Details available but not overwhelming. That's designing for how people actually process information.

Now adapt it. Same information, different user: "Redesign this dashboard for an executive who only has thirty seconds to check status. What would you prioritize differently?"

You get a second version. Same data, different emphasis. Executive view shows status indicators and one-line summaries. Details are there if they want them, but the quick version tells the story.

You're thinking through information architecture. The AI helps you consider what matters to whom.

This works for settings pages, onboarding flows, email layouts. Anything that presents information to humans.

UI on Command is rapid prototyping of information architecture. You get from idea to structure in minutes. Then designers can make it beautiful.

Think of something you need to present. Data, options, information. Describe what you need.
""",

    "05_deep_dive_research": """
You could become informed on any topic in an afternoon.

We all encounter moments where we need to understand something quickly. A new industry. A technology trend. A competitor's strategy. A domain we've never worked in before.

The old way: hours of reading, tabs everywhere, trying to piece together a coherent picture. And even then, you're not sure if you missed something important.

Deep Dive Research is structured exploration. Asking the right questions in the right sequence.

Say I need to understand the electric vehicle charging infrastructure market. I know nothing about it.

First prompt: "Give me a comprehensive overview of the EV charging infrastructure market. Cover background and history, current state, key players, major trends, and implications for the next five years. Structure this so I could brief an executive after reading it."

That's the foundation. Broad but structured. Now I understand the landscape.

Follow up: "What are the three most controversial or debated aspects of this market right now? Where do experts disagree?"

Now I'm getting nuance. Not just what is, but what's contested. That's where interesting insights live.

Third prompt: "If I were entering this market as a new player, what would I need to understand that isn't obvious from surface-level research? What do insiders know that outsiders miss?"

You're asking for knowledge that takes years to learn through experience.

Finally: "Create a reading list. What are the five most important articles, reports, or resources someone should read to go deeper? Explain why each one matters."

Now you have a curated path forward. Not random searching. Targeted depth.

In about fifteen minutes, you've gone from zero to informed enough to have a real conversation. Maybe not an expert, but informed enough to ask the right questions.

Deep Dive Research is structured curiosity. The right prompts in the right sequence take you from unfamiliar to informed faster than you'd expect.

Pick something you've been meaning to learn about. Take fifteen minutes and go deep.
""",

    "06_competitive_analysis": """
Your competitors are working hard. Do you know what they're working on?

Most competitive analysis is surface level. Visit their website, check their pricing, maybe read a press release. That's not analysis. That's browsing.

Real competitive intelligence means understanding positioning, identifying strengths and weaknesses, mapping strategy, and finding gaps.

Here's competitive analysis that actually matters. Say I'm looking at three competitors in the project management space.

First prompt: "Analyze these three competitors across positioning, stated value proposition, primary target customer, pricing strategy, and key differentiators. Present this as a comparison matrix."

Side by side. Now I can see the landscape.

Surface features don't tell the whole story. Next prompt: "Based on their public communications, marketing, and product focus, what does each competitor seem to believe about where the market is heading? What bets are they making?"

This is strategic. We're not comparing features. We're understanding worldviews. Company A thinks AI integration is the future. Company B is betting on simplicity. Company C is focused on enterprise security. Different beliefs, different strategies.

Next prompt: "Where are the gaps? What customer needs are none of these competitors addressing well? What opportunities exist in the white space?"

This is where competitive analysis becomes strategic planning. You're not just understanding others. You're finding your own path.

Finally: "If I wanted to position against each of these competitors specifically, what would be the strongest messaging angle? Give me a positioning statement that highlights their weakness and my potential strength."

In twenty minutes, you've done analysis you can actually use. And you can update it whenever you want. Competitors change. Your analysis can keep pace.

Competitive analysis isn't about copying what others do. It's about understanding the game well enough to play it differently.

List your top three competitors. Run this analysis. See what you learn.
""",

    "07_tone_matching": """
The same message, said differently, lands completely differently. Are you matching your tone to your audience?

A communication truth most people ignore: it's not just what you say, it's how you say it. The same information, delivered in the wrong tone, gets ignored, misunderstood, or creates friction.

We know this intuitively, but executing it? Switching between formal and casual, technical and accessible, urgent and calm? That takes effort. Unless you have help.

Tone matching in action. I've got an announcement about a product delay. Not fun news. Let's see how the same core message adapts.

First, internal team: "Rewrite this announcement for our internal engineering team. Be direct, acknowledge the challenge, focus on the path forward. Technical details are appropriate."

Straightforward. No spin. Acknowledges the situation, explains the cause, outlines next steps. Engineers appreciate directness.

Same news, different audience: "Now rewrite this for our executive leadership. Focus on business impact, mitigation steps, and timeline. Keep it brief and action-oriented."

Different emphasis. Less technical detail. More focus on outcomes and decisions needed.

One more: "Rewrite this for our customer-facing support team. They'll be getting questions. Help them understand the situation and give them language to use with customers. Empathetic but confident."

See how different that is? Support teams need to feel informed and equipped. The tone is reassuring because they need to reassure others.

The mindset shift: every piece of communication is actually multiple pieces of communication. Same core message, adapted for who's receiving it.

This works for difficult feedback that needs to land gently, exciting news that needs to sound professional, technical explanations that need to make sense to non-technical people.

The skill isn't writing different messages. It's knowing how to transform one message into many.

Tone matching is empathy made practical. You're changing how you say it for who's hearing it.

Take something you need to communicate. Write it three ways for three audiences.
""",

    "08_project_planning": """
Every project that went wrong started with a plan that wasn't good enough.

Planning is where projects are won or lost. But most planning is either too shallow, missing critical details, or too overwhelming, drowning in complexity.

The sweet spot: comprehensive enough to guide real work, clear enough to actually follow.

Project planning that works. Say we're launching a new customer portal. Three-month timeline. Multiple teams involved.

First prompt: "Create a detailed project plan for launching a customer portal. Include phases, major milestones, key workstreams, dependencies between teams, and estimated durations. Structure this so it could guide weekly planning meetings."

What you get: specific phases. Discovery and design. Development. Testing. Launch prep. Each phase has milestones. Each milestone has dependencies mapped.

Where most plans fall short: the details. Go deeper: "For the development phase, break down the work into specific tasks. For each task, identify who owns it, what needs to be true before they can start, and what risks might delay completion."

Task-level detail. Owner clarity. Dependency awareness. Risk flags built in.

A prompt most people don't think to use: "What are we most likely forgetting? What tasks or considerations typically get missed in projects like this? Add a section for commonly overlooked items."

That's experience encoded. It knows what gets forgotten. Integration testing. Documentation. Training. Stakeholder communication.

Finally: "Create a week-one action list. What needs to happen in the first five days to set this project up for success?"

Now you have a starting point. Specific. Actionable.

Good project planning isn't about predicting the future perfectly. It's about thinking through the work completely enough that surprises become manageable.

Take your next project. Run it through this planning sequence.
""",

    "09_scenario_planning": """
The future isn't one thing. It's many possibilities. Are you planning for all of them?

What separates good strategists from everyone else: they don't just plan for what they expect to happen. They plan for what might happen. Multiple scenarios. Different futures. Prepared for each.

Most of us skip this because it's hard. Imagining alternatives takes cognitive effort. But that effort is what prevents getting blindsided.

Scenario planning in action. Say we're deciding whether to expand into a new market. Big decision. Lots of uncertainty.

First prompt: "For a market expansion decision, identify the three or four most critical uncertainties that could shape how this plays out. What factors could go very differently than expected?"

Economic conditions. Regulatory changes. Competitor response. Customer adoption speed. These are the key variables. The things we can't fully predict.

Build scenarios: "Create four distinct scenarios based on different combinations of these uncertainties. For each scenario, give it a name, describe the conditions, and explain what it would mean for our expansion decision."

Scenario one: fast growth, favorable conditions. Scenario two: slow start, eventually successful. Scenario three: aggressive competitor response. Scenario four: regulatory complications.

Four possible futures. Each plausible. Each requiring different responses.

Next: "For each scenario, what would be our best strategic response? What would we do differently in each future?"

Now we're preparing for them. In scenario one, accelerate investment. In scenario three, differentiate harder. In scenario four, build relationships early.

Final prompt: "What actions make sense across all scenarios? What can we do now that helps us regardless of which future materializes?"

These are your robust moves. The things worth doing no matter what.

Scenario planning isn't about predicting the future. It's about preparing for multiple futures. When you've thought through the possibilities, surprises become manageable.

Take an upcoming decision. Identify the key uncertainties. Build your scenarios.
""",

    "10_vibe_engineering": """
You could describe a product and watch it come to life. That's vibe engineering.

The name sounds playful, but the concept is practical. Vibe engineering means using AI to go from concept to working prototype through conversation. You describe what you want, refine it, iterate, and something real emerges.

It's a process. And it changes what individuals can create.

Vibe engineering in action. Say I want to build a simple habit tracking app. Nothing fancy. Just something that helps me stick to new behaviors.

First, describe the vibe: "I want to build a habit tracking app that feels calm and encouraging, not gamified and stressful. Simple interface. Focus on streaks but without making me feel bad when I miss a day. What would this look like? Describe the user experience."

Not starting with features. Starting with feeling. The vibe comes first.

Now structural: "Based on that vision, what are the core screens and interactions? Walk me through how a user would set up a habit, track it daily, and see their progress."

The experience design emerges from the vibe. Calm means minimal notifications. Encouraging means celebrating progress without punishing gaps. These are vibe decisions.

Next: "Now let's get technical. What's the simplest tech stack to build this? What would the data model look like? How would I structure the code?"

From vibe to vision to architecture. Through conversation.

The final step: "Generate the initial code for the core tracking functionality. Keep it simple and well-commented so I can understand and modify it."

Working code. Not perfect. Not production-ready. But real. Something you can run, test, and improve.

The whole journey takes maybe an hour. From idea to functional prototype.

Vibe engineering makes creation more accessible. You need to know what you want and how to describe it. The AI handles the translation.

What have you been wanting to build? Describe the vibe. Start the conversation.
""",

    "11_learning_acceleration": """
You could cut your learning curve in half. Maybe more.

We're all trying to learn things. New skills. New domains. New technologies. It takes longer than we want. Not because we're slow, but because learning efficiently is itself a skill most people never develop.

Learning acceleration is structuring your learning so you get to useful understanding faster. Not shortcuts. Better paths.

How to learn anything faster. Say I want to understand machine learning well enough to work with a data science team. Not become an expert. Just become conversant.

First prompt: "I need to understand machine learning well enough to collaborate with data scientists. I have a business background, not technical. Create a learning plan that gets me to useful understanding in twenty hours of study. What should I learn and in what order?"

Not a textbook curriculum. A practical path. Conceptual foundations first. Then common algorithms as concepts, not math. Then how to evaluate models. Then how to ask good questions. Structured for the specific goal.

Next: "For the conceptual foundations section, teach me the core concepts I need. Explain each one like I'm smart but new to this. Use analogies to business concepts I'd already understand."

Learning happens. Supervised versus unsupervised, explained through business analogies. Training data as experience. Models as decision frameworks. Concepts you can actually grasp.

An important prompt: "What are the common misconceptions people have when learning this? What mistakes am I likely to make in my understanding?"

You're learning what to avoid, not just what to learn. Pre-empting confusion.

Finally: "Give me five questions I should be able to answer if I understand this well. Let me test myself."

Built-in assessment. You know when you've actually learned versus when you just feel like you have.

Learning acceleration isn't about being smarter. It's about being more strategic. The right questions, in the right order, with the right reality checks.

Pick something you've been meaning to learn. Build your accelerated plan.
""",

    "12_decision_making": """
Stuck on a decision? There's a better way than going in circles.

Big decisions are hard. Not because we lack intelligence. Because we lack structure. Our brains get overwhelmed by complexity, emotion, and uncertainty. We go in circles. We second-guess. We delay.

Structured decision making isn't about removing human judgment. It's about creating conditions where human judgment works better.

Decision support in action. Say I'm deciding whether to leave my job for a startup opportunity. Difficult decision. High stakes. High uncertainty.

First, clarify: "Help me think through this career decision. Let's identify what I actually need to decide. What's the core choice here, and what related questions do I need to answer?"

Already useful. The core choice is clear, but there are related questions. Timeline. Negotiation possibilities. Risk tolerance. We're mapping the decision space.

Structure it: "What are the key factors I should weigh in this decision? Help me create a framework for evaluation. What matters most?"

Financial security. Career growth. Learning opportunity. Work-life balance. Mission alignment. Risk tolerance. The factors emerge. Now you can think about each one explicitly instead of them swirling in your head.

An important prompt: "Play devil's advocate for each option. What's the strongest case against taking the startup role? What's the strongest case against staying in my current position?"

We naturally favor one option and dismiss concerns about it. Forcing the counter-argument surfaces what we're avoiding.

Test it: "What additional information would most change my thinking? What do I not know that I should try to learn before deciding?"

Maybe talk to people who've made similar transitions. Maybe negotiate better terms. The decision might need more input before it needs more thinking.

Finally: "If I were advising a friend in exactly this situation, what would I tell them? Help me step outside my own emotional attachment."

Distance creates clarity. The advice we'd give others is often wiser than the choices we make for ourselves.

Decision making isn't about finding the right answer. It's about thinking through the choice completely enough that you can commit with confidence.

Take a decision you've been avoiding. Run it through this process.
"""
}


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def generate_tts(client, script_name, script_text):
    """Generate TTS for a single script."""
    full_content = f"{STYLE_PROMPT}: {script_text}"

    print(f"  Generating: {script_name}...")

    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-tts",
        contents=full_content,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                language_code="en-US",
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Charon",
                    )
                )
            ),
        )
    )

    if response.candidates and response.candidates[0].content.parts:
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        output_file = f"audio/{script_name}.wav"
        wave_file(output_file, audio_data)
        duration = len(audio_data) / (24000 * 2)
        print(f"  ✓ {script_name}.wav ({duration:.1f}s)")
        return True
    else:
        print(f"  ✗ {script_name} - No audio data")
        return False


def main():
    print("=" * 60)
    print("Cyborg Skills TTS Batch Generator")
    print("=" * 60)
    print(f"Model: gemini-2.5-pro-preview-tts")
    print(f"Voice: Charon (Male)")
    print(f"Scripts: {len(SCRIPTS)}")
    print(f"Rate limit: 5 requests/minute (free tier)")
    print("=" * 60)

    # Create output directory
    os.makedirs("audio", exist_ok=True)

    client = genai.Client(api_key=API_KEY)

    script_items = list(SCRIPTS.items())
    batch_size = 5

    for batch_start in range(0, len(script_items), batch_size):
        batch_end = min(batch_start + batch_size, len(script_items))
        batch = script_items[batch_start:batch_end]

        print(f"\nBatch {batch_start // batch_size + 1}: Scripts {batch_start + 1}-{batch_end}")
        print("-" * 40)

        for script_name, script_text in batch:
            try:
                generate_tts(client, script_name, script_text)
            except Exception as e:
                print(f"  ✗ {script_name} - Error: {e}")

        # Wait between batches (except after the last one)
        if batch_end < len(script_items):
            print(f"\nWaiting 65 seconds for rate limit...")
            time.sleep(65)

    print("\n" + "=" * 60)
    print("Generation complete!")
    print(f"Audio files saved to: audio/")
    print("=" * 60)


if __name__ == "__main__":
    main()
