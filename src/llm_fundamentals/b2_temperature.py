import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

prompt = "Suggest one name for a new savings account for young people. Reply with the name only."

for temperature in [0.0, 1.0, 2.0]:
    answers = []
    for _ in range(4):
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temperature),
        )
        answers.append(response.text.strip())
        time.sleep(4)   # stay under 15 requests per minute

    print(f"\nTemperature {temperature}: {len(set(answers))} different answers out of 4")
    for answer in answers:
        print("  -", answer)