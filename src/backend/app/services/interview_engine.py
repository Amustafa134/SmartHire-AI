BASIC_QUESTIONS = {
    "AI Engineer": [
        "What is machine learning?",
        "Explain supervised vs unsupervised learning.",
    ],
}

def generate_question(role: str, difficulty: int = 1) -> str:
    # MVP = fixed bank (LLM later)
    return BASIC_QUESTIONS.get(role, ["Tell me about yourself"])[difficulty - 1]
