from typing import Optional
from pydantic import BaseModel,EmailStr

class Persona(BaseModel):
    id: Optional[int] = None
    nombre: str
    edad: int
    email: EmailStr

#API
from fastapi import FastAPI, HTTPException

app = FastAPI()

#Base de datos simulada con un array
persona_db = []

# crear persona

@app.post("/personas/", response_model=Persona)
def crear_persona(persona:Persona):
    persona.id = len(persona_db)+1
    persona_db.append(persona)
    return persona

# ver persona por id
@app.get("/personas/{persona_id}", response_model=Persona)
def obtener_persona(persona_id: int):
    for persona in persona_db:
        if persona.id == persona_id:
            return persona
        raise HTTPException(status_code=404, detail="Persona no encontrada")

#Listar personas
@app.get("/personas/",response_model=list[Persona])
def listar_persona():
    return persona_db

# Actualizar
@app.put("/personas/{persona_id}",response_model=Persona)
def actualizar_persona(persona_id: int,persona_actualizada: Persona):
    for index, persona in enumerate(persona_db):
        if persona.id == persona_id:
            persona_db[index]= persona_actualizada
            persona_actualizada.id=persona_id
            return persona_actualizada
    raise HTTPException(status_code=404,detail="Persona no encontrada")

#Eliminar
@app.delete("/personas/{persona_id}",response_model=dict)
def eliminar_persona(persona_id: int):
    for index, persona in enumerate(persona_db):
        if persona.id == persona_id:
            del persona_db[index]
            return{"detail": "Persona Eliminada"}
    raise HTTPException(status_code=404, detail="Persona no encontrada")

