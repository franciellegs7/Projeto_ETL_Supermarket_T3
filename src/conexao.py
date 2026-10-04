# Conexão com o PostgreSQL, compartilhada pelos scripts do pipeline.

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine_supermarket = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('USUARIO')}:{os.getenv('SENHA')}"
    f"@{os.getenv('HOST')}:{os.getenv('PORTA')}"
    f"/{os.getenv('BANCO')}"
)