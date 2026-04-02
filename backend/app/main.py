import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .db.database import Base, engine, ping_database
from .utils.logger import get_logger

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Fraud Detection API...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")
    except Exception as exc:
        logger.error(f"DB setup failed: {exc}")

    if ping_database():
        logger.info("Supabase connection: OK")
    else:
        logger.warning("Supabase connection: FAILED – check DATABASE_URL in .env")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Fraud Detection API",
    description="Real-time anomaly detection for financial transactions.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({ms:.1f}ms)")
    return response


@app.get("/", tags=["system"])
def root():
    return {"message": "Fraud Detection API is running.", "docs": "/docs"}


app.include_router(router)