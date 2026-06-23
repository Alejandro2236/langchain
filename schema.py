from pydantic import BaseModel, Field
from typing import Literal

class FormularioIncidente(BaseModel):
    empleado: str
    correo: str
    departamento: str
    descripcion: str

class TicketAnalizado(BaseModel):
    categoria: Literal[
        "Infraestructura y Servidores",
        "Software Corporativo/ERP",
        "Redes y Conectividad",
        "Hardware de Oficina",
        "No Clasificable / Inválido"
    ] = Field(description="Categoría tecnológica del incidente.")
    
    criticidad: Literal["Alta", "Media", "Baja", "N/A"] = Field(
        description="Impacto operativo del caso. N/A si es inválido."
    )
    resumen: str = Field(description="Resumen técnico ejecutivo de máximo 15 palabras.")
    solucion_infraestructura: str = Field(
        description="Pasos iniciales de mitigación o mensaje de rechazo si es inválido."
    )