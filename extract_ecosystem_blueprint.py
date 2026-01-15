#!/usr/bin/env python3
"""
Focused extraction of Cyborg Skills Ecosystem components, products, and content types.
"""

import os
import sys
from pathlib import Path
import anthropic
from datetime import datetime
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file using PyMuPDF."""
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


def analyze_batch_with_claude(client: anthropic.Anthropic, batch_transcripts: str, batch_num: int, total_batches: int) -> str:
    """Send a batch of transcripts to Claude API for focused ecosystem extraction."""

    prompt = f"""You are extracting information about the "Cyborg Skills Ecosystem" from meeting transcripts.

This is batch {batch_num} of {total_batches}. Focus ONLY on extracting information about:

1. **PRODUCTS & CONTENT FORMATS** - What products are discussed for the ecosystem?
   - Books (what kind? micro-stories? guides?)
   - Audio content (podcasts? audiobooks?)
   - Video content (what types? formats? lengths?)
   - Social media content (LinkedIn? other platforms?)
   - Apps or software tools
   - Games or gamification elements
   - Physical products (cards? decks? materials?)
   - Courses or training programs
   - Newsletters or regular content

2. **MARKETPLACE & DISTRIBUTION**
   - How would these products be sold/distributed?
   - Website plans (cyborgskills.com)
   - Pricing models discussed
   - B2B vs B2C approaches

3. **CONTENT CREATION METHODS**
   - How is content created? (AI-generated? human?)
   - Tools mentioned for content creation
   - Repurposing strategies (e.g., transcript to X)

4. **CAMPAIGNS & THEMES**
   - Any campaign ideas mentioned
   - Content themes or pillars
   - Target audiences

5. **SPECIFIC SKILL CONTENT**
   - Individual skills mentioned (beyond the 7 habits)
   - Skill categories or types
   - "52 skills" concept details

Extract EVERYTHING mentioned about these topics. Include specific quotes where relevant.

TRANSCRIPTS:
---
{batch_transcripts}
---

Extract all ecosystem product and content information from these transcripts."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return message.content[0].text


def consolidate_results(client: anthropic.Anthropic, all_extractions: list) -> str:
    """Consolidate multiple batch extractions into a comprehensive ecosystem blueprint."""

    combined = "\n\n---\n\n".join([f"## BATCH {i+1} EXTRACTION:\n{ext}" for i, ext in enumerate(all_extractions)])

    prompt = f"""Consolidate these extraction reports into a comprehensive blueprint of the Cyborg Skills Ecosystem.

Create a detailed, organized document that captures EVERYTHING discussed about:
- All product types (books, audio, video, social media, apps, games, physical products, courses, newsletters, etc.)
- Distribution and marketplace plans
- Content creation approaches
- Campaign ideas and themes
- Individual skills and skill categories

Be thorough - don't leave anything out. Organize it clearly with sections and bullet points.

EXTRACTIONS TO CONSOLIDATE:
{combined}

---

Create a comprehensive Cyborg Skills Ecosystem Blueprint covering all products, content types, and distribution approaches discussed."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
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

    print(f"Found {len(pdf_files)} PDF files to process")
    print("-" * 60)

    transcript_texts = []
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Extracting: {pdf_file.name}")
        text = extract_text_from_pdf(str(pdf_file))
        if text:
            transcript_texts.append((pdf_file.name, text))

    total_chars = sum(len(t[1]) for t in transcript_texts)
    print("-" * 60)
    print(f"Total extracted text: {total_chars:,} characters")

    MAX_CHARS_PER_BATCH = 400000
    batches = []
    current_batch = []
    current_batch_chars = 0

    for name, text in transcript_texts:
        formatted = f"\n{'='*80}\nTRANSCRIPT: {name}\n{'='*80}\n{text}"
        text_len = len(formatted)
        if current_batch_chars + text_len > MAX_CHARS_PER_BATCH and current_batch:
            batches.append("\n".join(current_batch))
            current_batch = [formatted]
            current_batch_chars = text_len
        else:
            current_batch.append(formatted)
            current_batch_chars += text_len

    if current_batch:
        batches.append("\n".join(current_batch))

    print(f"\nSplit into {len(batches)} batches for processing")
    print("-" * 60)

    batch_results = []
    for i, batch in enumerate(batches, 1):
        print(f"\n[Batch {i}/{len(batches)}] Analyzing ecosystem content...")
        try:
            result = analyze_batch_with_claude(client, batch, i, len(batches))
            batch_results.append(result)
            print(f"[Batch {i}/{len(batches)}] Complete")
        except anthropic.APIError as e:
            print(f"API Error on batch {i}: {e}")
            sys.exit(1)

    print("\n" + "-" * 60)
    if len(batch_results) > 1:
        print("Consolidating ecosystem blueprint...")
        try:
            final_result = consolidate_results(client, batch_results)
        except anthropic.APIError as e:
            print(f"API Error during consolidation: {e}")
            final_result = "\n\n---\n\n".join([f"## BATCH {i+1}:\n{r}" for i, r in enumerate(batch_results)])
    else:
        final_result = batch_results[0]

    output_file = Path("/home/user/cyborg-skills-ecosystem-development/ecosystem_blueprint.md")
    with open(output_file, "w") as f:
        f.write(f"# Cyborg Skills Ecosystem Blueprint\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"---\n\n")
        f.write(final_result)

    print(f"\n{'='*60}")
    print("EXTRACTION COMPLETE!")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    print(f"\n{'-'*60}\n")
    print(final_result)


if __name__ == "__main__":
    main()
