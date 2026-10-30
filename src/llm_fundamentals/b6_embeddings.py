import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
client = genai.Client()
EMBED_MODEL = "gemini-embedding-001"

url = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
df = pd.read_csv(url).sample(180, random_state=42).reset_index(drop=True)

def embed(texts):
    vectors = []
    for i in range(0, len(texts), 90):             # 90 texts per call (under 100/minute)
        result = client.models.embed_content(model=EMBED_MODEL, contents=texts[i:i + 90])
        vectors += [e.values for e in result.embeddings]
        if i + 90 < len(texts):
            print(f"  embedded {i + 90}/{len(texts)}, waiting 62 s for the per-minute limit...")
            time.sleep(62)
    return np.array(vectors)

def cosine(query_vector, matrix):
    return matrix @ query_vector / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_vector))

doc_vectors = embed(df["text"].tolist())
print(f"{len(df)} messages -> each one is now {doc_vectors.shape[1]} numbers\n")

queries = [
    "the cash machine ate my card",
    "money left my account for something I never bought",
    "what does it cost to send money to another country",
]

for query, query_vector in zip(queries, embed(queries)):
    scores = cosine(query_vector, doc_vectors)
    print(f"Query: {query}")
    for i in scores.argsort()[::-1][:3]:
        print(f"  {scores[i]:.3f}  [{df.loc[i, 'category']}] {df.loc[i, 'text']}")
    print()