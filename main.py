import random
import time

NUMBER_LENGTH = 4
SEPARATOR = "-" * 47


def print_intro() -> None:
    """Vypíše úvodní pozdrav a pravidla hry."""
    print("Hi there!")
    print(SEPARATOR)
    print(f"I've generated a random {NUMBER_LENGTH} digit number for you.")
    print("Let's play a bulls and cows game.")
    print(SEPARATOR)
    print("Enter a number:")
    print(SEPARATOR)


def generate_secret_number(length: int = NUMBER_LENGTH) -> str:
    """Vrátí náhodné číslo s unikátními číslicemi, které nezačíná nulou."""
    first_digit = random.choice("123456789")
    # zbývající číslice vybíráme z těch, které ještě nebyly použity
    remaining = [digit for digit in "0123456789" if digit != first_digit]
    return first_digit + "".join(random.sample(remaining, length - 1))


def validate_guess(guess: str, length: int = NUMBER_LENGTH) -> str | None:
    """
    Ověří tip hráče.

    Vrátí text chyby, nebo None, pokud je tip v pořádku.
    """
    if not guess.isdigit():
        return "Your guess must contain only digits."
    if len(guess) != length:
        return f"Your guess must have exactly {length} digits."
    if guess[0] == "0":
        return "Your guess must not start with zero."
    if len(set(guess)) != length:
        return "Your guess must not contain duplicate digits."
    return None


def get_valid_guess() -> str:
    """Opakovaně žádá hráče o tip, dokud nezadá platné číslo."""
    while True:
        guess = input(">>> ").strip()
        error = validate_guess(guess)
        if error is None:
            return guess
        print(error)
        print(SEPARATOR)


def evaluate_guess(secret: str, guess: str) -> tuple[int, int]:
    """Vrátí počet bulls a cows pro daný tip."""
    bulls = sum(1 for s, g in zip(secret, guess) if s == g)
    # společné číslice bez ohledu na pozici, bez těch, které už jsou bulls
    cows = len(set(secret) & set(guess)) - bulls
    return bulls, cows


def pluralize(count: int, word: str) -> str:
    """Vrátí počet se slovem v jednotném, nebo množném čísle."""
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def format_guesses(count: int) -> str:
    """Vrátí počet pokusů se správným tvarem slova guess/guesses."""
    return f"{count} guess" if count == 1 else f"{count} guesses"


def format_result(bulls: int, cows: int) -> str:
    """Vrátí naformátovaný výsledek tipu, např. '1 bull, 2 cows'."""
    return f"{pluralize(bulls, 'bull')}, {pluralize(cows, 'cow')}"


def print_congratulations(attempts: int, elapsed: float) -> None:
    """Vypíše gratulaci s počtem pokusů a dobou hry."""
    print("Correct, you've guessed the right number")
    print(f"in {format_guesses(attempts)}!")
    print(f"It took you {elapsed:.1f} seconds.")
    print(SEPARATOR)
    print("That's amazing!")


def play_game() -> int:
    """Odehraje jednu hru a vrátí počet pokusů."""
    secret = generate_secret_number()
    attempts = 0
    start_time = time.time()

    while True:
        guess = get_valid_guess()
        attempts += 1
        bulls, cows = evaluate_guess(secret, guess)
        if bulls == NUMBER_LENGTH:
            print_congratulations(attempts, time.time() - start_time)
            return attempts
        print(format_result(bulls, cows))
        print(SEPARATOR)


def ask_play_again() -> bool:
    """Zeptá se hráče, zda chce hrát znovu."""
    answer = input("Do you want to play again? (y/n): ").strip().lower()
    return answer == "y"


def print_statistics(results: list[int]) -> None:
    """Vypíše statistiky počtu pokusů ze všech odehraných her."""
    print(SEPARATOR)
    print(f"Games played: {len(results)}")
    print(f"Best game: {format_guesses(min(results))}")
    print(f"Average: {sum(results) / len(results):.1f} guesses")


def main() -> None:
    """Hlavní funkce programu, řídí opakování her a statistiky."""
    results = []
    while True:
        print_intro()
        results.append(play_game())
        if not ask_play_again():
            break
    print_statistics(results)


if __name__ == "__main__":
    main()
