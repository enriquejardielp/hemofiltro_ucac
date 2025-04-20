#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 app.py &  # Arranca el servidor en background
sleep 2

# Detectar IP local automáticamente
IP=$(ipconfig getifaddr en0)

# Si no detecta en0, prueba en1 (depende del Mac)
if [ -z "$IP" ]; then
  IP=$(ipconfig getifaddr en1)
fi

# Abrir navegador con la IP real
open http://$IP:8000
