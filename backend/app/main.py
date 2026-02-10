from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings
from app.auth import verify_root_credentials, create_access_token

# ==============================================================================
# MODELOS DE DATOS (DTOs)
# ==============================================================================
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ==============================================================================
# GESTIÓN DE CICLO DE VIDA (LIFESPAN) - RF-06/07
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta al arrancar el servidor.
    Objetivo 5.2: Forzar la conexión a la BD para crear el archivo .db
    """
    print(f"🔄 INICIANDO MOTOR DE BASE DE DATOS: {settings.final_database_url}")
    
    # Crear motor (Engine)
    engine = create_async_engine(settings.final_database_url, echo=True)
    
    # Intento de conexión real (Smoke Test de Persistencia)
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ PERSISTENCIA VERIFICADA: Conexión exitosa (dashboard.db creado si es local)")
    except Exception as e:
        print(f"❌ ERROR CRÍTICO DE PERSISTENCIA: {e}")
    
    yield
    
    # Cierre (Shutdown)
    await engine.dispose()
    print("🛑 MOTOR DE BASE DE DATOS APAGADO")

# ==============================================================================
# ENTRYPOINT FASTAPI
# ==============================================================================
app = FastAPI(
    title="Dashboard Backend",
    version="1.2.0",
    lifespan=lifespan, # Vinculamos el ciclo de vida
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --- CONFIGURACIÓN CORS (RF-10) ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/health")
async def health_check():
    return {
        "status": "active",
        "system": "Stateless Dashboard",
        "database_mode": "PostgreSQL (Async)" if "postgres" in settings.final_database_url else "SQLite (Local)"
    }

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """
    Objetivo 5.3: Test de Seguridad (Root Secret + Pepper)
    """
    # 1. Validar Credenciales (Argon2id vs ROOT_SECRET)
    is_valid = verify_root_credentials(credentials.email, credentials.password)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Credenciales Inválidas (Root Check Failed)")
    
    # 2. Generar Token (Firma con ROOT_SECRET + SYSTEM_PEPPER)
    access_token = create_access_token(
        data={"sub": credentials.email, "role": "root"}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}