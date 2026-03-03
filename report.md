# High-Level to Low-Level Architecture Pipeline — Report

## 1. Purpose

This tool automates the conversion of **high-level business requirements** into **low-level technical specifications** using the Google Gemini large-language model. Given a plain-text description of what a system should do, the tool produces:

| Output Section | Description |
|---|---|
| **System Modules** | Components / microservices, their responsibilities, interfaces, and dependencies. |
| **Database Schemas** | Tables / collections with columns, data types, keys, and relationships. |
| **Pseudo-code** | Algorithmic logic for each module's core functionality. |

## 2. Architecture

```
┌──────────────────┐      ┌────────────────┐      ┌──────────────┐
│  Input (.txt)    │ ───▶ │  generator.py  │ ───▶ │  Output (.md) │
│  Business Reqs   │      │  Gemini API    │      │  Tech Specs   │
└──────────────────┘      └────────────────┘      └──────────────┘
```

- **Input**: A `.txt` file containing high-level business requirements.
- **Processing**: The script sends the requirements to `gemini-2.0-flash` with a structured system prompt that enforces the three output sections.
- **Output**: A well-formatted Markdown file with the full technical specification.

## 3. Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | Google Gemini 2.0 Flash |
| SDK | `google-genai` |
| Config | `python-dotenv` |

## 4. Usage

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=<your-key>

# 3. Run the pipeline
python generator.py sample_requirement.txt output.md
```

## 5. Sample Input / Output

**Input** (`sample_requirement.txt`): A description of an Online Food Delivery Platform with 9 key features including registration, restaurant discovery, order management, real-time tracking, and more.

**Output** (`output.md`): A structured Markdown document containing:
1. Executive Summary
2. System Modules (e.g., Auth Service, Restaurant Service, Order Service, etc.)
3. Database Schemas (Users, Restaurants, MenuItems, Orders, Payments, Reviews, etc.)
4. Pseudo-code for each module's core logic

## 6. How It Works (Hardcoded Pipeline)

The pipeline follows a deterministic, hardcoded flow:

1. **Load config** — reads `GEMINI_API_KEY` from `.env`.
2. **Read input** — parses the business requirements text file.
3. **Construct prompt** — injects the requirements into a fixed system prompt that enforces the three-section output format.
4. **Call Gemini** — sends the prompt to `gemini-2.0-flash` with `temperature=0.4` for consistent results.
5. **Save output** — writes the Markdown response to disk.

The system prompt is hardcoded and ensures every run produces the same structured sections regardless of input domain.
