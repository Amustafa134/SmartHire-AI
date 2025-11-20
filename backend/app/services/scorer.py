def score_answer(answer: str) -> int:
    # MVP simple scoring
    if len(answer.split()) > 20:
        return 5
    elif len(answer.split()) > 10:
        return 3
    return 1
