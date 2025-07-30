# /var/www/yourusername_pythonanywhere_com_wsgi.py

import os
import sys

# Додаємо шлях до проекту
path = '/home/yourusername/my-fastapi-app'  # ЗМІНІТЬ USERNAME
if path not in sys.path:
    sys.path.insert(0, path)

# Активуємо віртуальне середовище
# Цей код потрібен, якщо ви не налаштували virtualenv в web tab
# activate_this = '/home/yourusername/my-fastapi-app/venv/bin/activate_this.py'
# exec(open(activate_this).read(), dict(__file__=activate_this))

# Імпортуємо FastAPI додаток
from main import app

# Обгортаємо в ASGI to WSGI адаптер
from asgiref.wsgi import WsgiToAsgi
application = WsgiToAsgi(app)