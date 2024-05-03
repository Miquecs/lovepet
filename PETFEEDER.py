pet-feeder-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── db.py
├── requirements.txt
├── vercel.json
└── README.md

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, time
from .db import init_db, get_db
import sqlite3

app = FastAPI()

# Inicializa o banco de dados ao iniciar a API
init_db()

# Modelo para configuração de alarmes
class AlarmConfig(BaseModel):
    alarme1: time
    alarme2: time

# Modelo para status do alimentador
class FeederStatus(BaseModel):
    temperatura_ambiente: float
    vezes_aproximacao: int
    horario_atual: datetime

@app.get("/hora_atual")
async def get_hora_atual():
    return {"hora_atual": datetime.now()}

@app.get("/obter_alarmes")
async def get_alarme():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT alarme1, alarme2 FROM alarmes WHERE id = 1")
    result = cursor.fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Alarmes não encontrados")

    return {"alarme1": result[0], "alarme2": result[1]}

@app.post("/definir_alarmes")
async def set_alarme(alarme_config: AlarmConfig):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE alarmes SET alarme1 = ?, alarme2 = ? WHERE id = 1", (alarme_config.alarme1, alarme_config.alarme2))
    conn.commit()
    
    return {"status": "Alarmes atualizados"}

@app.post("/acionar_alimentador")
async def acionar_alimentador():
    # Simula o acionamento do alimentador
    return {"status": "Alimentador acionado"}

@app.post("/enviar_status")
async def receber_status(feeder_status: FeederStatus):
    # Recebe os dados do alimentador e armazena ou processa conforme necessário
    return {"status": "Status recebido"}

import sqlite3

# Inicializa o banco de dados com a tabela de alarmes
def init_db():
    conn = sqlite3.connect("alimentador.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS alarmes (id INTEGER PRIMARY KEY, alarme1 TIME, alarme2 TIME)"
    )
    # Insere valores padrão, se necessário
    cursor.execute("INSERT OR IGNORE INTO alarmes (id, alarme1, alarme2) VALUES (1, '06:00', '18:00')")
    conn.commit()
    conn.close()

# Obter uma conexão com o banco de dados
def get_db():
    return sqlite3.connect("alimentador.db")

{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}

fastapi
uvicorn
sqlite3

uvicorn app.main:app --reload
