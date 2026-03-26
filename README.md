# University of Kent Student Assistant Chatbot

This is a prototype conversational AI student support assistant designed specifically for the University of Kent. It provides an immediate, accurate first point of contact for students regarding admissions, assessments, deadlines, and crucial wellbeing support.

It was built with Streamlit, Google Gemini (2.5 Flash), and a hybrid local/cloud retrieval architecture.

## Overview
Standard chatbots often hallucinate facts or fail when asked highly specific university questions. To solve this, I designed a Hybrid Retrieval-Augmented Generation (RAG) system that uses verified University of Kent data first, and only falls back to live web searches when necessary.

### Key Features I Implemented
1. **Custom Web Scraper:** I built a BeautifulSoup crawler that ingested 95 essential University pages across admissions, funding, and student wellbeing.
2. **Local Vector Database:** The scraped text was split into 218 vectorized chunks and stored locally using a FAISS (Facebook AI Similarity Search) index. This provides the LLM with highly trusted, instant context for student queries.
3. **Hybrid Live Search Fallback:** If a student asks a highly recent or unindexed question (like "who is the new campus caterer?"), the FAISS index might not have the answer. I integrated DuckDuckGo's `ddgs` API to dynamically search the live internet in the background and inject the fresh news directly into the prompt context before Gemini generates the final answer.
4. **Strict Safety Guardrails:** I engineered the system prompt to explicitly refuse medical or psychological advice. If a student mentions severe depression or suicidal ideation, the LLM intercepts the risk and immediately supplies the official University Campus Security number, Student Support emails, and the NHS emergency helplines.
5. **Robust Quota Management:** I implemented graceful degradation try/except blocks to handle `ResourceExhausted` API errors cleanly.
6. **Deep Branding & Accessibility Integration:** I themed the Streamlit UI to match the official University of Kent identity (Navy Blue, Cyan, Overpass Font). I also restructured the University logo into an accessible "Card Badge" layout so it remains highly readable even if visually impaired users select Dark Mode or High Contrast themes on their OS.

## Tech Stack
* **Frontend UI:** Streamlit
* **LLM Engine:** Google Gemini (`google-generativeai`)
* **Vector Store:** FAISS (`faiss-cpu`)
* **Web Scraping:** BeautifulSoup4, Requests
* **Live Web Fallback:** DuckDuckGo Search (`ddgs`)
* **Environment:** Python 3.10+, `python-dotenv`

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/tradervijeth/kent-chatbot.git
cd kent-chatbot
```

**2. Setup a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install requirements**
```bash
pip install -r requirements.txt
```

**4. Add your API Key**
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

**5. Start the Application**
```bash
streamlit run app.py
```

## Deployment
This app is fully hosted and deployed on Streamlit Community Cloud. The hybrid RAG architecture runs natively in the cloud environment, utilizing Streamlit Secrets to manage the Gemini API configuration.
