#!/usr/bin/env python3
"""
Extract quotable moments from transcripts for social media.
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


def extract_quotes(client: anthropic.Anthropic, batch_transcripts: str, batch_num: int, total_batches: int) -> str:
    prompt = f"""Extract quotable moments from these transcripts that would work well for social media (LinkedIn posts, quote cards).

A good quotable moment:
- Is self-contained (makes sense without context)
- Expresses a strong point of view
- Is memorable and shareable
- Is 1-3 sentences max
- Has a slightly provocative or insightful quality

Categories to look for:
1. **Hot Takes** - Contrarian or surprising claims about AI, work, learning
2. **Framework Quotes** - Clear articulations of concepts (Transparent Equipment, Extended Mind, etc.)
3. **Future Predictions** - Statements about where things are heading
4. **Call to Action** - Inspiring statements about what people should do
5. **Problem Statements** - Clear articulation of challenges or pain points

For each quote provide:
- The exact quote
- Speaker (if identifiable)
- Category
- Suggested context/caption for social media

TRANSCRIPTS (Batch {batch_num}/{total_batches}):
---
{batch_transcripts}
---

Extract 20-30 quotable moments from these transcripts."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def consolidate(client: anthropic.Anthropic, extractions: list) -> str:
    combined = "\n\n---\n\n".join([f"## BATCH {i+1}:\n{ext}" for i, ext in enumerate(extractions)])

    prompt = f"""Consolidate these extracted quotes into a social media content bank.

Organize by category:
1. Hot Takes
2. Framework Quotes
3. Future Predictions
4. Calls to Action
5. Problem Statements

For each quote include:
- The quote
- Suggested LinkedIn post format (with hook and context)
- Hashtag suggestions

Remove duplicates, keep the best version of similar quotes.
Select the top 50 most impactful quotes overall.

EXTRACTIONS:
{combined}

Create a ready-to-use social media quote bank."""

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

    print(f"Extracting quotes from {len(pdf_files)} transcripts...")

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
        result = extract_quotes(client, batch, i, len(batches))
        results.append(result)

    print("Consolidating results...")
    final = consolidate(client, results) if len(results) > 1 else results[0]

    output = Path("/home/user/cyborg-skills-ecosystem-development/content/quote_bank.md")
    output.parent.mkdir(exist_ok=True)

    with open(output, "w") as f:
        f.write(f"# Social Media Quote Bank\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        f.write(final)

    print(f"\nSaved to: {output}")


if __name__ == "__main__":
    main()
