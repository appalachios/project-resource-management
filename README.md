# project-resource-management

This repository contains utilities for analyzing project data. The `autotask_ai_summary.py` script ingests Autotask CSV reports and uses the OpenAI API to generate summaries.

## Requirements
- Python 3.8+
- `openai` Python package (see `requirements.txt`)

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the summarizer with your Autotask CSV export:
   ```bash
   export OPENAI_API_KEY=your-key
   python autotask_ai_summary.py path/to/report.csv
   ```
   Optionally specify `--max-rows` to limit how many rows are sent to OpenAI.
