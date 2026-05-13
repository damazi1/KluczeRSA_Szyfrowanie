from flask import Flask, render_template, request, redirect, url_for
from RSA import RSA, generate_large_prime
from SSS import SSS
import requests

app = Flask(__name__)

# Initialize RSA with 1024-bit large prime numbers
rsa = RSA(bits=1024)
# SSS wymaga liczby pierwszej większej niż dzielony sekret (który może osiągnąć wielkość modułu n).
# Ponieważ n ma do 2048 bitów, używamy generatora z RSA do stworzenia 2049-bitowej liczby pierwszej
sss = SSS(prime=generate_large_prime(2049))

# Global state to keep track of operations
state = {
    'secret': None,
    'shares': None,
    'servers': ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"],
    'reconstructed_secret': None,
    'decrypted_message': None,
    'messages': []
}

@app.route('/')
def index():
    return render_template('index.html', rsa=rsa, sss=sss, state=state)

@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    global rsa, sss
    bits = request.form.get('bits', default=1024, type=int)
    rsa = RSA(bits=bits)
    # Generujemy nową liczbę pierwszą dla SSS o wielkości n + 1 bit
    prime_bits = rsa.n.bit_length() + 1
    sss = SSS(prime=generate_large_prime(prime_bits))
    
    state['secret'] = None
    state['shares'] = None
    state['messages'].append(f"Nowe klucze RSA wygenerowane (Rozmiar: {bits} bitów). Nowa liczba pierwsza SSS ma {prime_bits} bitów.")
    return redirect(url_for('index'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    key = request.form.get('key', type=int)
    if key is not None:
        state['secret'] = rsa.encrypt(key)
        state['messages'].append("Klucz został zaszyfrowany.")
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if state['secret'] is not None:
        message = rsa.decrypt(state['secret'])
        state['messages'].append(f"Odszyfrowana wiadomość: {message}")
    else:
        state['messages'].append("Brak klucza do rozszyfrowania.")
    return redirect(url_for('index'))

@app.route('/split', methods=['POST'])
def split():
    if state['secret'] is not None:
        k = request.form.get('k', type=int)
        t = request.form.get('t', type=int)
        if k and t:
            try:
                state['shares'] = sss.split_secret(state['secret'], t, k)
                state['messages'].append(f"Podzielono klucz na {k} udziałów (próg {t}).")
            except Exception as e:
                state['messages'].append(f"Błąd podziału: {str(e)}")
    else:
        state['messages'].append("Brak zaszyfrowanego klucza do podziału.")
    return redirect(url_for('index'))

@app.route('/send_servers', methods=['POST'])
def send_servers():
    if state['shares'] is not None:
        for idx, (share_id, part) in enumerate(state['shares']):
            if idx < len(state['servers']):
                server = state['servers'][idx]
                try:
                    requests.post(f"{server}/share", json={"share": [share_id, part]})
                    state['messages'].append(f"Udział {share_id} wysłany do {server}")
                except Exception as e:
                    state['messages'].append(f"Błąd wysyłania do {server}: {e}")
            else:
                state['messages'].append(f"Brak serwera dla udziału {share_id}.")
    else:
        state['messages'].append("Brak udziałów do wysłania.")
    return redirect(url_for('index'))

@app.route('/fetch_servers', methods=['POST'])
def fetch_servers():
    fetched_shares = []
    for server in state['servers']:
        try:
            response = requests.get(f"{server}/share")
            if response.status_code == 200:
                fetched_shares.append(tuple(response.json()["share"]))
                state['messages'].append(f"Pobrano udział z {server}")
        except Exception:
            state['messages'].append(f"Nie udało się połączyć z {server}")
            
    if fetched_shares:
        try:
            reconstructed = sss.reconstruct_secret(fetched_shares)
            state['reconstructed_secret'] = reconstructed
            state['decrypted_message'] = rsa.decrypt(reconstructed)
            state['messages'].append(f"Zrekonstruowany klucz: {reconstructed}")
            state['messages'].append(f"Odkodowana wiadomość: {state['decrypted_message']}")
        except Exception as e:
             state['messages'].append(f"Błąd podczas rekonstrukcji: {e}")
    else:
        state['messages'].append("Nie udało się pobrać udziałów z serwerów.")
    return redirect(url_for('index'))

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    state['messages'] = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
