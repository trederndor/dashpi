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
# Aggiunge al crontab una riga commentata per avviare lo script all’avvio (se non già presente)
CRON_MARK="# Avvia dashpi.py all'avvio del server"
CRON_CMD="@reboot python3 /home/mosca/dashpi/dashpi.py"

# Aggiunge al crontab dell'utente corrente una riga commentata per avviare lo script all’avvio (se non già presente)
CRON_MARK="# Avvia dashpi.py all'avvio del server"
CRON_CMD="@reboot python3 /home/mosca/dashpi/dashpi.py"

# Ottiene il crontab esistente o crea uno vuoto se non esiste
crontab -l 2>/dev/null > /tmp/current_cron || true

# Controlla se la riga commentata esiste già
if ! grep -Fq "$CRON_MARK" /tmp/current_cron; then
    {
      cat /tmp/current_cron
      echo ""
      echo "$CRON_MARK"
      echo "# $CRON_CMD"
    } | crontab -
    echo "📝 Righe commentate per l’avvio automatico aggiunte al crontab dell’utente corrente."
else
    echo "ℹ️ Righe commentate già presenti nel crontab dell’utente corrente."
fi

# Pulisce
rm /tmp/current_cron


echo "✅ Tutto installato. Puoi ora avviare lo script Python!"
