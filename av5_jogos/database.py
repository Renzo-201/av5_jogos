import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base

load_dotenv()

def obter_engine():
    db_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if db_type == "mysql":
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "root")
        host = os.getenv("MYSQL_HOST", "localhost")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DATABASE", "biblioteca_jogos")
        
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        print(f"[CONEXÃO] Conectando ao MySQL no servidor '{host}'...")
    else:
        url = "sqlite:///biblioteca_jogos.db"
        print("[CONEXÃO] Conectando ao banco SQLite local ('biblioteca_jogos.db')...")

    return create_engine(url)

engine = obter_engine()
Base.metadata.create_all(engine)
