#!/usr/bin/env python3
"""
Script to extract cyborg habits, cyborg skills, and cyborg skills ecosystem
information from transcription PDF files using Claude API.

Processes transcripts in batches to handle large context, then consolidates results.
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
    """Send a batch of transcripts to Claude API for analysis."""

    prompt = f"""You are an expert analyst extracting information about "Cyborg Habits", "Cyborg Skills", and the "Cyborg Skills Ecosystem" from meeting transcripts.

This is batch {batch_num} of {total_batches}. Extract ALL relevant information from these transcripts.

Focus on extracting information about:
1. **Cyborg Habits** - What they are, how they work, features, usage, development, implementation
2. **Cyborg Skills** - Types, how they relate to cyborg habits, technical details
3. **Cyborg Skills Ecosystem** - Components, interactions, vision, business/technical discussions
4. **Key Concepts & Terminology** - Specific terms and frameworks
5. **People & Roles** - Key people and their roles
6. **Technical Implementation** - How systems are built, integrated, deployed
7. **Future Plans & Roadmap** - Future development discussions

Be thorough and include specific quotes where they provide important context.

TRANSCRIPTS:
---
{batch_transcripts}
---

Extract all cyborg-related information from these transcripts, organized by category."""

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
    """Consolidate multiple batch extractions into a final comprehensive report."""

    combined = "\n\n---\n\n".join([f"## BATCH {i+1} EXTRACTION:\n{ext}" for i, ext in enumerate(all_extractions)])

    prompt = f"""You are tasked with consolidating multiple extraction reports about "Cyborg Habits", "Cyborg Skills", and the "Cyborg Skills Ecosystem".

Below are extractions from different batches of meeting transcripts. Please consolidate all this information into a single, comprehensive, well-organized report.

Requirements:
- Merge duplicate information but preserve unique details
- Organize information clearly under appropriate headings
- Maintain chronological context where relevant
- Preserve important quotes
- Create a coherent narrative from all the extracted pieces

EXTRACTIONS TO CONSOLIDATE:
{combined}

---

Please provide a comprehensive consolidated report covering:
1. Cyborg Habits - Complete overview
2. Cyborg Skills - All types and details
3. Cyborg Skills Ecosystem - Full ecosystem description
4. Key Concepts & Terminology
5. People & Roles
6. Technical Implementation Details
7. Future Plans & Roadmap
8. Timeline of Development (if discernible)"""

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
    # Initialize Claude client
    api_key = os.environ.get("CLAUDE_API") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: No API key found. Set CLAUDE_API or ANTHROPIC_API_KEY env var.")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    transcripts_dir = Path("/home/user/cyborg-skills-ecosystem-development/transcripts")

    if not transcripts_dir.exists():
        print(f"Error: Transcripts directory not found: {transcripts_dir}")
        sys.exit(1)

    # Get all PDF files
    pdf_files = sorted(transcripts_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in transcripts directory")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF files to process")
    print("-" * 60)

    # Extract text from all PDFs
    transcript_texts = []

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Extracting: {pdf_file.name}")
        text = extract_text_from_pdf(str(pdf_file))
        if text:
            transcript_texts.append((pdf_file.name, text))
        else:
            print(f"  Warning: No text extracted from {pdf_file.name}")

    total_chars = sum(len(t[1]) for t in transcript_texts)
    print("-" * 60)
    print(f"Total extracted text: {total_chars:,} characters")
    print("-" * 60)

    # Batch transcripts to stay under token limits
    # More conservative: ~4 chars per token, targeting ~150k tokens per batch
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

    # Process each batch
    batch_results = []

    for i, batch in enumerate(batches, 1):
        print(f"\n[Batch {i}/{len(batches)}] Sending {len(batch):,} characters to Claude API...")
        try:
            result = analyze_batch_with_claude(client, batch, i, len(batches))
            batch_results.append(result)
            print(f"[Batch {i}/{len(batches)}] Complete - extracted {len(result):,} characters")
        except anthropic.APIError as e:
            print(f"API Error on batch {i}: {e}")
            sys.exit(1)

    # Consolidate results if multiple batches
    print("\n" + "-" * 60)
    if len(batch_results) > 1:
        print("Consolidating results from all batches...")
        try:
            final_result = consolidate_results(client, batch_results)
        except anthropic.APIError as e:
            print(f"API Error during consolidation: {e}")
            # Fallback: just combine the batch results
            final_result = "\n\n---\n\n".join([f"## BATCH {i+1} RESULTS:\n{r}" for i, r in enumerate(batch_results)])
    else:
        final_result = batch_results[0]

    # Save the results
    output_file = Path("/home/user/cyborg-skills-ecosystem-development/cyborg_extraction_results.md")

    with open(output_file, "w") as f:
        f.write(f"# Cyborg Skills Ecosystem - Information Extraction\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Source:** {len(pdf_files)} transcription files\n\n")
        f.write(f"**Processing:** {len(batches)} batch(es)\n\n")
        f.write(f"---\n\n")
        f.write(final_result)

    print(f"\n{'='*60}")
    print("EXTRACTION COMPLETE!")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    print(f"\n{'-'*60}")
    print("EXTRACTED INFORMATION:")
    print(f"{'-'*60}\n")
    print(final_result)


if __name__ == "__main__":
    main()
