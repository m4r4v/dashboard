import sys
import os
import re

try:
    from passlib.context import CryptContext
except ImportError:
    print("❌ Error: Librerías no encontradas.")
    sys.exit(1)

# Configuración
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ENV_PATH = "/workspace/.env"


def update_env_file(secret, hash_value):
    """
    Lee el archivo .env, actualiza o agrega las variables, y guarda los cambios.
    """
    if not os.path.exists(ENV_PATH):
        print(f"❌ Error: No encuentro el archivo en {ENV_PATH}")
        print(
            "   ¿Agregaste el volumen '- ./.env:/workspace/.env' en docker-compose.yml?"
        )
        return False

    with open(ENV_PATH, "r") as f:
        content = f.read()

    # Patrones Regex para encontrar las claves (incluso si tienen valores antiguos)
    # ^ comienza línea, .* cualquier contenido, $ fin de línea, flags=MULTILINE

    # 1. Actualizar AUTH_SECRET
    new_secret_line = f"AUTH_SECRET={secret}"
    if re.search(r"^AUTH_SECRET=.*$", content, re.MULTILINE):
        content = re.sub(
            r"^AUTH_SECRET=.*$", new_secret_line, content, flags=re.MULTILINE
        )
    else:
        content += f"\n{new_secret_line}"

    # 2. Actualizar ROOT_AUTH_HASH
    new_hash_line = f"ROOT_AUTH_HASH={hash_value}"
    if re.search(r"^ROOT_AUTH_HASH=.*$", content, re.MULTILINE):
        content = re.sub(
            r"^ROOT_AUTH_HASH=.*$", new_hash_line, content, flags=re.MULTILINE
        )
    else:
        content += f"\n{new_hash_line}"

    # Guardar cambios
    with open(ENV_PATH, "w") as f:
        f.write(content)

    return True


def generate():
    print("\n🤖 --- Autómata de Identidad (Write Mode) ---")

    email = input("1. Email del SuperAdmin: ").strip()
    password = input("2. Password del SuperAdmin: ").strip()
    secret = input("3. SYSTEM_SECRET (Pepper) [Enter para auto-generar]: ").strip()

    if not secret:
        import secrets

        secret = secrets.token_urlsafe(32)
        print(f"   ⚡ Secret generado: {secret}")

    # Generar Hash y Escapar para Docker ($ -> $$)
    raw_input = f"{email}{password}{secret}"
    auth_hash_raw = pwd_context.hash(raw_input)
    auth_hash_docker = auth_hash_raw.replace("$", "$$")

    # Escribir en el archivo
    print(f"\n📂 Accediendo a {ENV_PATH}...")
    success = update_env_file(secret, auth_hash_docker)

    if success:
        print("\n✅ ¡ARCHIVO .env ACTUALIZADO AUTOMÁTICAMENTE!")
        print("-" * 60)
        print("⚠️  IMPORTANTE: Para que los cambios surtan efecto en el servidor,")
        print("    debes reiniciar el contenedor:")
        print("    $ docker compose restart backend")
        print("-" * 60)


if __name__ == "__main__":
    generate()
