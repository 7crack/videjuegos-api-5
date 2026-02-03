from datetime import date
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Videojuego(SQLModel, table=True):
    id: int | None = Field(default = None, primary_key=True)
    titulo: str = Field(index=True, max_length=100)
    genero: str = Field(max_length=50)
    fecha_lanzamiento: date | None = Field(nullable=True)

# dto de Videojuego
class VideojuegoCreate(BaseModel):
    titulo: str
    genero: str
    fecha_lanzamiento: date | None = None

class VideojuegoUpdate(BaseModel):
    titulo: str | None = None
    genero: str | None = None
    fecha_lanzamiento: date | None = None

class VideojuegoResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    fecha_lanzamiento: date | None = None

# mapping entre modelo y dto
def map_videojuego_to_response(videojuego: Videojuego) -> VideojuegoResponse:
    return VideojuegoResponse(
        id=videojuego.id,
        titulo=videojuego.titulo,
        genero=videojuego.genero,
        fecha_lanzamiento=videojuego.fecha_lanzamiento
    )

def map_create_to_videojuego(videojuego_create: VideojuegoCreate) -> Videojuego:
    return Videojuego(
        titulo=videojuego_create.titulo,
        genero=videojuego_create.genero,
        fecha_lanzamiento=videojuego_create.fecha_lanzamiento
    )

def map_update_to_videojuego(videojuego: Videojuego, videojuego_update: VideojuegoUpdate) -> Videojuego:
    if videojuego_update.titulo is not None:
        videojuego.titulo = videojuego_update.titulo
    if videojuego_update.genero is not None:
        videojuego.genero = videojuego_update.genero
    if videojuego_update.fecha_lanzamiento is not None:
        videojuego.fecha_lanzamiento = videojuego_update.fecha_lanzamiento
    return videojuego