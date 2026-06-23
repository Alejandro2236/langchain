import os
import psycopg2
from dotenv import load_dotenv
from schema import FormularioIncidente, TicketAnalizado

load_dotenv()

def guardar_en_postgres(form: FormularioIncidente, ticket: TicketAnalizado):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        
        query = """
            INSERT INTO tickets (empleado, correo, departamento, categoria, criticidad, resumen, solucion_infraestructura)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        valores = (
            form.empleado,
            form.correo,
            form.departamento,
            ticket.categoria,
            ticket.criticidad,
            ticket.resumen,
            ticket.solucion_infraestructura
        )
        
        cursor.execute(query, valores)
        conn.commit()
        print("[Postgres] Registro insertado exitosamente.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Postgres Error]: {e}")