from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"


def extract_json(text: str):
    """
    Safely extract JSON array from LLM output.
    """

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response")

    json_text = match.group(0)

    return json.loads(json_text)

class BatchJustificationGenerator:

    def build_prompt(
        self,
        results,
        job_description,
        resume_sections_map
    ):

        candidates = []

        for res in results:

            sections = resume_sections_map[res["resume"]]

            best_text = sections.get(
                res["best_section"], ""
            )[:600]

            candidates.append({
                "resume": res["resume"],
                "decision": res["status"],
                "jd_score": res["jd_score"],
                "market_score": res["market_score"],
                "best_section": res["best_section"],
                "evidence": best_text
            })

        prompt = f"""
You are an AI hiring assistant.

JOB DESCRIPTION:
{job_description}

For EACH candidate below,
generate a short hiring justification.

Return STRICT JSON format:

[
  {{
    "resume": "...",
    "justification": "..."
  }}
]

CANDIDATES:
{json.dumps(candidates, indent=2)}
"""

        return prompt

    # ------------------------------------------------

    def generate(
        self,
        results,
        job_description,
        resume_sections_map
    ):

        prompt = self.build_prompt(
            results,
            job_description,
            resume_sections_map
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
            temperature=0.3,
        )

        content = response.choices[0].message.content

        try:
            return extract_json(content)
        except Exception as e:
            print("⚠ JSON parsing failed")
            return []