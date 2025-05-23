"""
=========================================================
 Telegram Downloader Script - Interfaz Gráfica con Zenity
 Autor: drack_krack
 Fecha: 23/05/2025
=========================================================

📜 Derechos de Autor:
Este software está protegido por derechos de autor y ha sido creado por drack_krack. 
Se distribuye bajo la Licencia GNU GPL v3.

🔐 Política de Seguridad y Uso:
- Este script está diseñado exclusivamente para uso educativo, auditorías legales o gestión de contenidos propios.
- No está permitido usar este software para acceder, recopilar o distribuir información de canales o grupos sin autorización expresa de sus propietarios.
- El mal uso de este script puede violar políticas de privacidad, derechos de autor o leyes nacionales de protección de datos.
- El autor no se hace responsable del uso indebido de esta herramienta.

✅ Al usar este script, aceptas esta política y asumes la responsabilidad de su uso.
=========================================================
"""

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelPrivate, UserNotParticipant
import os
import subprocess
import re

# ← Inserta tus datos
API_ID = 123456  # Reemplaza con tu API ID
API_HASH = "abc123def456..."  # Reemplaza con tu API HASH

DOWNLOAD_PATH = "/home/osint/Desktop/TelegramPruebas"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def aceptar_politica():
    resultado = subprocess.run([
        "zenity", "--question",
        "--title=Política de Seguridad",
        "--text=Este script está destinado exclusivamente a fines educativos y legales.\n\n"
        "Cualquier uso no autorizado o con fines maliciosos es responsabilidad del usuario.\n\n"
        "¿Aceptas continuar bajo estos términos?"
    ])
    return resultado.returncode == 0

def zenity_input(texto):
    result = subprocess.run(["zenity", "--entry", "--title=Telegram Downloader", "--text", texto],
                            capture_output=True, text=True)
    return result.stdout.strip()

def zenity_error(texto):
    subprocess.run(["zenity", "--error", "--text", texto, "--title=Error"])

def zenity_info(texto):
    subprocess.run(["zenity", "--info", "--text", texto, "--title=Completado"])

def zenity_checklist(opciones):
    args = ["zenity", "--list", "--checklist", "--column=Seleccionar", "--column=Archivo",
            "--width=500", "--height=400", "--title=Selecciona archivos"]
    for nombre in opciones:
        args.extend(["FALSE", nombre])
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout.strip().split("|") if result.returncode == 0 else []

def zenity_listar_tipos():
    result = subprocess.run([
        "zenity", "--list", "--checklist", "--title=Selecciona qué quieres descargar",
        "--column=Seleccionar", "--column=Tipo",
        "TRUE", "Documentos",
        "TRUE", "Audios",
        "TRUE", "Videos",
        "TRUE", "Imágenes",
        "TRUE", "Mensajes de texto",
        "TRUE", "Miembros",
        "TRUE", "Enlaces"
    ], capture_output=True, text=True)
    return result.stdout.strip().split("|") if result.returncode == 0 else []

def main():
    if not aceptar_politica():
        zenity_error("Debes aceptar la política para continuar.")
        return

    app = Client("mi_sesion_completa", api_id=API_ID, api_hash=API_HASH)

    with app:
        chat_id = zenity_input("Ingresa el @usuario o ID del canal/grupo:")
        if not chat_id:
            zenity_error("No se ingresó canal/grupo.")
            return

        try:
            chat_info = app.get_chat(chat_id)
        except PeerIdInvalid:
            zenity_error("El ID o usuario proporcionado es inválido.")
            return
        except ChannelPrivate:
            zenity_error("No tienes acceso a este canal/grupo (es privado).")
            return
        except UserNotParticipant:
            zenity_error("No estás unido a este canal/grupo.")
            return
        except Exception as e:
            zenity_error(f"Error inesperado al acceder al chat: {e}")
            return

        tipos = zenity_listar_tipos()
        if not tipos:
            zenity_error("No se seleccionó ningún tipo.")
            return

        mensajes = app.get_chat_history(chat_id, limit=1000)
        archivos = []
        textos = []
        enlaces = []

        for msg in mensajes:
            if not isinstance(msg, Message):
                continue

            nombre = None
            tipo = None

            if msg.document and "Documentos" in tipos:
                nombre = msg.document.file_name
                tipo = "document"
            elif msg.audio and "Audios" in tipos:
                nombre = msg.audio.file_name
                tipo = "audio"
            elif msg.voice and "Audios" in tipos:
                nombre = f"nota_voz_{msg.id}.ogg"
                tipo = "voice"
            elif msg.video and "Videos" in tipos:
                nombre = msg.video.file_name or f"video_{msg.id}.mp4"
                tipo = "video"
            elif msg.photo and "Imágenes" in tipos:
                nombre = f"imagen_{msg.id}.jpg"
                tipo = "photo"
            elif msg.text:
                if "Mensajes de texto" in tipos:
                    textos.append(f"[{msg.date}] {msg.from_user.first_name if msg.from_user else 'Desconocido'}: {msg.text}")
                if "Enlaces" in tipos:
                    encontrados = re.findall(r'(https?://[^\s]+)', msg.text)
                    enlaces.extend(encontrados)

            if nombre and tipo:
                archivos.append((msg, nombre))

        if "Mensajes de texto" in tipos and textos:
            with open(os.path.join(DOWNLOAD_PATH, "mensajes.txt"), "w") as f:
                f.write("\n".join(textos))

        if "Enlaces" in tipos and enlaces:
            with open(os.path.join(DOWNLOAD_PATH, "enlaces.txt"), "w") as f:
                f.write("\n".join(enlaces))

        if "Miembros" in tipos:
            miembros = []
            try:
                for miembro in app.get_chat_members(chat_id):
                    nombre = miembro.user.first_name or ""
                    usuario = f"@{miembro.user.username}" if miembro.user.username else "Sin username"
                    miembros.append(f"{nombre} ({usuario})")
            except Exception as e:
                zenity_error(f"No se pudieron obtener los miembros: {e}")
            else:
                with open(os.path.join(DOWNLOAD_PATH, "miembros.txt"), "w") as f:
                    f.write("\n".join(miembros))

        if archivos:
            nombres = [nombre for _, nombre in archivos]
            seleccionados = zenity_checklist(nombres)
            for msg, nombre in archivos:
                if nombre in seleccionados:
                    app.download_media(msg, file_name=os.path.join(DOWNLOAD_PATH, nombre))

        zenity_info(f"¡Proceso completado!\nDescargas guardadas en:\n{DOWNLOAD_PATH}")

if __name__ == "__main__":
    main()
