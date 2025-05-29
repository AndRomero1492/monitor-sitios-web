import smtplib
from email.message import EmailMessage

def enviar_alerta(destinatario, url):
    remitente = "andress.romero.2004@gmail.com"  # <- cámbialo
    contraseña = "hyrm ycmn faod dajr"  # <- esta es la de 16 dígitos

    asunto = " ALERTA: Sitio caído"
    cuerpo = f"El sitio {url} está caído. Verifica lo antes posible."

    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo, charset='utf-8')


    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(mensaje)
        print(f" Alerta enviada a {destinatario} por caída de {url}")
    except Exception as e:
        print(f" Error al enviar correo: {e}")
