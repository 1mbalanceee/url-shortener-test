import string

ALPHABET = string.digits + string.ascii_letters
BASE = len(ALPHABET)

def encode_base62(num: int) -> str:
    """Encode an integer to a base62 string."""
    if num == 0:
        return ALPHABET[0]
    arr = []
    while num:
        num, rem = divmod(num, BASE)
        arr.append(ALPHABET[rem])
    return ''.join(reversed(arr))
