from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse, map_videojuego_to_response, map_create_to_videojuego

from data.videojuegos_repository import VideojuegosRepository
from data.db import init_db, get_session

router = APIRouter(prefix="/api/videojuegos", tags=["videojuegos"])

SessionDep = Annotated[Session, Depends(get_session)]

# Rutas de la API para gestionar videojuegos

@router.get("/", response_model=list[VideojuegoResponse])
async def lista_videojuegos(session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuegos = repo.get_all_videojuegos()
    return [map_videojuego_to_response(videojuego) for videojuego in videojuegos]

@router.post("/", response_model=VideojuegoResponse)
async def nuevo_videojuego(videojuego_create: VideojuegoCreate, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego = map_create_to_videojuego(videojuego_create)
    videojuego_creado = repo.create_videojuego(videojuego)
    return map_videojuego_to_response(videojuego_creado)

@router.get("/{videojuego_id}", response_model=VideojuegoResponse)
async def videojuego_por_id(videojuego_id: int, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return map_videojuego_to_response(videojuego_encontrado)

@router.delete("/{videojuego_id}", status_code=204)
async def borrar_videojuego(videojuego_id: int, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, details="Videojuego no encontrado")
    repo.delete_videojuego(videojuego_id)
    return None

@router.patch("/{videojuego_id}", response_model=VideojuegoResponse)
async def cambia_videojuego(videojuego_id: int, videojuego: Videojuego, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, details="Videojuego no encontrado")
    videojuego_data = videojuego.model_dump(exclude_unset=True)
    videojuego_encontrado.sqlmodel_update(videojuego_data)
    repo.update_videojuego(videojuego_encontrado.id, videojuego_data)
    return map_videojuego_to_response(videojuego_encontrado)

@router.put("/", response_model=VideojuegoResponse)
async def cambia_videojuego(videojuego: Videojuego, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego.id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, details="Videojuego no encontrado")
    videojuego_data = videojuego.model_dump()
    videojuego_encontrado.sqlmodel_update(videojuego_data)
    repo.update_videojuego(videojuego_encontrado.id, videojuego_data)
    return map_videojuego_to_response(videojuego_encontrado)
