# University of Kent Student Assistant Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kent-chatbotassessment.streamlit.app/)

This is a prototype conversational AI student support assistant designed specifically for the University of Kent. It provides an immediate, accurate first point of contact for students regarding admissions, assessments, deadlines, and crucial wellbeing support.

It was built with Streamlit, Google Gemini (2.5 Flash), and a hybrid local/cloud retrieval architecture.

## Overview
Standard chatbots often hallucinate facts or fail when asked highly specific university questions. To solve this, I designed a Hybrid Retrieval-Augmented Generation (RAG) system that uses verified University of Kent data first, and only falls back to live web searches when necessary.

### Key Features I Implemented
1. **Custom Web Scraper:** I built a BeautifulSoup crawler that ingested 95 essential University pages across admissions, funding, and student wellbeing.
2. **Local Vector Database:** The scraped text was split into 218 vectorized chunks and stored locally using a FAISS (Facebook AI Similarity Search) index. This provides the LLM with highly trusted, instant context for student queries.
3. **Deep Hybrid Web Scraper (Live Fallback):** If a student asks a highly recent or unindexed question (like "who is the new Vice-Chancellor?"), the FAISS index might not have the answer. I integrated DuckDuckGo's `ddgs` API to dynamically search the live internet. Rather than just relying on generic search engine snippets, the chatbot physically crawls the topmost URLs using `BeautifulSoup4` in the background, extracting up to 6,000 characters of raw text, and injecting those concrete facts directly into the LLM's context window.
4. **Contextual Query Expansion:** A classic problem with RAG systems is handling follow-up questions (e.g., Q1: "What is the meningitis outbreak?" -> Q2: "Where can I get vaccinated?"). I engineered a conversational memory pipeline that seamlessly concatenates previous user prompts into the background search query, guaranteeing the FAISS and DDGS retrieval engines never lose track of the topic.
5. **Strict Safety Guardrails:** I engineered the system prompt to explicitly refuse medical or psychological advice. If a student mentions severe depression or suicidal ideation, the LLM intercepts the risk and immediately supplies the official University Campus Security number, Student Support emails, and the NHS emergency helplines.
6. **Robust Quota Management:** I implemented graceful degradation try/except blocks to handle `ResourceExhausted` API errors cleanly.
7. **Deep Branding Integration:** I themed the Streamlit UI to match the official University of Kent identity (Navy Blue, Cyan, Overpass Font).
8. **Real-time Streaming UI:** Engineered the Gemini LLM connection to stream the generated responses token-by-token back to the frontend, driving perceived latency limits to near-zero.
9. **Interactive Memory Controls:** Programmed a persistent application sidebar enabling immediate chat context resets via a custom `st.session_state` wiping function.

### Accessibility (a11y) Features
To ensure the chatbot is usable by a diverse student body, I engineered several accessibility features directly into the frontend:
- **WCAG-Compliant Color Contrast:** Interactive elements (buttons, chat bubbles) use the official UKC Cyan hue (`#0085cf`) paired strictly with `color: white`, satisfying WCAG 2.1 AA contrast ratio requirements.
- **High-Contrast Dark Mode Support:** The university logo is wrapped in an inline CSS container with a stark white background (`padding: 5px; border-radius: 8px`). This guarantees it remains 100% legible even if a visually impaired user forces their OS into Dark Mode or a High Contrast accessibility theme.
- **Keyboard Navigation Focus Rings:** I implemented a custom glowing cyan CSS focus halo around the chat input to assist motor-impaired users navigating exclusively via the `TAB` key.
- **Semantic HTML & Screen Reader Support:** The Streamlit DOM tree respects native `<h1>` heading hierarchy and preserves standard `aria-labels` on inputs and buttons, meaning visually impaired users using Apple VoiceOver or NVDA can natively read and interact with the chatbot interface.

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
This app is fully hosted and deployed on Streamlit Community Cloud. You can access the live demo here: **[Kent Student Assistant Chatbot](https://kent-chatbotassessment.streamlit.app/)**

> **Note on Usage Limits:** This prototype utilizes the free tier of the Google Gemini API. As a result, there are strict rate limits on the number of queries allowed per minute. If you encounter a *"high demand"* error message while testing the demo, the API quota has temporarily been reached. Please wait 60 seconds and try your message again!

The hybrid RAG architecture runs natively in the cloud environment, utilizing Streamlit Secrets to manage the Gemini API configuration.
