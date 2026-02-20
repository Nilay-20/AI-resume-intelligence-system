from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL = "llama-3.1-8b-instant"


class MarketGenerator:

    def build_prompt(self, role, market_text):

        return f"""
You are an industry analyst.

Generate a professional market analysis describing:

- current industry expectations
- hiring trends
- responsibilities
- evolving skills
- market demand

ROLE: {role}

WEB DATA:
{market_text}
"""

    def generate_market_context(self, role, cleaned_text):

        prompt = self.build_prompt(role, cleaned_text[:7000])

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
            temperature=0.3,
        )

        return chat_completion.choices[0].message.content