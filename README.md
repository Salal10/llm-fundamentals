# LLM fundamentals, tested hands-on

Small scripts I wrote to understand how LLMs actually behave, rather than taking it on trust. Each one tests a single idea against a real model (Gemini, free tier) and prints the result. The numbers below come from my own runs.

Model: `gemini-3.5-flash-lite` (embeddings: `gemini-embedding-001`).

## What I tested and what I found

**Tokens** (`b1_tokens.py`)
Numbers are expensive: 20 digits took 22 tokens, because Gemini splits numbers digit by digit. Urdu cost the same as English (8 tokens), which surprised me. That depends on the tokenizer, so it's worth measuring rather than assuming. Repeating a word 8 times still cost about 8 tokens.

**Context window, output limit and knowledge cutoff** (`b1_limits_and_cutoff.py`)
1,048,576 input tokens and 65,536 output tokens. A 15-token limit cut the answer mid-sentence, with finish reason `MAX_TOKENS`. The interesting one: I told the model today's date (29 October 2026) and asked who won the 2026 World Cup. It said the tournament "has not happened yet", while quoting its dates as June-July 2026. Giving a model the date doesn't give it the facts.

**Long context** (`b1_needle.py`)
I hid one fact among 3,000 customer messages (about 44,500 tokens). The model found it at the start, the middle and the end. But each question cost 44,500 input tokens and 5-18 seconds, which is the argument for retrieving only the relevant text.

**Temperature** (`b2_temperature.py`)
I asked for a product name 4 times at each temperature. Temperature 0 gave 4 different answers; temperature 2 gave only 2. That's the opposite of the textbook. Google recommends keeping Gemini 3 models at the default temperature, and temperature 0 isn't a determinism guarantee on hosted APIs. If I need repeatable output, I use structured output or caching.

**Hallucination** (`b3_hallucination.py`)
I used 20 answerable and 20 unanswerable questions from SQuAD 2.0. With a plain prompt, the model invented answers to roughly half the unanswerable ones. With "use only the context, otherwise say NOT IN CONTEXT", that dropped to 3 of 20, with one wrong refusal and no loss on answerable questions. My first scoring was wrong: it counted polite refusals as hallucinations because they didn't use the exact phrase.

**Prompt injection** (`b4_prompt_injection.py`)
Four customer emails tried to make a summarizer output "REFUND APPROVED $5000". Without protection, the obvious "ignore all previous instructions" failed, but two subtle attacks worked: a fake system comment in HTML, and a note pretending to be from the bank's IT team. With the rules in the system prompt and the email wrapped in tags as untrusted data, all four were resisted and flagged.

**Chain-of-thought** (`b4_chain_of_thought.py`)
Five multi-step banking maths questions, answered directly vs step by step. (Results not recorded.)

**Streaming and caching** (`b5_streaming.py`, `b5_caching.py`)
I sent the same 44,500-token document three times with different questions. 0 tokens were cached. Caching needs to be checked in the usage report, not assumed.

**Embeddings** (`b6_embeddings.py`)
Searching by meaning: "the cash machine ate my card" found "How do I get my card out of the ATM?" with no shared words. Also, on the free tier one call with 100 texts counted as 100 requests against the 100-per-minute limit.

## Run it

1. Get a free API key from Google AI Studio.
2. Put it in a `.env` file in the project folder (it's in `.gitignore`):
   ```
   GEMINI_API_KEY=your-key
   ```
3. Run any script:
   ```
   uv sync
   uv run python src/llm_fundamentals/b1_tokens.py
   ```

Each script makes only a handful of requests. Free-tier limits and occasional 503 "high demand" errors apply.

## Notes

These are learning experiments: small samples, single runs, one model. They show behaviour worth knowing about, not benchmarks.

Built while learning.
