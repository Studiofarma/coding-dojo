def evaluate_mastermind(
    guess: list[str], combination: list[str]
) -> tuple[int, int]:
    correct = 0
    misplaced = 0
    for i, element in enumerate(guess):
        if element == combination[i]:
            correct += 1
            continue
        if element in combination:
            misplaced += 1
    return (correct, misplaced)
