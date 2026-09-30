from pathlib import Path
import os
from dotenv import load_dotenv


PASTA_RAIZ = Path(__file__).resolve().parent

PASTA_DADOS = PASTA_RAIZ / "data"
PASTA_ORIGINAL = PASTA_DADOS / "original"
PASTA_RAW = PASTA_DADOS / "raw"
PASTA_STAGING = PASTA_DADOS / "staging"
PASTA_PROCESSED = PASTA_DADOS / "processed"


load_dotenv(PASTA_RAIZ / ".env")


POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DATABASE", "transparencia"),
}