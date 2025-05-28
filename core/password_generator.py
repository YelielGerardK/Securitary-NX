import secrets
import string
from config.app_config import AMBIGUOUS_CHARS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
import os
from multiprocessing import Pool, cpu_count

def generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_symbols=True,
    exclude_ambiguous=False
):
    if not (MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH):
        raise ValueError(f"La longueur doit être comprise entre {MIN_PASSWORD_LENGTH} et {MAX_PASSWORD_LENGTH}.")
    alphabet = ''
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation
    if exclude_ambiguous:
        alphabet = ''.join(c for c in alphabet if c not in AMBIGUOUS_CHARS)
    if not alphabet:
        raise ValueError("Aucun type de caractère sélectionné.")
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (
            (not use_lowercase or any(c.islower() for c in password))
            and (not use_uppercase or any(c.isupper() for c in password))
            and (not use_digits or any(c.isdigit() for c in password))
            and (not use_symbols or any(c in string.punctuation for c in password))
        ):
            return password

def _generate_password_worker(args):
    return generate_password(**args)

def generate_multiple_passwords(
    count=1,
    **kwargs
):
    # Détection dynamique du nombre de cœurs, limitation à 4
    max_workers = min(4, cpu_count() or 1)
    if count == 1:
        return [generate_password(**kwargs)]
    # Prépare les arguments pour chaque tâche
    args_list = [kwargs.copy() for _ in range(count)]
    with Pool(processes=max_workers) as pool:
        results = pool.map(_generate_password_worker, args_list)
    return results 