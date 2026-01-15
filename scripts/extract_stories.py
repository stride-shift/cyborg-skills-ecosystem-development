#!/usr/bin/env python3
"""
Extract micro-stories and Damascus moments from transcripts.
"""

import os
import sys
from pathlib import Path
import anthropic
from datetime import datetime
import fitz


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        for page in doc:
            text = page.get_text()
            if text:
                text_parts.append(text)
        doc.close()
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def extract_stories(client: anthropic.Anthropic, batch_transcripts: str, batch_num: int, total_batches: int) -> str:
    prompt = f"""You are extracting micro-stories and "Damascus moments" from meeting transcripts about Cyborg Habits and Cyborg Skills.

A "Damascus moment" is defined as: "You have an experience that is so powerful that it changes the rest of your life" - a sudden profound realization about AI's value and potential.

From these transcripts, extract:

1. **MICRO-STORIES** - Any narrative examples, anecdotes, or stories mentioned that illustrate:
   - Someone using AI effectively
   - A transformation or improvement through AI use
   - A before/after scenario
   - A relatable situation where AI helped
   For each story, provide: The story, who it involves (anonymized if needed), which habit it illustrates

2. **DAMASCUS MOMENTS** - Specific instances where someone had a breakthrough realization about AI:
   - What triggered the moment
   - What they realized
   - How it changed their approach

3. **STORY SEEDS** - Incomplete mentions that could be expanded into full stories:
   - Brief references to examples
   - Hypothetical scenarios discussed
   - Analogies that could become narratives

Be thorough - capture every narrative element, even partial ones.

TRANSCRIPTS (Batch {batch_num}/{total_batches}):
---
{batch_transcripts}
---

Extract all stories, moments, and narrative seeds."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def consolidate(client: anthropic.Anthropic, extractions: list) -> str:
    combined = "\n\n---\n\n".join([f"## BATCH {i+1}:\n{ext}" for i, ext in enumerate(extractions)])

    prompt = f"""Consolidate these extracted micro-stories and Damascus moments into a single organized document.

Group them by:
1. **Complete Micro-Stories** (ready to use)
2. **Damascus Moments** (breakthrough realizations)
3. **Story Seeds** (to be developed further)

Within each group, note which of the 7 habits each story best illustrates:
- Explain It, Plan It, Critique It, Guide Me, Imagine It, What If, Improve It

Remove duplicates but preserve all unique details.

EXTRACTIONS:
{combined}

Create a comprehensive story bank organized for use in the book and marketing content."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def main():
    api_key = os.environ.get("CLAUDE_API") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: No API key found.")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    transcripts_dir = Path("/home/user/cyborg-skills-ecosystem-development/transcripts")
    pdf_files = sorted(transcripts_dir.glob("*.pdf"))

    print(f"Extracting micro-stories from {len(pdf_files)} transcripts...")

    transcript_texts = []
    for i, pdf_file in enumerate(pdf_files, 1):
        text = extract_text_from_pdf(str(pdf_file))
        if text:
            transcript_texts.append((pdf_file.name, text))

    MAX_CHARS = 400000
    batches = []
    current_batch = []
    current_chars = 0

    for name, text in transcript_texts:
        formatted = f"\n{'='*60}\n{name}\n{'='*60}\n{text}"
        if current_chars + len(formatted) > MAX_CHARS and current_batch:
            batches.append("\n".join(current_batch))
            current_batch = [formatted]
            current_chars = len(formatted)
        else:
            current_batch.append(formatted)
            current_chars += len(formatted)
    if current_batch:
        batches.append("\n".join(current_batch))

    print(f"Processing {len(batches)} batches...")

    results = []
    for i, batch in enumerate(batches, 1):
        print(f"  Batch {i}/{len(batches)}...")
        result = extract_stories(client, batch, i, len(batches))
        results.append(result)

    print("Consolidating results...")
    final = consolidate(client, results) if len(results) > 1 else results[0]

    output = Path("/home/user/cyborg-skills-ecosystem-development/content/micro_stories.md")
    output.parent.mkdir(exist_ok=True)

    with open(output, "w") as f:
        f.write(f"# Micro-Stories & Damascus Moments Bank\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        f.write(final)

    print(f"\nSaved to: {output}")


if __name__ == "__main__":
    main()
