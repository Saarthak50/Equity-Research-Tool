# Equity Research Tool

A Streamlit app that reads financial news articles from URLs and answers questions about them, with sources.

## What it does

- Takes news article URLs
- Splits and embeds the content, stores it in FAISS
- Answers questions using Groq's LLM, citing sources

## Setup

Clone the repo:

```
git clone https://github.com/Saarthak50/Equity-Research-Tool.git
cd Equity-Research-Tool
```

Install dependencies:

```
pip install -r requirements.txt
```

Get a Groq API key at https://console.groq.com, then copy `.env.example` to `.env` and set it:

```
cp .env.example .env
```

```
GROQ_API_KEY=your_api_key_here
```

Run:

```
streamlit run main.py
```

## Stack

- Streamlit
- Groq (`openai/gpt-oss-120b`)
- FAISS
- LangChain
- sentence-transformers embeddings

## Notes

- `faiss_store_grokai.pkl` is generated locally when you process URLs; it's gitignored, not committed.
- `.env` is gitignored — don't commit your API key.

## Author

[Saarthak50](https://github.com/Saarthak50)
