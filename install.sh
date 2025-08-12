
---

## **install.sh**
```bash
#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}==> Avvio installazione dipendenze per Dashboard Servizi...${NC}"

# Aggiornamento pacchetti
sudo apt update -y

# Installazione pacchetti di sistema
echo -e "${GREEN}==> Installo pacchetti di sistema...${NC}"
sudo apt install -y curl python3 python3-pip procps

# Creazione requirements.txt (se non esiste già)
if [ ! -f requirements.txt ]; then
  echo -e "${GREEN}==> Creo requirements.txt...${NC}"
  cat <<EOF > requirements.txt
Flask
EOF
fi

# Installazione pacchetti Python
echo -e "${GREEN}==> Installo dipendenze Python...${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo -e "${GREEN}✅ Installazione completata!${NC}"
echo "Puoi avviare l'app con:"
echo -e "${GREEN}python3 app.py${NC}"
