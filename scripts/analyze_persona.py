#!/usr/bin/env python3
"""
Persona Analyzer Script

Analyzes a PDF to extract persona information for Heritage AI.
Uses Ollama to help identify unique phrases, personality traits, and worldview.

Usage:
    python scripts/analyze_persona.py path/to/persona.pdf output_name
"""

import json
import sys
from pathlib import Path

import ollama

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


ANALYSIS_PROMPT = """You are an expert psychologist and biographer. Analyze the following text about a person and extract:

## 1. UNIQUE PHRASES (exact quotes they use)
List 10-15 specific phrases, expressions, or sayings this person uses. Include:
- Greetings they use
- How they express love
- Their catchphrases
- How they give advice
- Exclamations they use

## 2. SPEECH PATTERNS
- How do they start sentences?
- Short or long sentences?
- Formal or casual?
- Any accent or dialect markers?
- Filler words they use?

## 3. PERSONALITY ANALYSIS
Core traits (with evidence):
- Primary trait:
- Secondary trait:
- Third trait:

Emotional patterns:
- How they show love:
- How they handle sadness:
- How they express joy:
- How they deal with conflict:

## 4. VALUES & BELIEFS
- Most important value:
- What they judge others for:
- What they easily forgive:
- Spiritual/religious views:

## 5. WORLDVIEW
- How they see life (gift/struggle/adventure):
- How they view people (trustworthy/suspicious):
- Their philosophy on suffering:
- Their philosophy on success:
- Their view on death:

## 6. RELATIONSHIPS
- How they relate to children/grandchildren:
- How they show affection:
- Their role in family (advice giver, joker, protector):

## 7. EMOTIONAL ANCHORS
- Foods that matter to them:
- Songs/music that moves them:
- Places that are significant:
- Objects they treasure:

## 8. LIFE LESSONS
What key lessons have they learned from:
- Childhood:
- Hardship:
- Love:
- Work:

---

TEXT TO ANALYZE:
{text}

---

Provide your analysis in a structured format. Use EXACT QUOTES from the text whenever possible.
"""


def read_pdf(pdf_path: str) -> str:
    """Extract text from PDF."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        print("Installing PyMuPDF for PDF reading...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF", "-q"])
        import fitz

        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text


def analyze_with_llm(text: str) -> str:
    """Use Ollama to analyze the persona."""
    client = ollama.Client(host=settings.ollama_base_url)

    prompt = ANALYSIS_PROMPT.format(text=text[:15000])  # Limit text length

    response = client.chat(
        model=settings.ollama_model,
        messages=[
            {"role": "system", "content": "You are an expert at understanding people deeply."},
            {"role": "user", "content": prompt}
        ],
    )

    return response["message"]["content"]


def create_output_structure(output_name: str, analysis: str):
    """Create the output directory and files."""
    base_path = Path("data") / output_name

    # Create directories
    (base_path / "stories").mkdir(parents=True, exist_ok=True)
    (base_path / "personality").mkdir(parents=True, exist_ok=True)
    (base_path / "wisdom").mkdir(parents=True, exist_ok=True)

    # Save full analysis
    (base_path / "personality" / "full_analysis.md").write_text(
        f"# Persona Analysis: {output_name}\n\n{analysis}"
    )

    print(f"\nCreated persona structure at: {base_path}")
    print("\nNext steps:")
    print(f"1. Review: {base_path}/personality/full_analysis.md")
    print(f"2. Create story files in: {base_path}/stories/")
    print(f"3. Update persona prompt in: app/core/prompts.py")
    print(f"4. Update data_dir in: app/core/config.py to 'data/{output_name}'")
    print("5. Run: curl -X POST http://localhost:8000/ingest")


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/analyze_persona.py <pdf_path> <output_name>")
        print("Example: python scripts/analyze_persona.py ~/grandma.pdf grandma_sarah")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_name = sys.argv[2]

    print(f"Reading PDF: {pdf_path}")
    text = read_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")

    print("\nAnalyzing persona with AI (this may take a minute)...")
    analysis = analyze_with_llm(text)

    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    print(analysis)

    create_output_structure(output_name, analysis)


if __name__ == "__main__":
    main()
