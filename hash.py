from passlib.handlers.bcrypt import bcrypt

from Variables import ValueStorage


def verify_hash_againts_password(hash: str, password: str) -> bool:
    return bcrypt.verify(password, hash)


def get_hash_for_password(password: str, rounds: int = 8) -> str:  # TODO dev 2, prod 8 - 12
    return bcrypt.using(ident="2b", rounds=rounds).hash(password)

print(get_hash_for_password("!Qwertyuiop123!", 10))
print(verify_hash_againts_password("$2b$10$d4x0HFMbr8KXMi2LNcwj3.Z.VC80OF/ayHjdub8cFR2O9DEEFHN5m", "!Qwertyuiop123!"))

# 00003254200015144012
print(get_hash_for_password("22222222222", 10))
print(verify_hash_againts_password("$2b$10$nHJm2Q7V2UWVtHS9R9Vet.1vN5lrYIyQXczyR11x.ZCDayAT6Vov.", "1976-12-22"))


verify_hash_againts_password = ValueStorage.verify_hash_againts_password