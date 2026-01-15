#!/usr/bin/env python3
"""
Extract framework explanations and key concepts from transcripts.
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
        return ""


def extract_frameworks(client: anthropic.Anthropic, batch_transcripts: str, batch_num: int, total_batches: int) -> str:
    prompt = f"""Extract all framework explanations and key concept definitions from these transcripts.

Look for explanations of:

1. **CORE PHILOSOPHICAL CONCEPTS**
   - Extended Mind Hypothesis (Andy Clark)
   - Transparent Equipment
   - Natural-Born Cyborgs
   - Cyborg identity and definition

2. **THE 7 HABITS**
   - Explain It
   - Plan It
   - Critique It
   - Guide Me
   - Imagine It
   - What If
   - Improve It
   (Get every explanation, example, and nuance about each)

3. **KEY TERMINOLOGY**
   - Damascus Moments
   - Awareness Asymmetry
   - Behavior Change vs Learning
   - In-Flow-of-Work
   - Functional Whole / Functional Unit

4. **METAPHORS & ANALOGIES**
   - Iron Man metaphor
   - Musician/instrument analogy
   - Pencil analogy
   - Any other analogies used to explain concepts

5. **DIFFERENTIATION**
   - Why this isn't training
   - Why this isn't a course
   - What makes it different from traditional AI training

For each concept, capture:
- Definition/explanation
- Examples given
- Analogies used
- Why it matters

TRANSCRIPTS (Batch {batch_num}/{total_batches}):
---
{batch_transcripts}
---

Extract comprehensive framework content."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def consolidate(client: anthropic.Anthropic, extractions: list) -> str:
    combined = "\n\n---\n\n".join([f"## BATCH {i+1}:\n{ext}" for i, ext in enumerate(extractions)])

    prompt = f"""Consolidate these framework extractions into a comprehensive glossary and concept guide.

Create sections for:

1. **Philosophy & Foundation**
   - Extended Mind Hypothesis
   - Transparent Equipment
   - Cyborg Definition

2. **The 7 Habits** (comprehensive entry for each)
   - Definition
   - How it works
   - Examples
   - Common applications
   - Related prompts

3. **Key Terminology Glossary**
   - Each term with clear definition

4. **Metaphors & Analogies Bank**
   - Each metaphor with full explanation

5. **Positioning & Differentiation**
   - Why this isn't traditional training
   - What makes it unique

Merge duplicate explanations, keeping the richest versions.
This should be THE reference document for all Cyborg Skills concepts.

EXTRACTIONS:
{combined}

Create the definitive framework reference document."""

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

    print(f"Extracting frameworks from {len(pdf_files)} transcripts...")

    transcript_texts = []
    for pdf_file in pdf_files:
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
        result = extract_frameworks(client, batch, i, len(batches))
        results.append(result)

    print("Consolidating results...")
    final = consolidate(client, results) if len(results) > 1 else results[0]

    output = Path("/home/user/cyborg-skills-ecosystem-development/content/framework_reference.md")
    output.parent.mkdir(exist_ok=True)

    with open(output, "w") as f:
        f.write(f"# Cyborg Skills Framework Reference\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        f.write(final)

    print(f"\nSaved to: {output}")


if __name__ == "__main__":
    main()
