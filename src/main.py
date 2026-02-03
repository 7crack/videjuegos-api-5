from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse, map_videojuego_to_response, map_create_to_videojuego
from data.db import init_db, get_session
from data.videojuegos_repository import VideojuegosRepository
from routers.api_videojuegos_router import router as api_videojuegos_router


import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(api_videojuegos_router)

# Ruta para la pagina principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para ver la lista de videojuegos
@app.get("/videojuegos", response_class=HTMLResponse)
async def ver_videojuegos(request: Request, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuegos = repo.get_all_videojuegos()
    return templates.TemplateResponse("videojuegos/videojuegos.html", {"request": request, "videojuegos": videojuegos})

# Ruta para agregar un nuevo videojuego
@app.get("/videojuegos/nuevo", response_class=HTMLResponse)
async def nuevo_videojuego_form(request: Request):

    """Formulario para añadir un videojuego nuevo"""
    return templates.TemplateResponse("videojuegos/videojuego_form.html", {
        "request": request,
        "videojuego": Videojuego()
    })

@app.post("/videojuegos/new", response_class=HTMLResponse)
async def crear_videojuego(request: Request, session: SessionDep):
    form_data = await request.form()
    titulo = form_data.get("titulo")
    fecha_lanzamiento = form_data.get("fecha_lanzamiento") or None
    genero = form_data.get("genero")

    videojuego_create = VideojuegoCreate(
        titulo=titulo,
        fecha_lanzamiento=fecha_lanzamiento,
        genero=genero
    )

    repo = VideojuegosRepository(session)
    videojuego = map_create_to_videojuego(videojuego_create)
    repo.create_videojuego(videojuego)

    return RedirectResponse(url="/videojuegos", status_code=303)

@app.get("/videojuegos/{videojuego_id}", response_class=HTMLResponse)
async def videojuego_por_id(videojuego_id: int, request: Request, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    videojuego_response = map_videojuego_to_response(videojuego_encontrado)
    return templates.TemplateResponse("videojuegos/videojuego_detalle.html", {"request": request, "videojuego": videojuego_response})

# Ruta para mostrar el formulario de edición
@app.get("/videojuegos/{videojuego_id}/editar", response_class=HTMLResponse)
async def editar_videojuego_form(request: Request, videojuego_id: int, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego = repo.get_videojuego(videojuego_id)
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    videojuego_response = map_videojuego_to_response(videojuego)
    return templates.TemplateResponse("videojuegos/videojuego_edit.html", {"request": request, "videojuego": videojuego_response})

# Ruta para actualizar un videojuego
@app.post("/videojuegos/{videojuego_id}/editar")
async def editar_videojuego(
    videojuego_id: int,
    session: SessionDep,
    titulo: str = Form(...),
    fecha_salida: str = Form(...),
    genero: str = Form(...)
):
    repo = VideojuegosRepository(session)
    videojuego = repo.get_videojuego(videojuego_id)
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    
    # Actualizar usando el método del repositorio
    videojuego_data = {
        "titulo": titulo,
        "fecha_lanzamiento": fecha_salida,
        "genero": genero
    }
    repo.update_videojuego(videojuego_id, videojuego_data)
    return RedirectResponse(url=f"/videojuegos/{videojuego_id}", status_code=303)

# Ruta para eliminar un videojuego
@app.delete("/videojuegos/{videojuego_id}")
async def eliminar_videojuego(videojuego_id: int, session: SessionDep):
    repo = VideojuegosRepository(session)
    videojuego = repo.get_videojuego(videojuego_id)
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    
    repo.delete_videojuego(videojuego_id)
    return {"message": "Videojuego eliminado correctamente"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
