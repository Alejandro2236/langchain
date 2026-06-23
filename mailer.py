import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from schema import FormularioIncidente, TicketAnalizado

load_dotenv()

def enviar_correo_alta_prioridad(form: FormularioIncidente, ticket: TicketAnalizado):
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_pass:
        print("[Mailer] Alerta simulada (Faltan variables SMTP en .env):")
        print(f"NOTIFICACIÓN: Incidente CRÍTICO en {form.departamento}. Resumen: {ticket.resumen}")
        return

    asunto = f"EMERGENCIA TI: Caso Crítico Detectado en {form.departamento}"
    cuerpo = f"""
    Hola equipo de Soporte Nivel 3,
    
    La IA ha clasificado un nuevo incidente de criticidad ALTA.
    
    Detalles del Reporte:
    - Empleado: {form.empleado} ({form.correo})
    - Departamento: {form.departamento}
    - Resumen Ejecutivo: {ticket.resumen}
    
    Solución Inicial Sugerida:
    {ticket.solucion_infraestructura}
    
    Por favor, ingresar a la base de datos PostgreSQL para auditar el caso.
    """
    
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = smtp_user
    msg['To'] = smtp_user

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [smtp_user], msg.as_string())
        server.quit()
        print("[Mailer] Correo de alerta enviado al equipo de ingeniería.")
    except Exception as e:
        print(f"[Mailer Error]: No se pudo enviar el correo: {e}")