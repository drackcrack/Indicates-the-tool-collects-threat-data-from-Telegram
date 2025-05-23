
📜 Información del Script
Nombre: Telegram Downloader GUI

Autor: drack_krack

Licencia: GNU GPL v3

Propósito: Uso educativo y para investigación en Threat Intelligence.

✅ Seguridad y Legalidad
Incluye una política de uso que se presenta al iniciar el script mediante Zenity, la cual debe aceptarse para continuar.

Se prohíbe su uso con fines maliciosos.

Se aclara que el uso es bajo tu responsabilidad.

🔧 Manual de Instalación
Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/tu_usuario/telegram-downloader-gui.git
cd telegram-downloader-gui
Crea un entorno virtual:

bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate
Instala dependencias:

bash
Copiar
Editar
pip install pyrogram tgcrypto
sudo apt install zenity -y
Configura tu API:
Abre el script en un editor y reemplaza:

python
Copiar
Editar
API_ID = 123456
API_HASH = "abc123def456..."
con tus datos obtenidos desde https://my.telegram.org.

Ejecuta el script:

bash
Copiar
Editar
python telegram_downloader_gui.py
⚙️ ¿Cómo Funciona?
Al iniciar, muestra una ventana Zenity con la política de uso.

Pide el ID de canal o grupo (puede ser tipo @canal o -100xxxxxxxxxx).

Permite seleccionar qué tipo de datos descargar (documentos, audios, imágenes, texto, miembros, enlaces).

Analiza los últimos 1000 mensajes y organiza los datos:

Guarda mensajes y enlaces en .txt.

Muestra una lista gráfica para elegir qué archivos multimedia descargar.

Descarga los archivos seleccionados y guarda todo en una carpeta de destino definida.

