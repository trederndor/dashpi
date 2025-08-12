from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'b3f8c3e1d52b4a1a9e2cf17248f5d9c495e689177048b94cf1f35d2bb6a3c9f5'  # Cambiala con una segreta vera!

SERVIZI = {
    "AdGuard":    {"proc": "AdGuardHome", "link": "https://yourdomain:2020/", "icon": "/static/adguard.svg"},
    "Apache":     {"proc": "apache2",     "link": "http://yourdomain/", "icon": "/static/apache.svg"},
#    "Minecraft Server":  {"proc": "paper.jar",   "link": "", "icon": "/static/minecraft.svg"},
#    "Mysterium":  {"proc": "myst",        "link": "http://192.168.1.24:4449/#/dashboard", "icon": "/static/mysterium.svg"},
    "NoIP2":      {"proc": "noip2",       "link": "https://www.noip.com/", "icon": "/static/noip.png"},
#    "Python":     {"proc": "python",      "link": "", "icon": "/static/python.svg"},
    "Webmin":     {"proc": "webmin",      "link": "https://yourdomain:10000/sysinfo.cgi?xnavigation=1", "icon": "/static/webmin.svg"},
    "Pi-Monitor": {"proc": "python3 /home/mosca/programmipython/Pi-Monitor/app.py", "link": "http://192.168.1.24:8003/", "icon": "/static/pi-monitor.ico"},
    "Trascrittore": {"proc": "bot/trascrittore.py", "link": "", "icon": "/static/python.svg"},
    "Telegram Bot": {"proc": "botriavvio.py", "link": "", "icon": "/static/python.svg"},
    "Wireguard":      {"proc": "wg-quick@wg0", "link": "http://192.168.1.24:5000/", "icon": "/static/wireguard.svg"},
    "JellyFin":      {"proc": "jellyfin", "link": "https://yourdomain:8920/web/#/login.html", "icon": "/static/jellyfin.svg"},
    "Network speed monitor":      {"proc": "/usr/bin/python speed.py", "link": "http://192.168.1.24:5050/", "icon": ""},
}


MANUAL_PYTHON_APPS = {
    #"Cine Vault Pro": {"icon": "/static/CineVault-pittogramma-giallo.svg", "link": "https://yourdomain:7771/"},
    #"Cine Vault":     {"icon": "/static/CineVault-pittogramma-giallo.svg", "link": "https://yourdomain:5000/"},
}

# Credenziali login hardcoded (da sostituire o migliorare)
USER_CREDENTIALS = {
    "user": "Password!"
}

import subprocess

def check_service(procname):
    try:
        if procname.startswith("wg-quick@"):
            result = subprocess.run(["systemctl", "is-active", procname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            return result.stdout.strip() == b'active'
        else:
            result = subprocess.run(['pgrep', '-f', procname], stdout=subprocess.PIPE)
            return result.returncode == 0
    except Exception:
        return False

from flask import jsonify

@app.route('/stati_servizi')
def stati_servizi():
    if not session.get('logged_in'):
        return jsonify({}), 403

    stati = {nome: check_service(info['proc']) for nome, info in SERVIZI.items()}
    return jsonify(stati)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if USER_CREDENTIALS.get(username) == password:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Credenziali errate, riprova."
            return render_template_string(LOGIN_TEMPLATE, error=error)
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    stati = {}
    attivi = 0
    totali = len(SERVIZI)

    for nome, info in sorted(SERVIZI.items()):
        attivo = check_service(info['proc'])
        stati[nome] = attivo
        if attivo:
            attivi += 1

    python_apps = MANUAL_PYTHON_APPS

    return render_template_string(DASHBOARD_TEMPLATE,
                              stati=stati,
                              attivi=attivi,
                              totali=totali,
                              python_apps=python_apps,
                              manual_apps=MANUAL_PYTHON_APPS,
                              servizi=SERVIZI)


LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
<link rel="icon" type="image/svg+xml" href="/static/dashboard.svg">
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Login</title>
  <style>
    body {
      background: #121212;
      font-family: Arial, sans-serif;
      display: flex;
      height: 100vh;
      justify-content: center;
      align-items: center;
      margin: 0;
    }
    .login-box {
      background: #1e1e1e;
      padding: 30px 40px;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
      width: 320px;
      text-align: center;
    }
    h2 {
      margin-bottom: 20px;
      color: #ffffff;
    }
    input[type=text], input[type=password] {
      width: 100%;
      padding: 10px 12px;
      margin: 10px 0 20px 0;
      border: 1px solid #ccc;
      border-radius: 5px;
      box-sizing: border-box;
      font-size: 1em;
    }
    button {
      width: 100%;
      background-color: #3b82f6;
      color: white;
      border: none;
      padding: 12px;
      font-size: 1em;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    button:hover {
      background-color: #2563eb;
    }
    .error {
      color: #f87171;
      margin-bottom: 15px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>Login Dashboard</h2>
    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}
    <form method="POST" action="{{ url_for('login') }}">
      <input type="text" name="username" placeholder="Username" required autofocus />
      <input type="password" name="password" placeholder="Password" required />
      <button type="submit">Accedi</button>
    </form>
  </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
<link rel="icon" type="image/svg+xml" href="/static/dashboard.svg">
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dashboard Servizi</title>
  <style>
   body {
  font-family: Arial, sans-serif;
  background: #121212;  /* Colore scuro di sfondo */
  color: #e0e0e0;  /* Colore del testo chiaro */
  margin: 0;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 10px;
  color: #ffffff;  /* Colore del titolo bianco */
}

.logout {
  position: fixed;
  top: 15px;
  right: 20px;
  background: #333;
  border: none;
  padding: 8px 14px;
  border-radius: 5px;
  cursor: pointer;
  color: #e0e0e0;
  font-weight: bold;
  transition: background-color 0.3s ease;
  text-decoration: none;
  font-size: 0.9em;
}

.logout:hover {
  background: #555;
}

/* Grid layout per le card */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
  max-width: 1000px;
  margin: 20px auto;
}

.card {
  background: #1e1e1e;  /* Colore di sfondo scuro per la card */
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.15);
  text-align: center;
  color: #e0e0e0;  /* Testo chiaro per le card */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}

.card.active {
  border-left: 6px solid #34D399;  /* Verde attivo per stato attivo */
  color: #34D399;
}

.card.inactive {
  border-left: 6px solid #F87171;  /* Rosso attivo per stato inattivo */
  color: #F87171;
}

.title {
  font-weight: 600;
  font-size: 1.15em;
  margin-bottom: 10px;
  color: #ffffff;  /* Titoli bianchi */
}

.status {
  font-size: 1em;
  margin-bottom: 15px;
  font-weight: 500;
}

.status.active {
  color: #34D399;
}

.status.inactive {
  color: #F87171;
}

button.link-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
  align-self: center;
  min-width: 120px;
}

button.link-btn:disabled {
  background-color: #a1a1aa;
  cursor: not-allowed;
}

button.link-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.summary {
  max-width: 400px;
  margin: 30px auto 20px;
  background: #1e1e1e;  /* Colore di sfondo scuro per il riepilogo */
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.15);
  text-align: center;
  font-size: 1.2em;
  font-weight: 600;
  color: #e0e0e0;  /* Testo chiaro nel riepilogo */
}

.python-apps {
  max-width: 700px;
  margin: 20px auto 40px;
  background: #1e1e1e;  /* Colore di sfondo scuro per le app Python */
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.15);
}

.python-apps h2 {
  margin-top: 0;
  text-align: center;
  font-weight: 700;
  color: #1e40af;  /* Colore blu per il titolo delle app Python */
}

.python-apps ul {
  list-style: none;
  padding-left: 0;
}

.python-apps li {
  background: #333;  /* Colore scuro per ciascun elemento */
  margin: 8px 0;
  padding: 12px 15px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 1em;
  display: flex;
  justify-content: space-between;
  align-items: center;
  word-break: break-word;
}

@media (max-width: 480px) {
  body {
    padding: 15px 10px;
  }
  .card {
    padding: 16px;
  }
  .summary {
    max-width: 100%;
  }
  .python-apps {
    max-width: 100%;
    padding: 15px;
  }
  .python-apps li {
    flex-direction: column;
    align-items: flex-start;
  }
  .python-apps button.link-btn {
    margin-top: 8px;
    min-width: auto;
    width: 100%;
  }
}

  </style>
</head>
<body>
  <a href="{{ url_for('logout') }}" class="logout">Logout</a>
  <h1>Dashboard Servizi</h1>
  <div class="grid">
    {% for nome, attivo in stati.items() %}
      {% set css_class = "active" if attivo else "inactive" %}
      {% set link = servizi[nome]["link"] %}
      <div class="card {{ css_class }}" data-nome="{{ nome }}">

        <div class="title">
  <img src="{{ servizi[nome]['icon'] }}" alt="{{ nome }} icon" style="width:20px; vertical-align:middle; margin-right:8px;">
  {{ nome }}
</div>

        <div class="status {{ css_class }}">
          {{ "Attivo" if attivo else "Non attivo" }}
        </div>
        {% if link %}
          <button class="link-btn" 
            onclick="window.open('{{ link }}', '_blank')">
            Apri pagina
          </button>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <div class="summary">
    Servizi attivi: {{ attivi }}/{{ totali }}
  </div>

  <div class="python-apps">
  <h2>App Python</h2>
  {% if python_apps %}
    <ul>
    {% for app, info in python_apps.items() %}
      <li>
        <span class="app-title">
          <img src="{{ info['icon'] }}" alt="{{ app }} icon" style="width:20px; vertical-align:middle; margin-right:8px;">
          {{ app }}
        </span>

        {% if info["link"] %}
          <button class="link-btn" 
            onclick="window.open('{{ info['link'] }}', '_blank')">
            Apri pagina
          </button>
        {% endif %}
      </li>
    {% endfor %}
    </ul>
  {% else %}
    <p style="text-align:center;">Nessuna app Python attiva</p>
  {% endif %}
</div>

</body>
<script>
function aggiornaStati() {
  fetch('/stati_servizi')
    .then(response => {
      if (!response.ok) throw new Error("Errore nella risposta");
      return response.json();
    })
    .then(data => {
      let attivi = 0;
      const totali = Object.keys(data).length;

      for (const [nome, attivo] of Object.entries(data)) {
        const card = document.querySelector(`.card[data-nome="${nome}"]`);
        if (!card) continue;
        const statusEl = card.querySelector(".status");
        if (attivo) {
          attivi++;
          card.classList.add("active");
          card.classList.remove("inactive");
          statusEl.textContent = "Attivo";
          statusEl.classList.add("active");
          statusEl.classList.remove("inactive");
        } else {
          card.classList.remove("active");
          card.classList.add("inactive");
          statusEl.textContent = "Non attivo";
          statusEl.classList.remove("active");
          statusEl.classList.add("inactive");
        }
      }

      // Aggiorna il conteggio nel riepilogo
      const summary = document.querySelector(".summary");
      if (summary) {
        summary.textContent = `Servizi attivi: ${attivi}/${totali}`;
      }
    })
    .catch(error => console.error("Errore aggiornamento stati:", error));
}

// Aggiorna ogni 1 secondo
setInterval(aggiornaStati, 1000);
</script>

</html>
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002
, ssl_context=(
            "/etc/letsencrypt/live/yourdomain/fullchain.pem",  # Certificato
            "/etc/letsencrypt/live/yourdomain/privkey.pem"     # Chiave privata
	    )
)
