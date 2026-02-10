# Script de utilidad para generar ROOT_SECRET
from argon2.low_level import hash_secret_raw, Type

# DATOS DEL .ENV (Deben coincidir EXACTAMENTE)
PEPPER = "m4r4v-pepper-local-dev-secure-v1"
EMAIL = "admin@dashboard.com"
PASS = "admin"

payload = f"{EMAIL}{PASS}".encode()
salt = PEPPER.encode()[:16].ljust(16, b"0")

hashed = hash_secret_raw(
    secret=payload,
    salt=salt,
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=64,
    type=Type.ID,
)

print("\n=== TU NUEVO ROOT_SECRET ===")
print(hashed.hex())
print("============================\n")
