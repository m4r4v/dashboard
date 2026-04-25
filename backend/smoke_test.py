import httpx

BASE_URL = "http://localhost:8000/api"
ROOT_EMAIL = "admin@dashboard.com" 
ROOT_PASS = "admin"

def run_smoke_test():
    print("🚀 SMOKE TEST DE EMERGENCIA\n" + "="*40)
    with httpx.Client() as client:
        # 1. Login con manejo de errores
        res = client.post(f"{BASE_URL}/auth/login", json={"email": ROOT_EMAIL, "password": ROOT_PASS})
        if res.status_code != 200:
            print(f"❌ LOGIN FALLIDO ({res.status_code}): {res.text}")
            return
        
        token = res.json().get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login exitoso.")

        # 2. Provocar Errores
        client.get(f"{BASE_URL}/node/no-existe")
        client.post(f"{BASE_URL}/auth/login", json={"email": "hacker", "password": "1"})

        # 3. Verificar Métricas
        res = client.get(f"{BASE_URL}/node/metrics", headers=headers)
        print("\n📊 MÉTRICAS ACTUALES:")
        print(res.text)
        
        if "http_errors_total" in res.text:
            print("\n✅ TELEMETRÍA CONFIRMADA.")
        else:
            print("\n❌ TELEMETRÍA NO ENCONTRADA.")

if __name__ == "__main__":
    run_smoke_test()