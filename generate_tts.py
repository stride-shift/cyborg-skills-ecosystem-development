#!/usr/bin/env python3
"""
Generate TTS audio using Gemini 2.5 Pro TTS
"""

import os
import wave
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_TRIAL")

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Script 1: Meeting to Summary - Full script, rewritten for genuine delivery
script_text = """
What if your meeting notes wrote themselves and actually captured what mattered?

Here's the thing. Most people leave meetings with scattered notes, or worse, no notes at all. The information starts fading within hours. We've all been there. Back-to-back meetings, trying to remember who said what, what we actually decided.

But with this one skill, you'll turn any meeting transcript into a structured, actionable summary before you've even left the room. And I mean sixty seconds.

So here's what a typical meeting transcript looks like. It's messy. It's long. People talking over each other, tangents about someone's weekend, that one person who always goes off-topic.

Now, here's the prompt. Ready?

"Summarize this meeting with key decisions, action items with owners, open questions, and next steps."

That's it. Paste your transcript, add that prompt, and watch what happens.

Look at this output. Clean sections. Decisions clearly stated. Action items with actual names attached, not just "someone should follow up." Open questions flagged so nothing falls through the cracks.

But here's where it gets better. You can refine it. Try this: "Add deadlines mentioned and highlight any risks discussed."

Now you've got a document that's better than anything you'd write manually. And it took thirty seconds.

Here's something most people don't realize. You can adapt this for different audiences instantly.

Same transcript, new prompt: "Create a two-sentence version for Slack."

Done. Executive summary for your boss, detailed version for the team, Slack update for stakeholders. Same meeting, three formats, under two minutes total.

The people who use this consistently become known as the person who always has their act together. The one who sends the clear follow-up.

Meeting to Summary is your first step toward what I call Meeting to Execution. Start with summaries, then graduate to having AI draft the actual deliverables discussed. The meeting ends, the work begins automatically.

Try this with your next meeting transcript. Just that one prompt. Next week, we go beyond summaries to actual outputs.
"""

# Style prompt incorporating the accent guide
style_prompt = """Speak with genuine interest and natural expressiveness. Engaging but grounded, not theatrical or salesy.
South African international accent - warm and clear.
Vary your pace and emphasis to keep it interesting - slow down on key insights, let important points land.
Sound like someone who actually finds this useful and wants to share it, not someone performing excitement."""

# Combine prompt and text for Vertex AI API format
full_content = f"{style_prompt}: {script_text}"

def main():
    print("Initializing Gemini client...")

    # Initialize client with API key
    client = genai.Client(api_key=API_KEY)

    print("Generating TTS audio...")
    print(f"Model: gemini-2.5-pro-preview-tts")
    print(f"Voice: Charon (Male)")
    print("-" * 50)

    try:
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

        # Extract audio data
        if response.candidates and response.candidates[0].content.parts:
            audio_data = response.candidates[0].content.parts[0].inline_data.data

            output_file = "meeting_to_summary_full.wav"
            wave_file(output_file, audio_data)
            print(f"\nAudio saved to: {output_file}")
            print(f"File size: {len(audio_data)} bytes")
        else:
            print("No audio data in response")
            print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
