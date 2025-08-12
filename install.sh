#!/bin/bash
set -e

echo "=== 🛠 INSTALLAZIONE DIPENDENZE ==="

# Installa curl se non presente
if ! command -v curl &> /dev/null; then
    echo "⚠️ curl non trovato. Installazione in corso..."
    sudo apt-get update
    sudo apt-get install -y curl
else
    echo "✅ curl già installato"
fi
# Installa unzip se non presente
if ! command -v unzip &> /dev/null; then
    echo "⚠️ unzip non trovato. Installazione in corso..."
    sudo apt-get install -y unzip
else
    echo "✅ unzip già installato"
fi

# Controlla Python 3
if command -v python3 &> /dev/null; then
    echo "✅ Python3 già installato"
else
    echo "⚠️ Python3 non trovato. Installazione in corso..."
    sudo apt update
    sudo apt install -y python3
fi

# Controlla pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 già installato"
else
    echo "⚠️ pip3 non trovato. Installazione in corso..."
    sudo apt install -y python3-pip
fi

# Installa dipendenze Python
echo "📦 Installazione dipendenze da requirements.txt"
pip install --break-system-packages --upgrade pip
pip install --break-system-packages -r requirements.txt
# Estrazione static.zip
if [ -f "static.zip" ]; then
    echo "📂 Estrazione static.zip"
    if command -v unzip &> /dev/null; then
        unzip -o static.zip
        echo "✅ static.zip estratto con unzip"
    else
        echo "❌ unzip non disponibile. Impossibile estrarre static.zip"
        exit 1
    fi
else
    echo "⚠️ static.zip non trovato, niente da estrarre"
fi
crontab -l > /tmp/current_cron 2>/dev/null || true
grep -Fq "# Avvia dashpi.py all'avvio del server" /tmp/current_cron && echo "Trovato" || echo "Non trovato"

# Se non trovato:
{
  cat /tmp/current_cron
  echo ""
  echo "# Avvia dashpi.py all'avvio del server"
  echo "# @reboot python3 /home/mosca/dashpi/dashpi.py"
} | crontab -


echo "✅ Tutto installato. Puoi ora avviare lo script Python!"
