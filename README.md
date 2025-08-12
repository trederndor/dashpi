# dashpi
# Dashboard Servizi Flask

Questa è una semplice dashboard web in **Flask** per monitorare lo stato di vari servizi e aprire rapidamente i loro link.  
Mostra quali servizi sono attivi sul sistema, aggiornandosi automaticamente ogni secondo.

## **Funzionalità**
- **Login** con credenziali (attualmente hardcoded, da migliorare per produzione).
- **Verifica automatica** dello stato dei processi tramite `pgrep` o `systemctl`.
- **Aggiornamento in tempo reale** tramite JavaScript e fetch API.
- **Interfaccia responsive** in tema scuro.
- **Supporto SSL** (Let's Encrypt).

## **Requisiti di sistema**
- Linux con `systemd`
- Python 3.7+
- Certificati SSL validi (o modificare `app.run()` per usare HTTP)
- Pacchetti di sistema:
  - `curl`
  - `python3-pip`
  - `procps` (per `pgrep`)
  - `systemctl` (già presente nella maggior parte delle distro)
  - `flask`

## Quick Installation

```bash
curl -sSL https://raw.githubusercontent.com/trederndor/dashpi/refs/heads/main/fastinstall.sh | bash
```
## Manual Installation

```bash
git clone https://github.com/trederndor/dashpi.git ~/dashpi
cd ~/dashpi
chmod +x ./install.sh
sudo ./install.sh
python3 dashpi.py
```

mini service status dashboard with links
