def is_an_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_too_big(number):
    return number > 1000000


def is_too_small(number):
    return number <= 1


def decompose(number):
    primes = []
    for candidate in range(2, number + 1):
        while number % candidate == 0:
            primes.append(candidate)
            number /= candidate
    return primes