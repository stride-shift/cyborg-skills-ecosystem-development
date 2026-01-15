#!/usr/bin/env python3
"""
Script to extract information about cyborg habits, cyborg skills, and the
cyborg skills ecosystem from meeting transcripts using Gemini's large context window.

Uses direct REST API calls with proxy support.
"""

import os
import base64
import json
import subprocess
import tempfile
from pathlib import Path

# Configuration
TRANSCRIPTS_DIR = Path("/home/user/cyborg-skills-ecosystem-development/transcripts")
OUTPUT_FILE = Path("/home/user/cyborg-skills-ecosystem-development/cyborg_ecosystem_extraction.md")

# Use the trial API key from environment
API_KEY = os.environ.get("GEMINI_API_TRIAL") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Neither GEMINI_API_TRIAL nor GEMINI_API_KEY environment variable is set")

HTTP_PROXY = os.environ.get("HTTP_PROXY", "")

# Models to try in order of preference (large context window models)
MODELS_TO_TRY = [
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro",
]


def load_pdf_as_base64(pdf_path: Path) -> str:
    """Load a PDF file and return it as base64 encoded string."""
    with open(pdf_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def try_model_with_curl(model_name: str, payload: dict) -> dict | None:
    """Try to make a request with a specific model using curl (to handle proxy correctly)."""
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"

    print(f"\nTrying model: {model_name}")

    # Write payload to temp file to handle large data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        payload_file = f.name

    try:
        # Use curl with --noproxy "" to force proxy use (needed in this environment)
        cmd = [
            "curl", "-s",
            "--noproxy", "",
            "--proxy", HTTP_PROXY,
            "-H", "Content-Type: application/json",
            "-X", "POST",
            "-d", f"@{payload_file}",
            "--max-time", "600",
            api_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=660)
        response_text = result.stdout

        if not response_text:
            print(f"  Empty response")
            if result.stderr:
                print(f"  Stderr: {result.stderr[:500]}")
            return None

        # Check for HTML error pages
        if response_text.strip().startswith("<!DOCTYPE") or response_text.strip().startswith("<html"):
            if "403" in response_text:
                print(f"  Error 403: Permission denied - API key may not be valid")
            elif "404" in response_text:
                print(f"  Error 404: Model not found")
            else:
                print(f"  HTTP Error in response")
            return None

        # Try to parse as JSON
        try:
            data = json.loads(response_text)

            # Check for API error response
            if "error" in data:
                error = data["error"]
                print(f"  API Error {error.get('code', 'unknown')}: {error.get('message', 'unknown')}")
                return None

            return data
        except json.JSONDecodeError:
            print(f"  Invalid JSON response: {response_text[:200]}")
            return None

    except subprocess.TimeoutExpired:
        print(f"  Request timed out")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None
    finally:
        # Clean up temp file
        try:
            os.unlink(payload_file)
        except:
            pass


def main():
    # Gather all PDF files
    pdf_files = sorted(TRANSCRIPTS_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF transcripts to process")

    if not pdf_files:
        print("No PDF files found!")
        return

    # Build the content parts
    parts = []

    # Add the extraction prompt
    extraction_prompt = """You are an expert analyst tasked with extracting comprehensive information from meeting transcripts.

Please analyze ALL the attached PDF transcripts thoroughly and extract ALL information related to:

1. **CYBORG HABITS** - Extract everything about:
   - What cyborg habits are (definition, concept)
   - How they work
   - Features and functionality
   - User feedback and experiences
   - Development progress and roadmap
   - Any technical implementation details
   - Examples of specific cyborg habits mentioned
   - How users interact with cyborg habits
   - Any metrics or KPIs mentioned

2. **CYBORG SKILLS** - Extract everything about:
   - What cyborg skills are (definition, concept)
   - Types of cyborg skills mentioned
   - How they differ from cyborg habits
   - Technical implementation details
   - Use cases and examples
   - Development status

3. **CYBORG SKILLS ECOSYSTEM** - Extract everything about:
   - The overall vision for the ecosystem
   - Components of the ecosystem
   - How different parts connect
   - Business model or monetization plans
   - Target users/market
   - Integration plans
   - Roadmap and future plans
   - Key stakeholders and their roles
   - Any companies or organizations mentioned (Pragma, Strideshift, Nano Banana, etc.)

Please be EXHAUSTIVE in your extraction. Include:
- Direct quotes where particularly insightful
- Dates and timeline information
- Names of people involved and their roles
- Specific product features discussed
- Technical architecture decisions
- User research findings
- Any metrics, numbers, or data points mentioned

Format your response as a well-organized Markdown document with clear sections and subsections.
Include a summary at the beginning and detailed findings in subsequent sections.
"""

    parts.append({"text": extraction_prompt})

    # Add all PDF files
    print("Loading PDF files...")
    total_size = 0
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"  [{i}/{len(pdf_files)}] Loading: {pdf_path.name}")
        try:
            pdf_base64 = load_pdf_as_base64(pdf_path)
            total_size += len(pdf_base64)
            parts.append({
                "inlineData": {
                    "mimeType": "application/pdf",
                    "data": pdf_base64
                }
            })
        except Exception as e:
            print(f"    Error loading {pdf_path.name}: {e}")

    # Add closing instruction
    parts.append({
        "text": """
Now please analyze all the transcripts above and provide a comprehensive extraction of all information about cyborg habits, cyborg skills, and the cyborg skills ecosystem. Be thorough and detailed.
"""
    })

    print(f"\nTotal parts to send: {len(parts)} (1 prompt + {len(pdf_files)} PDFs + closing)")
    print(f"Total PDF data size: {total_size / 1024 / 1024:.2f} MB (base64 encoded)")
    print("This may take several minutes due to the large context...")

    payload = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": {
            "maxOutputTokens": 65536,
        }
    }

    # Try each model until one works
    result = None
    used_model = None
    for model in MODELS_TO_TRY:
        result = try_model_with_curl(model, payload)
        if result:
            used_model = model
            break

    if not result:
        print("\n" + "="*60)
        print("ERROR: All models failed.")
        print("="*60)
        print("\nPossible causes:")
        print("1. The GEMINI_API_TRIAL key may be invalid or expired")
        print("2. The API key may not have permission for these models")
        print("3. API quota may be exhausted")
        print("\nTo fix:")
        print("1. Get a valid API key from https://aistudio.google.com/")
        print("2. Set it: export GEMINI_API_KEY='your-key-here'")
        print("3. Run this script again")
        return

    print(f"\nSuccess with model: {used_model}")

    # Extract the response text
    try:
        candidates = result.get("candidates", [])
        if not candidates:
            print("No candidates in response")
            print(json.dumps(result, indent=2)[:2000])
            return

        content_parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [p.get("text", "") for p in content_parts if "text" in p]
        result_text = "\n\n".join(text_parts)

        if not result_text:
            print("No text in response")
            print(json.dumps(result, indent=2)[:2000])
            return

    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        print(json.dumps(result, indent=2)[:2000])
        return

    # Save to file
    print(f"\nSaving results to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        f.write(f"# Cyborg Skills Ecosystem - Extracted Information\n\n")
        f.write(f"*Extracted from {len(pdf_files)} meeting transcripts using {used_model}*\n\n")
        f.write("---\n\n")
        f.write(result_text)

    print(f"\nExtraction complete! Results saved to: {OUTPUT_FILE}")
    print(f"\nFirst 2000 characters of output:\n")
    print(result_text[:2000])


if __name__ == "__main__":
    main()
