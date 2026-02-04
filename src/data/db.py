from dotenv import load_dotenv
import os
from sqlmodel import create_engine, SQLModel, Session, select
from models.videojuego import Videojuego

load_dotenv()

# Priorizar DATABASE_URL si existe (para Render)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Construir desde variables individuales (para desarrollo local)
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_server: str = os.getenv("DB_SERVER", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "videojuegosdb")
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    print("⚠️  Usando configuración local de base de datos")
else:
    print("✅ Usando DATABASE_URL de variables de entorno")

print(f"🔗 DATABASE_URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        statement = select(Videojuego)
        existing = session.exec(statement).first()
        
        if not existing:
            videojuegos = [
                Videojuego(titulo="The Legend of Zelda: Breath of the Wild", genero="Action-adventure", fecha_lanzamiento="2017-03-03"),
                Videojuego(titulo="God of War", genero="Action-adventure", fecha_lanzamiento="2018-04-20"),
                Videojuego(titulo="Red Dead Redemption 2", genero="Action-adventure", fecha_lanzamiento="2018-10-26"),
                Videojuego(titulo="The Witcher 3: Wild Hunt", genero="Action RPG", fecha_lanzamiento="2015-05-19"),
                Videojuego(titulo="Minecraft", genero="Sandbox, Survival", fecha_lanzamiento="2011-11-18"),
            ]
            for v in videojuegos:
                session.add(v)
            session.commit()
            print("✅ Datos iniciales insertados")
        else:
            print("✅ Base de datos ya contiene datos")