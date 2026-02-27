from fastapi import FastAPI

from database import engine
from models import Base
from controllers.transacoes_controller import router as transacoes_router
from controllers.test_whatsapp_controller import router as test_whatsapp_router



app = FastAPI(
    title="API Financeira",
    description="Bot financeiro estilo WhatsApp",
    version="1.0.0"
)

# Cria as tabelas no banco SQLite
Base.metadata.create_all(bind=engine)

# Registra os controllers
app.include_router(transacoes_router)
app.include_router(test_whatsapp_router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "API rodando com sucesso 🚀"
    }
