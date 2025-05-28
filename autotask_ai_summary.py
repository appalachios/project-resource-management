import csv
import os
import argparse
from typing import List, Dict

import openai


def load_csv(path: str) -> List[Dict[str, str]]:
    """Load CSV file and return list of rows."""
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def build_prompt(rows: List[Dict[str, str]], max_rows: int = 10) -> str:
    """Build prompt text from CSV rows."""
    selected = rows[:max_rows]
    header = ', '.join(selected[0].keys()) if selected else ''
    lines = [header]
    for row in selected:
        lines.append(', '.join(row.get(col, '') for col in row.keys()))
    table = '\n'.join(lines)
    prompt = (
        "Summarize the following Autotask report data in a concise manner, highlighting key trends "
        "and important metrics.\n" + table
    )
    if len(rows) > max_rows:
        prompt += f"\n(Only first {max_rows} of {len(rows)} rows shown.)"
    return prompt


def summarize(rows: List[Dict[str, str]], api_key: str) -> str:
    """Request an AI-generated summary from OpenAI."""
    client = openai.OpenAI(api_key=api_key)
    prompt = build_prompt(rows)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in IT management that summarizes Autotask reports.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize an Autotask CSV report using OpenAI")
    parser.add_argument("csv_path", help="Path to Autotask CSV report")
    parser.add_argument("--api-key", dest="api_key", help="OpenAI API key. Defaults to OPENAI_API_KEY env var")
    parser.add_argument("--max-rows", type=int, default=10, help="Maximum rows to include in the prompt")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        parser.error("OpenAI API key must be provided via --api-key or OPENAI_API_KEY environment variable")

    rows = load_csv(args.csv_path)
    summary = summarize(rows, api_key)
    print(summary)


if __name__ == "__main__":
    main()
