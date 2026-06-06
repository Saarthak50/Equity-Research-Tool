# 📈 Equity Research Tool

An AI-powered tool that analyzes financial news articles and answers your questions with **cited sources**.

## What It Does

- Takes multiple news article URLs
- Reads and understands all the content
- Lets you ask questions in plain English
- Gives answers backed by actual text from the articles

## How It Works

1. You paste news URLs
2. The tool reads all articles
3. You ask a question (e.g., "What are the risks mentioned?")
4. You get an answer with quotes and sources

## Tech Used

- Streamlit - for the web interface
- Groq LLM - to generate answers
- FAISS - to find relevant information fast
- LangChain - to connect everything

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Sarthak50/Equity-Research-Tool.git
cd Equity-Research-Tool
```

### 2.Install requirements
```pip install -r requirements.txt```

### 3.Get your Groq API key

    1. Go to https://console.groq.com
    2. Sign up and get your free API key

### 4. Create a .env file
  ```GROQ_API_KEY=your_api_key_here```

### 5. Run the app
```streamlit run main.py```

## Project Structure
Equity-Research-Tool/
├── main.py                 # Main app
├── requirements.txt        # Dependencies
├── .env                   # API key (your own)
└── faiss_store_grokai.pkl # Saved data store

## Why I Built This

Reading multiple financial articles and remembering key points is hard. This tool does the reading and remembering for you, so you can focus on asking the right questions.

## Connect

GitHub: Sarthak50
