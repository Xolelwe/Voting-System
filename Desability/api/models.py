from django.db import models

"""
api_data.py

In-memory data storage for the API.
Replace these with Django models for persistence.
"""

# Candidates for voting
CANDIDATES = {
    1: 'Accessible Transport',
    2: 'Inclusive Education',
    3: 'Assistive Technology',
    4: 'Healthcare Accessibility',
    5: 'Digital Inclusion'
}

# Vote counters and voter lists
VOTE_COUNT = {cid: 0 for cid in CANDIDATES}
VOTERS = {cid: [] for cid in CANDIDATES}  # Stores usernames who voted for each candidate

# Survey configuration
SURVEY_QUESTIONS = [
    "Are schools accessible for students with disabilities?",
    "Do workplaces provide reasonable accommodations?",
    "Is public transport disability-friendly?",
    "Do you have access to assistive technology?",
    "Are healthcare facilities inclusive?",
    "Do you feel represented in policy-making?",
    "Are emergency services accessible?",
    "Do you have access to digital accessibility tools?",
    "Is voting easy for people with disabilities?",
    "Would you recommend improvements in accessibility laws?"
]
OPTIONS = ["Yes", "No", "Partially"]

# Survey responses storage
SURVEY_RESPONSES = []  # List of {user: username, responses: [answers]}

# Authentication tokens
VALID_TOKENS = {}  # Maps token -> username

# Chat history (optional)
CHAT_CONVERSATIONS = {}  # Maps user_id -> list of {question, answer, timestamp}
