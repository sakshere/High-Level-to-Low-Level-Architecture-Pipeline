"""
High-Level to Low-Level Architecture Pipeline
===============================================
An AI-based automation tool that converts high-level business requirements
into low-level technical specifications (modules, schemas, pseudo-code)
using the Google Gemini API.

Usage:
    python generator.py <input_file> <output_file>

Example:
    python generator.py sample_requirement.txt output.md
"""

import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash"
MAX_RETRIES = 3
RETRY_DELAYS = [30, 60, 90]  # seconds between retries

SYSTEM_PROMPT = """
You are an expert software architect. Your job is to convert high-level
business requirements into a detailed low-level technical specification.

Given the business requirements provided by the user, produce a comprehensive
technical specification document with the following THREE sections. Use
Markdown formatting throughout.

────────────────────────────────────────────────────────────────────────
SECTION 1 — SYSTEM MODULES
────────────────────────────────────────────────────────────────────────
Identify every discrete module (or microservice / component) required to
implement the system. For each module provide:
  • Module name
  • Responsibility — what it does
  • Key interfaces — methods or API endpoints it exposes
  • Dependencies — which other modules it communicates with

Present the modules in a numbered list.

────────────────────────────────────────────────────────────────────────
SECTION 2 — DATABASE SCHEMAS
────────────────────────────────────────────────────────────────────────
Design the relational (or NoSQL) database schema for the system.
For each table / collection provide:
  • Table / Collection name
  • Columns / Fields with data types
  • Primary keys, foreign keys, and indexes
  • Relationships to other tables (1:1, 1:N, M:N)

Use Markdown tables for clarity.

────────────────────────────────────────────────────────────────────────
SECTION 3 — PSEUDO-CODE
────────────────────────────────────────────────────────────────────────
For each module identified in Section 1, write clear pseudo-code that
describes its core algorithmic logic. Use indented, readable pseudo-code
(not a specific programming language). Cover:
  • Input validation
  • Core business logic steps
  • Error handling
  • Return values

Present the pseudo-code inside fenced code blocks.

────────────────────────────────────────────────────────────────────────
IMPORTANT RULES
────────────────────────────────────────────────────────────────────────
• Be thorough — do NOT skip any module, table, or algorithm.
• Keep the document well-structured with clear Markdown headings.
• Use professional, precise language.
• Start the document with a brief "Executive Summary" paragraph.
""".strip()


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────

def load_api_key() -> str:
    """Load the Gemini API key from the .env file."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: GEMINI_API_KEY is not set.")
        print("  1. Copy .env.example to .env")
        print("  2. Replace 'your_api_key_here' with your actual Gemini API key.")
        sys.exit(1)
    return api_key


def read_requirements(filepath: str) -> str:
    """Read business requirements from a text file."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: Input file '{filepath}' not found.")
        sys.exit(1)
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        print(f"ERROR: Input file '{filepath}' is empty.")
        sys.exit(1)
    return text


def generate_specification(client: genai.Client, requirements: str) -> str:
    """Send the requirements to Gemini and return the technical specification."""
    print("🔄 Sending requirements to Gemini for analysis...")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=requirements,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.4,      # deterministic but still creative
            max_output_tokens=8192,
        ),
    )

    if not response.text:
        print("ERROR: Gemini returned an empty response.")
        sys.exit(1)

    return response.text


def save_output(content: str, filepath: str) -> None:
    """Write the generated specification to a Markdown file."""
    Path(filepath).write_text(content, encoding="utf-8")
    print(f"✅ Technical specification saved to: {filepath}")


# ──────────────────────────────────────────────
# Main pipeline
# ──────────────────────────────────────────────

def main() -> None:
    # --- CLI argument handling ---
    if len(sys.argv) != 3:
        print("Usage: python generator.py <input_file> <output_file>")
        print("Example: python generator.py sample_requirement.txt output.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # --- Step 1: Load API key ---
    print("=" * 60)
    print("  High-Level → Low-Level Architecture Pipeline")
    print("=" * 60)
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    print(f"✅ Gemini client initialized (model: {MODEL_NAME})")

    # --- Step 2: Read input requirements ---
    requirements = read_requirements(input_file)
    print(f"✅ Loaded requirements from: {input_file} ({len(requirements)} chars)")

    # --- Step 3: Generate specification via Gemini ---
    specification = generate_specification(client, requirements)
    print(f"✅ Specification generated ({len(specification)} chars)")

    # --- Step 4: Save output ---
    save_output(specification, output_file)

    # --- Summary ---
    print()
    print("─" * 60)
    print("Pipeline complete!")
    print(f"  Input:  {input_file}")
    print(f"  Output: {output_file}")
    print(f"  Model:  {MODEL_NAME}")
    print("─" * 60)


if __name__ == "__main__":
    main()
