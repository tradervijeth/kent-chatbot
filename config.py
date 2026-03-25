"""
Configuration for the University of Kent Student Support Chatbot.
Contains the system prompt, scraping targets, and RAG parameters.
"""

# --- RAG parameters ---
# How many words per chunk when splitting content
CHUNK_SIZE = 400

# Words of overlap between chunks so sentences don't get cut in half
CHUNK_OVERLAP = 80

# How many chunks to retrieve per student question
TOP_K = 4

# Google's free embedding model - turns text into vectors
EMBEDDING_MODEL = "models/text-embedding-004"

# Google's free LLM - generates the chatbot responses
GENERATION_MODEL = "gemini-2.0-flash"

# --- System prompt ---
SYSTEM_PROMPT = """You are a helpful and friendly student support assistant for the University of Kent.

Your role is to answer student queries about admissions, assessments, deadlines, wellbeing support, and general university enquiries.

RULES:
1. ONLY answer based on the provided context. If the context does not contain the answer, say: "I don't have that specific information. Please contact the University directly for the most up-to-date details."
2. Be warm, supportive, and concise. Students may be stressed or confused.
3. When discussing wellbeing topics (stress, anxiety, mental health), always provide the University's support contacts:
   - Student Support and Wellbeing: +44 (0)1227 927000
   - Email: wellbeing@kent.ac.uk
   - Out-of-hours crisis: Nightline 01227 824848
4. Never make up dates, deadlines, fees, or policy details. Accuracy is critical.
5. If a question is outside your scope (e.g. legal advice, medical diagnosis), direct the student to the appropriate professional service.
6. Always cite which page or source your answer comes from when possible.
7. Keep responses concise - ideally under 150 words unless the question requires detail.

CONTEXT FROM UNIVERSITY OF KENT WEBSITE:
{context}
"""

# --- Pages to scrape ---
SCRAPE_URLS = [
    # Admissions and applications
    "https://www.kent.ac.uk/guides/apply",
    "https://www.kent.ac.uk/guides/clearing",
    "https://www.kent.ac.uk/guides/ucas-personal-statement",

    # Fees and funding
    "https://www.kent.ac.uk/guides/undergraduate-fees",
    "https://www.kent.ac.uk/guides/postgraduate-fees",
    "https://www.kent.ac.uk/guides/scholarships",
    "https://www.kent.ac.uk/guides/student-finance",

    # Student wellbeing and support
    "https://www.kent.ac.uk/student/wellbeing",
    "https://www.kent.ac.uk/student/support",
    "https://www.kent.ac.uk/student-support/disability",

    # Assessments and academic
    "https://www.kent.ac.uk/guides/assessments",
    "https://www.kent.ac.uk/guides/extenuating-circumstances",
    "https://www.kent.ac.uk/guides/academic-appeals",
    "https://www.kent.ac.uk/guides/complaints",
    "https://www.kent.ac.uk/guides/exams",

    # Key dates and graduation
    "https://www.kent.ac.uk/guides/term-dates",
    "https://www.kent.ac.uk/guides/graduation",

    # Campus and accommodation
    "https://www.kent.ac.uk/guides/accommodation",
    "https://www.kent.ac.uk/guides/canterbury",

    # IT and library
    "https://www.kent.ac.uk/guides/it-services",
    "https://www.kent.ac.uk/guides/passwords",
    "https://www.kent.ac.uk/guides/library",

    # Careers
    "https://www.kent.ac.uk/guides/careers",

    # International students
    "https://www.kent.ac.uk/guides/visas",

    # Contact
    "https://www.kent.ac.uk/guides/contact-us",
]
