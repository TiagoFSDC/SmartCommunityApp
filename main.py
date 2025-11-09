import os
from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Configuração do Banco de Dados (SQLAlchemy)
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, func
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin, ST_MakePoint

# Carrega variáveis de ambiente (ex: .env)
load_dotenv()

# Configuração da URL do Banco de Dados (lendo do ambiente)
DB_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "seu_usuario"),
    password=os.getenv("DB_PASSWORD", "sua_senha"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", 5432),
    database=os.getenv("DB_NAME", "seu_banco_de_dados"),
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Definição dos Modelos (Refletindo o Django) ---
# Precisamos redefinir o modelo aqui para que o SQLAlchemy saiba ler a tabela
# A tabela 'core_event' foi criada pelo Django.

class Event(Base):
    _tablename_ = 'core_event' # Nome exato da tabela criada pelo Django
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    event_date = Column(DateTime)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    # Não precisamos de todos os campos, apenas os que vamos retornar.

# --- Pydantic Schemas (para resposta da API) ---
class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    event_date: datetime
    # O FastAPI serializará o campo 'location' (do PostGIS)
    
    class Config:
        from_attributes = True # Permite mapear do modelo SQLAlchemy

# --- Inicialização do App FastAPI ---
app = FastAPI(
    title="Microserviço de Geoprocessamento",
    description="Serviço para encontrar eventos de mutirão próximos."
)

# --- Endpoint de Geoprocessamento ---
@app.get("/near_me/", response_model=List[EventOut])
def get_events_near_me(
    lat: float = Query(..., description="Latitude do usuário"),
    lon: float = Query(..., description="Longitude do usuário"),
    dist: float = Query(10.0, description="Raio da distância em quilômetros")
):
    """
    Retorna uma lista de eventos (Mutirões) próximos a um ponto (lat/lon)
    dentro de um raio de distância (em km).
    """
    db = SessionLocal()
    try:
        # Cria um ponto PostGIS a partir da lat/lon (SRID 4326)
        user_location_geom = ST_MakePoint(lon, lat).op('::')(Geometry(srid=4326))
        
        # Converte a distância de KM para Metros (PostGIS usa metros para SRID 4326)
        distance_meters = dist * 1000

        # Query do SQLAlchemy + GeoAlchemy2
        # ST_DWithin: Retorna 'true' se as geometrias estiverem dentro da distância especificada.
        query = db.query(Event).filter(
            ST_DWithin(
                Event.location,
                user_location_geom,
                distance_meters
            )
        )
        
        events = query.all()
        return events

    except Exception as e:
        print(f"Erro de banco de dados: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a consulta de geolocalização."
        )
    finally:
        db.close()

@app.get("/health/")
def health_check():
    """Verificação simples de saúde do serviço."""
    return {"status": "ok"}