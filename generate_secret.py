"""Script de utilidad para generar ROOT_SECRET (y credenciales demo si no se
proveen). [CORREGIDO] La versión anterior tenía PEPPER/EMAIL/PASS hardcodeados
en el script committeado, contradiciendo RNF-01 ("Cero Secretos en Código").
Ahora se leen de variables de entorno, con fallback aleatorio si no existen.
"""

import os
import secrets

from argon2.low_level import Type, hash_secret_raw

EMAIL = os.environ.get("DEMO_EMAIL") or "admin@dashboard.com"
PASSWORD = os.environ.get("DEMO_PASSWORD") or secrets.token_urlsafe(12)
PEPPER = os.environ.get("SYSTEM_PEPPER") or secrets.token_urlsafe(32)

payload = f"{EMAIL}{PASSWORD}".encode()
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

print("\n=== CREDENCIALES GENERADAS ===")
print(f"DEMO_EMAIL={EMAIL}")
print(f"DEMO_PASSWORD={PASSWORD}")
print(f"SYSTEM_PEPPER={PEPPER}")
print(f"ROOT_SECRET={hashed.hex()}")
print("===============================\n")
