from typing import Union, Optional
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import psycopg2

from fastapi import FastAPI
app = FastAPI()

POSTGRE_KEY = os.getenv('POSTGRE_KEY')

# Para usar Javascript
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

class Usuario(BaseModel):
  id: Optional[int] = Field(default=None, primary_key=True)
  nameinfo: str
  passworda: str
  email: str


def conectar_bd():
    # Agregar siempre ?sslmode=require al final
    conexion = psycopg2.connect(
        POSTGRE_KEY
    )
    return conexion

def cerrar_bd(conexion):
    conexion.close()

# llamamos la url 
@app.get('/alldata', tags=['Usuario'])
def salida():
    try:
        #Creamos un result vacio
        result = []
        # arrancamos con la conexión a la BD
        conexion = conectar_bd()
        cursor = conexion.cursor()
        # insertamos el sql
        cursor.execute("SELECT * FROM usuario;")
        usuarios = cursor.fetchall() # Datos
        # printing -> reservado para enviar
        conexion.commit()

        # este codigo es creado por nosotros y nos trae las filas y las columnas y las mezcla
        if cursor.description:
            colnames = [desc[0] for desc in cursor.description] #  Nombres de las columnas
            result = [dict(zip(colnames, row)) for row in usuarios]  
        # cerramos la conexión 
        cerrar_bd(conexion)

        # retornamos el servicio
        return result
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return HTMLResponse(status_code=400, content={"mensaje": "Error al obtener los usuarios"})


@app.post('/save', tags=['Usuario'])
def crear(usuario: Usuario):
    try:

        # arrancamos con la conexión a la BD
        conexion = conectar_bd()
        cursor = conexion.cursor()
        # insertamos el sql
        cursor.execute("INSERT INTO usuario (nameinfo, passworda, email) VALUES (%s, %s, %s) RETURNING *",(usuario.nameinfo, usuario.passworda, usuario.email))
        # printing -> reservado para enviar
        conexion.commit()
        
        usuarioInfo = cursor.fetchone() # Datos
        
        # cierre de la conexión
        cerrar_bd(conexion)
        
        # se envia ese dato que obtuvimos y se crea la respuesta
        respuesta = {
            "mensaje": "Usuario creado con éxito",
            "id": usuarioInfo[0]
        }
        return respuesta

    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return HTMLResponse(status_code=500, content={"mensaje": "Error al crear usuario"})

@app.get("/")
def read_root():
    return {"Hello": "World", "inf": MY_ENV_VAR}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}