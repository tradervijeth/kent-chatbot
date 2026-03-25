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
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Google's free LLM - generates the chatbot responses
GENERATION_MODEL = "gemini-2.5-flash"

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
    "https://www.kent.ac.uk/courses/undergraduate/apply",
    "https://www.kent.ac.uk/courses/undergraduate/apply/how-to-apply",
    "https://www.kent.ac.uk/courses/undergraduate/apply/after-you-apply",
    "https://www.kent.ac.uk/courses/undergraduate/apply/application-timeline",
    "https://www.kent.ac.uk/clearing",
    "https://www.kent.ac.uk/courses/postgraduate/apply",
    "https://www.kent.ac.uk/courses/postgraduate",

    # Fees and funding
    "https://www.kent.ac.uk/courses/funding",
    "https://www.kent.ac.uk/courses/funding/undergraduate",
    "https://www.kent.ac.uk/courses/funding/postgraduate",

    # Student wellbeing and support
    "https://www.kent.ac.uk/student-support",
    "https://www.kent.ac.uk/student/wellbeing",
    "https://student.kent.ac.uk/support/wellbeing",
    "https://student.kent.ac.uk/support/mental-health",
    "https://student.kent.ac.uk/support/seeking-support-from-ssw",
    "https://student.kent.ac.uk/support/how-to-register-with-ssw",
    "https://student.kent.ac.uk/support/ssw-contact-us",
    "https://student.kent.ac.uk/support/getting-support-now",

    # Assessments and academic
    "https://www.kent.ac.uk/guides/extenuating-circumstances",
    "https://www.kent.ac.uk/guides/exams",
    "https://www.kent.ac.uk/guides/timetabling",
    "https://www.kent.ac.uk/guides/submitting-your-work",
    "https://www.kent.ac.uk/guides/using-moodle",
    "https://www.kent.ac.uk/guides/using-ai-in-your-studies",

    # Key dates
    "https://student.kent.ac.uk/studies/university-term-and-closure-dates",
    "https://www.kent.ac.uk/guides/term-dates",

    # Accommodation
    "https://www.kent.ac.uk/accommodation",
    "https://www.kent.ac.uk/accommodation/canterbury",

    # Library and IT
    "https://www.kent.ac.uk/library",
    "https://www.kent.ac.uk/library/opening-hours-and-support",
    "https://www.kent.ac.uk/welcome/library-it",
    "https://www.kent.ac.uk/it-services",

    # Careers
    "https://www.kent.ac.uk/guides/careers",
    "https://www.kent.ac.uk/careers",
    "https://www.kent.ac.uk/guides/study-plus",
    "https://www.kent.ac.uk/guides/employability-points",
    "https://www.kent.ac.uk/guides/jobshop",
    "https://www.kent.ac.uk/guides/life-after-uni",

    # International students
    "https://www.kent.ac.uk/international/how-to-apply",
    "https://www.kent.ac.uk/international/international-admission-deadlines",
    "https://www.kent.ac.uk/guides/immigration-and-visas",
    "https://www.kent.ac.uk/guides/international-students",

    # Student support hub
    "https://student.kent.ac.uk",
    "https://student.kent.ac.uk/support",
    "https://student.kent.ac.uk/support/engagement",
    "https://student.kent.ac.uk/support/administration",
    "https://student.kent.ac.uk/support/nexus",
    "https://student.kent.ac.uk/studies",
    "https://reportandsupport.kent.ac.uk/",

    # Financial and cost of living
    "https://www.kent.ac.uk/guides/finance-and-funding",
    "https://www.kent.ac.uk/guides/cost-of-living-support",

    # Disability and neurodiversity
    "https://student.kent.ac.uk/support/disability-and-neurodiversity",
    "https://www.kent.ac.uk/guides/disability-and-neurodiversity",

    # Safety
    "https://student.kent.ac.uk/support/safety",
    "https://www.kent.ac.uk/guides/safety",

    # Support for all groups
    "https://www.kent.ac.uk/guides/care-experienced-students",
    "https://www.kent.ac.uk/guides/long-term-health-conditions",
    "https://www.kent.ac.uk/guides/mature-commuting-and-part-time-students",
    "https://www.kent.ac.uk/guides/carers",
    "https://www.kent.ac.uk/guides/pregnant-students-and-parents",
    "https://www.kent.ac.uk/guides/estranged-students",

    # Student admin tools
    "https://www.kent.ac.uk/guides/student-status-letter",
    "https://www.kent.ac.uk/guides/kentvision",
    "https://www.kent.ac.uk/guides/presto",
    "https://www.kent.ac.uk/guides/progress-profiles",
    "https://www.kent.ac.uk/guides/student-conduct-and-complaints",

    # Campus facilities
    "https://www.kent.ac.uk/catering",
    "https://www.kent.ac.uk/sport",
    "https://www.kent.ac.uk/student-support/health",
    "https://www.kent.ac.uk/estates/parking",
    "https://www.kent.ac.uk/guides",
]
