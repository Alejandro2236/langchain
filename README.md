# SmartTicket: Guía de Despliegue Académico (LangChain + FastAPI)

Este repositorio contiene la réplica funcional de la capa de backend y frontend de la mesa de ayuda utilizando Python. 

El sistema utiliza **FastAPI** para exponer los endpoints, **LangChain** con **Gemini 2.5-flash** como middleware cognitivo para el procesamiento estructurado del lenguaje natural (NLP), y conecta con una base de datos relacional.

---

## NOTA CRÍTICA SOBRE LA BASE DE DATOS LOCAL

El sistema cuenta con un módulo de persistencia en tiempo real (`database.py`). Al ser una entrega diseñada para ejecutarse sobre una infraestructura **local**, el programa **arrojará un error de conexión si no se tiene un servidor de PostgreSQL corriendo en su máquina** con las credenciales del archivo `.env`.

### Estructura Requerida de la Tabla (`DDL`)
Si desea probar la persistencia en su entorno local, asegúrese de tener creada la siguiente tabla en su base de datos:

```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    empleado VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    criticidad VARCHAR(20) NOT NULL,
    resumen VARCHAR(255) NOT NULL,
    solucion_infraestructura TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
