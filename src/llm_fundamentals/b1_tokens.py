from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

texts = {
    "English":     "My card has not arrived yet.",
    "Urdu":        "میرا کارڈ ابھی تک نہیں آیا",
    "Roman Urdu":  "Mera card abhi tak nahi aaya",
    "Numbers":     "1234567890 9876543210",
    "Code":        "for i in range(10): print(i)",
    "Rare word":   "pneumonoultramicroscopicsilicovolcanoconiosis",
    "Repeated":    "card card card card card card card card",
}

for name, text in texts.items():
    tokens = client.models.count_tokens(model=MODEL, contents=text).total_tokens
    words = len(text.split())
    print(f"{name:11} | {len(text):3} chars | {words:2} words | {tokens:3} tokens")