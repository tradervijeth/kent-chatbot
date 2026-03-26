"""
University of Kent Student Support Chatbot
Built with Streamlit + Google Gemini + FAISS RAG pipeline.

Usage:
    streamlit run app.py
"""

import os
import streamlit as st
import base64
import google.generativeai as genai
from dotenv import load_dotenv
from ddgs import DDGS
from retriever import Retriever
from config import SYSTEM_PROMPT, GENERATION_MODEL

# --- Setup ---
load_dotenv(override=True)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


@st.cache_resource
def load_retriever():
    """Load the FAISS retriever once and cache it across reruns."""
    return Retriever()


# --- Page config ---
st.set_page_config(
    page_title="Kent Student Assistant",
    page_icon="🎓",
    layout="centered",
)

# --- UKC Branding ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700&display=swap');

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Overpass', Helvetica, Arial, sans-serif;
    }

    /* Header area */
    .stAppHeader {
        background-color: #101921;
    }

    /* Title styling */
    h1 {
        color: white;
        font-weight: 700;
    }

    /* Chat input focus ring */
    .stChatInput textarea:focus {
        border-color: #0085cf;
        box-shadow: 0 0 0 2px rgba(0, 133, 207, 0.3);
    }

    /* User chat bubble */
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #0085cf;
        color: white;
        border-radius: 16px;
        padding: 12px 16px;
    }

    /* Assistant chat bubble */
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #f0f2f6;
        border-radius: 16px;
        padding: 12px 16px;
    }

    /* Buttons - pill shaped, UKC cyan */
    .stButton > button {
        background-color: #0085cf;
        color: white;
        border: none;
        border-radius: 50px;
        font-family: 'Overpass', sans-serif;
        font-weight: 600;
        padding: 8px 24px;
    }
    .stButton > button:hover {
        background-color: #006ba7;
        color: white;
    }

    /* Expander (Sources) styling */
    .streamlit-expanderHeader {
        color: #0085cf;
        font-weight: 600;
    }

    /* Links in UKC cyan */
    a {
        color: #0085cf;
    }
    .stCaption, .stCaption p {
        color: rgba(255, 255, 255, 0.7);
    }

</style>
""", unsafe_allow_html=True)

# --- Kent Logo ---
with open("kent_logo.png", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()

st.markdown(
    f'<img src="data:image/png;base64,{logo_data}" width="180" style="margin-bottom: 8px; background-color: white; padding: 5px; border-radius: 8px;">',
    unsafe_allow_html=True,
)


# --- Header ---
st.markdown(
    "<h1>🎓 University of Kent Student Assistant</h1>",
    unsafe_allow_html=True,
)
st.caption(
    "Your first point of contact for admissions, assessments, deadlines, "
    "wellbeing support, and general enquiries."
)


# --- Initialise session state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm the University of Kent student support assistant. "
                "I can help with admissions, assessments, deadlines, wellbeing "
                "support, and general enquiries. How can I help you today?"
            ),
            "sources": [],
        }
    ]

# --- Load retriever ---
try:
    retriever = load_retriever()
except FileNotFoundError:
    st.error(
        "Knowledge base not found. Please run `python3 ingest.py` first "
        "to build the FAISS index."
    )
    st.stop()

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📄 Sources"):
                for source in message["sources"]:
                    st.markdown(f"- [{source['title']}]({source['url']})")

# --- Handle user input ---
if prompt := st.chat_input("Ask a question..."):
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "sources": [],
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching university information..."):
            
            # Contextual Query Expansion (Memory for Search Engines)
            # If there's a previous user question, combine it with the current prompt 
            # so FAISS and DDGS understand the context of short follow-up questions.
            search_query = prompt
            if len(st.session_state.messages) >= 4:
                # [-1] is current prompt, [-2] is last assistant reply, [-3] is last user question
                last_user_msg = st.session_state.messages[-3].get("content", "")
                # Only use the first 100 characters so the search engine doesn't get confused by massive paragraphs
                search_query = f"{last_user_msg[:100]} {prompt}"
            
            # Step 1: Retrieve relevant content from RAG using expanded query
            results = retriever.retrieve(search_query)
            context = retriever.format_context(results)

            # Step 1b: Supplement with live web search using expanded query
            web_sources = []
            try:
                with DDGS() as ddgs:
                    # Sometimes site-specific queries return empty lists format, so fallback if needed
                    web_results = list(ddgs.text(f"{search_query} site:kent.ac.uk", max_results=3))
                    if not web_results:
                        web_results = list(ddgs.text(search_query, max_results=3))
                    
                    if web_results:
                        import requests
                        from bs4 import BeautifulSoup
                        
                        web_context_parts = []
                        # 1. Always include the snippets
                        web_context_parts.append("\n".join([r["body"] for r in web_results]))
                        
                        # Save the web sources to display to the user later
                        for r in web_results:
                            web_sources.append({"title": f"Web: {r.get('title', 'Search Result')}", "url": r.get("href", "")})
                        
                        # 2. Scrape the full text of ALL search results to get extremely concrete details
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                        for i, r in enumerate(web_results):
                            url = r.get("href")
                            if url:
                                try:
                                    resp = requests.get(url, headers=headers, timeout=3)
                                    if resp.status_code == 200:
                                        soup = BeautifulSoup(resp.text, 'html.parser')
                                        # Strip out basic fluff and grab text
                                        for script in soup(["script", "style", "nav", "footer"]):
                                            script.decompose()
                                        text = soup.get_text(separator=' ', strip=True)
                                        # Append the first 2000 chars of each to avoid blowing up the token limit
                                        web_context_parts.append(f"\n--- Full Page Content Result {i+1} ({url}) ---\n{text[:2000]}")
                                except Exception:
                                    pass
                                
                        web_context = "\n\n".join(web_context_parts)
                        context += f"\n\nAdditional web search results:\n{web_context}"
            except Exception as e:
                pass  # Fallback to RAG-only if search fails


            # Step 2: Build the prompt with context
            full_prompt = SYSTEM_PROMPT.format(context=context)

            # Step 3: Call Gemini to generate a response
            # Pass the RAG context as a system instruction so it applies to the current turn
            # without mangling the chat history.
            model = genai.GenerativeModel(GENERATION_MODEL, system_instruction=full_prompt)
            chat_history = []
            for msg in st.session_state.messages[1:]:  # skip welcome message
                chat_history.append({
                    "role": msg["role"] if msg["role"] == "user" else "model",
                    "parts": [msg["content"]],
                })

            try:
                # chat_history already includes the latest user prompt from line 167
                response = model.generate_content(
                    contents=chat_history,
                )
                answer = response.text
            except Exception as e:
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    answer = (
                        "⚠️ I'm currently experiencing high demand and have reached "
                        "my usage limit. Please try again in a minute or two. "
                        "If the issue persists, try refreshing the page."
                    )
                else:
                    answer = (
                        "I'm sorry, I encountered an error processing your request. "
                        "Please try again."
                    )

        # Display the response
        st.markdown(answer)

        # Show sources
        sources = [{"title": r["title"], "url": r["url"]} for r in results]
        sources.extend(web_sources)
        
        if sources:
            with st.expander("📄 Sources"):
                for source in sources:
                    st.markdown(f"- [{source['title']}]({source['url']})")

        # Save to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })
