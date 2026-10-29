from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

# 1. How big is the context window?
info = client.models.get(model=MODEL)
print("Max input tokens: ", info.input_token_limit)
print("Max output tokens:", info.output_token_limit)

# 2. What happens when the answer hits the output limit?
response = client.models.generate_content(
    model=MODEL,
    contents="Explain what a bank overdraft is.",
    config=types.GenerateContentConfig(max_output_tokens=15),
)
print("\nAnswer with a 15-token limit:", response.text)
print("Finish reason:", response.candidates[0].finish_reason)

# 3. What does the model know about time?
questions = [
    "What is today's date?",
    "Who won the most recent FIFA World Cup, and in which year?",
    "Today is 29 October 2026. Who won the FIFA World Cup held in 2026?",
]
for q in questions:
    answer = client.models.generate_content(model=MODEL, contents=q).text
    print(f"\nQ: {q}\nA: {answer.strip()[:300]}")