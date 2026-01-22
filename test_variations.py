#!/usr/bin/env python3
"""
Test different voice style variations on the intro
"""

import os
import wave
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_TRIAL")

# Short intro text for testing
INTRO_TEXT = """
What if your meeting notes wrote themselves and actually captured what mattered?

Most people leave meetings with scattered notes, or worse, no notes at all. The information starts fading within hours. Back-to-back meetings, trying to remember who said what, what you actually decided.

With this skill, you turn any meeting transcript into a structured, actionable summary. About sixty seconds of work.
"""

# Different style variations to test
VARIATIONS = {
    "v1_conversational_warm": """Speak like you're genuinely sharing something useful with a friend.
Warm, conversational, naturally expressive. South African international accent.
Let your voice rise and fall naturally. Take your time on key points.""",

    "v2_confident_presenter": """Speak with quiet confidence, like an experienced presenter who knows their material cold.
Engaging but understated authority. South African international accent.
Measured pace with purposeful pauses. Let statements land.""",

    "v3_curious_storyteller": """Speak with genuine curiosity and discovery, like you're exploring an interesting idea out loud.
South African international accent. Thoughtful, with moments of enthusiasm when landing on insights.
Varied rhythm - sometimes quicker, sometimes slower for emphasis.""",

    "v4_direct_mentor": """Speak directly and plainly, like a mentor cutting through the noise.
South African international accent. No fluff, but still warm.
Confident pacing. Emphasis through simplicity, not volume.""",
}


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def main():
    os.makedirs("audio/variations", exist_ok=True)
    client = genai.Client(api_key=API_KEY)

    for name, style in VARIATIONS.items():
        print(f"\nGenerating {name}...")

        full_content = f"{style}: {INTRO_TEXT}"

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

            if response.candidates and response.candidates[0].content.parts:
                audio_data = response.candidates[0].content.parts[0].inline_data.data
                output_file = f"audio/variations/{name}.wav"
                wave_file(output_file, audio_data)
                duration = len(audio_data) / (24000 * 2)
                print(f"  ✓ {name}.wav ({duration:.0f}s)")
            else:
                print(f"  ✗ No audio data")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("\n" + "=" * 50)
    print("Variations saved to: audio/variations/")
    print("=" * 50)


if __name__ == "__main__":
    main()
