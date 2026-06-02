import hashlib
import random
import string
from math import gcd

PRINTABLE_ASCII = "".join(chr(i) for i in range(32, 127))
ASCII_MOD = len(PRINTABLE_ASCII)
KEY_CHARSET = string.ascii_letters + string.digits


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def next_prime_after(n):
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def validate_printable_ascii(text):
    for char in text:
        if char not in PRINTABLE_ASCII:
            raise ValueError("Plaintext must contain only printable ASCII characters (32-126).")


def prompt_prime_number():
    while True:
        prime_number = int(input("Enter PRIME_NUMBER: "))
        if is_prime(prime_number):
            return prime_number
        print("Invalid input. PRIME_NUMBER must be prime.")


def prompt_threshold():
    while True:
        threshold = int(input("Enter THRESHOLD: "))
        if threshold > 0:
            return threshold
        print("Invalid input. THRESHOLD must be a positive integer.")


def build_seed(master_key):
    digest = hashlib.sha256(master_key.encode("utf-8")).hexdigest()
    return int(digest, 16)


def build_transposed_ascii_map(grp):
    rows = [PRINTABLE_ASCII[i:i + grp] for i in range(0, ASCII_MOD, grp)]
    ordered_chars = []

    for col in range(grp):
        for row in rows:
            if col < len(row):
                ordered_chars.append(row[col])

    value_map = {char: value for value, char in enumerate(ordered_chars)}
    reverse_map = {value: char for char, value in value_map.items()}
    return {
        "grp": grp,
        "value_map": value_map,
        "reverse_map": reverse_map,
    }


def get_map_bundle(char, upper_bundle, lower_bundle):
    if char.islower():
        return lower_bundle
    return upper_bundle


def generate_key(rng, length):
    return "".join(rng.choice(KEY_CHARSET) for _ in range(length))


def generate_distinct_key_pair(rng, length_one, length_two):
    first_key = generate_key(rng, length_one)
    second_key = generate_key(rng, length_two)

    while second_key == first_key:
        second_key = generate_key(rng, length_two)

    return first_key, second_key


def derive_affine_a(rng):
    affine_a = rng.randint(1, ASCII_MOD - 1)
    while gcd(affine_a, ASCII_MOD) != 1:
        affine_a = rng.randint(1, ASCII_MOD - 1)
    return affine_a


def derive_parameters(master_key):
    seed = build_seed(master_key)
    rng = random.Random(seed)

    upper_grp = rng.randint(2, 94)
    lower_grp = rng.randint(2, 94)
    affine_a = derive_affine_a(rng)
    affine_b = rng.randint(0, ASCII_MOD - 1)

    mysz_len_1 = rng.randint(3, 16)
    mysz_len_2 = rng.randint(3, 16)
    col_len_1 = rng.randint(3, 16)
    col_len_2 = rng.randint(3, 16)

    myszkowski_key_one, myszkowski_key_two = generate_distinct_key_pair(rng, mysz_len_1, mysz_len_2)
    columnar_key_one, columnar_key_two = generate_distinct_key_pair(rng, col_len_1, col_len_2)

    return {
        "seed": seed,
        "upper_grp": upper_grp,
        "lower_grp": lower_grp,
        "affine_a": affine_a,
        "affine_b": affine_b,
        "mysz_len_1": mysz_len_1,
        "mysz_len_2": mysz_len_2,
        "col_len_1": col_len_1,
        "col_len_2": col_len_2,
        "myszkowski_key_one": myszkowski_key_one,
        "myszkowski_key_two": myszkowski_key_two,
        "columnar_key_one": columnar_key_one,
        "columnar_key_two": columnar_key_two,
    }


def build_case_specific_indices(text):
    upper_index = 0
    lower_index = 0
    indices = []

    for char in text:
        if char.isupper():
            upper_index += 1
            indices.append(upper_index)
        elif char.islower():
            lower_index += 1
            indices.append(lower_index)
        else:
            indices.append(None)

    return indices


def get_repeated_letters(text):
    counts = {}
    for char in text:
        if char.isalpha():
            counts[char] = counts.get(char, 0) + 1
    return {char for char, count in counts.items() if count > 1}


def apply_repeat_transformation(text, upper_bundle, lower_bundle):
    repeated_letters = get_repeated_letters(text)
    case_indices = build_case_specific_indices(text)
    transformed_chars = []

    for position, char in enumerate(text):
        if char == " ":
            transformed_chars.append(char)
            continue

        bundle = get_map_bundle(char, upper_bundle, lower_bundle)
        value = bundle["value_map"][char]

        if char in repeated_letters and case_indices[position] is not None:
            product = case_indices[position] * value
            next_prime = next_prime_after(product)
            difference = next_prime - product
            value = (value + difference) % ASCII_MOD

        transformed_chars.append(bundle["reverse_map"][value])

    return "".join(transformed_chars)


def apply_affine_cipher(text, affine_a, affine_b, upper_bundle, lower_bundle):
    encrypted_chars = []

    for char in text:
        if char == " ":
            encrypted_chars.append(char)
            continue

        bundle = get_map_bundle(char, upper_bundle, lower_bundle)
        value = bundle["value_map"][char]
        affine_value = (affine_a * value + affine_b) % ASCII_MOD
        encrypted_chars.append(bundle["reverse_map"][affine_value])

    return "".join(encrypted_chars)


def build_row_matrix(text, columns):
    return [text[i:i + columns] for i in range(0, len(text), columns)]


def myszkowski_transposition(text, key):
    if not text:
        return text

    columns = len(key)
    rows = build_row_matrix(text, columns)
    grouped_columns = {}

    for index, char in enumerate(key):
        grouped_columns.setdefault(char, []).append(index)

    encrypted = []
    for key_char in sorted(grouped_columns):
        column_group = grouped_columns[key_char]
        if len(column_group) == 1:
            column = column_group[0]
            for row in rows:
                if column < len(row):
                    encrypted.append(row[column])
        else:
            for row in rows:
                for column in column_group:
                    if column < len(row):
                        encrypted.append(row[column])

    return "".join(encrypted)


def columnar_transposition(text, key):
    if not text:
        return text

    columns = len(key)
    rows = build_row_matrix(text, columns)
    ordered_columns = sorted(range(columns), key=lambda index: (key[index], index))
    encrypted = []

    for column in ordered_columns:
        for row in rows:
            if column < len(row):
                encrypted.append(row[column])

    return "".join(encrypted)


def apply_global_transposition_preserving_spaces(text, transposition_function, key):
    compact_text = "".join(char for char in text if char != " ")
    transposed_text = transposition_function(compact_text, key)
    rebuilt_text = []
    compact_index = 0

    for char in text:
        if char == " ":
            rebuilt_text.append(" ")
        else:
            rebuilt_text.append(transposed_text[compact_index])
            compact_index += 1

    return "".join(rebuilt_text)


def apply_double_myszkowski(text, key_one, key_two):
    first_pass = apply_global_transposition_preserving_spaces(text, myszkowski_transposition, key_one)
    return apply_global_transposition_preserving_spaces(first_pass, myszkowski_transposition, key_two)


def apply_double_columnar_per_word(text, key_one, key_two):
    transformed_words = []

    for word in text.split(" "):
        if word:
            first_pass = columnar_transposition(word, key_one)
            second_pass = columnar_transposition(first_pass, key_two)
            transformed_words.append(second_pass)
        else:
            transformed_words.append(word)

    return " ".join(transformed_words)


def random_ascii_pair():
    return "".join(random.choice(PRINTABLE_ASCII) for _ in range(2))


def pad_word(word):
    if not word:
        return word

    word_length = len(word)
    target_prime = next_prime_after(word_length)
    gap = (target_prime - word_length) // 2
    first_pos = word_length // 2
    pair_one = random_ascii_pair()
    pair_two = random_ascii_pair()

    padded_chars = list(word)
    padded_chars[first_pos:first_pos] = list(pair_one)

    second_pos = first_pos + len(pair_one) + gap + 1
    if second_pos > len(padded_chars):
        second_pos = len(padded_chars)

    padded_chars[second_pos:second_pos] = list(pair_two)
    return "".join(padded_chars)


def apply_padding_per_word(text):
    padded_words = [pad_word(word) if word else word for word in text.split(" ")]
    return " ".join(padded_words)


def apply_small_word_prepadding(text, threshold):
    processed_words = []

    for word in text.split(" "):
        if word and len(word) < threshold:
            processed_words.append(pad_word(word))
        else:
            processed_words.append(word)

    return " ".join(processed_words)


def shift_word_by_pivot(word, pivot_value):
    shifted_chars = []

    for char in word:
        normalized = ord(char) - 32
        shifted_chars.append(chr(((normalized + pivot_value) % ASCII_MOD) + 32))

    return "".join(shifted_chars)


def apply_pivot_chain(text, prime_number):
    transformed_words = []
    previous_index = None

    for word in text.split(" "):
        if not word:
            transformed_words.append(word)
            continue

        word_length = len(word)
        if previous_index is None:
            pivot_index = (prime_number - word_length) % word_length
        else:
            x_value = previous_index * word_length
            prime_value = next_prime_after(x_value)
            y_value = x_value + prime_value + previous_index
            pivot_index = y_value % word_length

        pivot_char = word[pivot_index]
        pivot_value = ord(pivot_char) - 32
        transformed_words.append(shift_word_by_pivot(word, pivot_value))
        previous_index = pivot_index

    return " ".join(transformed_words)


plaintext = input("Enter MASTER plaintext: ")
master_key = input("Enter MASTER_KEY: ")
prime_number = prompt_prime_number()
threshold = prompt_threshold()

validate_printable_ascii(plaintext)
parameters = derive_parameters(master_key)

upper_bundle = build_transposed_ascii_map(parameters["upper_grp"])
lower_bundle = build_transposed_ascii_map(parameters["lower_grp"])

pre_padded_text = apply_small_word_prepadding(plaintext, threshold)
pivot_text = apply_pivot_chain(pre_padded_text, prime_number)
repeat_text = apply_repeat_transformation(pivot_text, upper_bundle, lower_bundle)
affine_text = apply_affine_cipher(
    repeat_text,
    parameters["affine_a"],
    parameters["affine_b"],
    upper_bundle,
    lower_bundle,
)
myszkowski_text = apply_double_myszkowski(
    affine_text,
    parameters["myszkowski_key_one"],
    parameters["myszkowski_key_two"],
)
columnar_text = apply_double_columnar_per_word(
    myszkowski_text,
    parameters["columnar_key_one"],
    parameters["columnar_key_two"],
)
final_ciphertext = apply_padding_per_word(columnar_text)

'''print("Upper grp =", parameters["upper_grp"])
print("Lower grp =", parameters["lower_grp"])
print("Affine a =", parameters["affine_a"])
print("Affine b =", parameters["affine_b"])
print("Myszkowski key 1 length =", parameters["mysz_len_1"])
print("Myszkowski key 2 length =", parameters["mysz_len_2"])
print("Myszkowski key 1 =", parameters["myszkowski_key_one"])
print("Myszkowski key 2 =", parameters["myszkowski_key_two"])
print("Columnar key 1 length =", parameters["col_len_1"])
print("Columnar key 2 length =", parameters["col_len_2"])
print("Columnar key 1 =", parameters["columnar_key_one"])
print("Columnar key 2 =", parameters["columnar_key_two"])
print("PRIME_NUMBER =", prime_number)
print("THRESHOLD =", threshold)
'''
print("Cipher text:", final_ciphertext)
