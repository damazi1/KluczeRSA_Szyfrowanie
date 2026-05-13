from RSA import RSA, generate_large_prime
from SSS import SSS
import requests


def main():
    print("---------- Witaj w programie szyfrującym ----------")
    secret = None
    shares = None
    # Initialize RSA with automatically generated large prime numbers (e.g. 1024 bits)
    rsa = RSA(bits=1024)
    # n ma około 2048 bitów (jeśli p i q to 1024). Liczba pierwsza do SSS musi być od niego większa!
    sss = SSS(prime=generate_large_prime(rsa.n.bit_length() + 1))

    servers = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]

    while True:
        print("Wybierz operację\n"
              "\t1. Szyfrowanie klucza\n"
              "\t2. Rozszyfrowywanie klucza\n"
              "\t3. Wyświetl informację o kluczach RSA\n"
              "\t4. Podziel klucz na części\n"
              "\t5. Rekonstruuj klucz\n"
              "\t6. Wyślij udziały na serwery (Docker)\n"
              "\t7. Pobierz udziały z serwerów i zrekonstruuj\n"
              "\t8. Generuj nowe klucze (automatycznie)\n"
              "\t9. Wyjście")
        try:
            i = int(input("Podaj numer: "))
        except ValueError:
            print("Proszę podać prawidłowy numer operacji (liczbę).")
            continue
        match i:
            case 1:
                try:
                    secret = rsa.encrypt(int(input("Podaj klucz: ")))
                    print("Klucz został zaszyfrowany.")
                except ValueError:
                    print("Niepoprawny klucz — podaj liczbę.")
            case 2:
                if secret is not None:
                    message = rsa.decrypt(secret)
                    print("Odszyfrowana wiadomość:", message)
                else:
                    print("Brak klucza")
            case 3:
                print(f"\n--- INFORMACJE O KLUCZACH RSA ---")
                print(f"Liczba pierwsza p: {rsa.p}")
                print(f"Liczba pierwsza q: {rsa.q}")
                print(f"Moduł (n): {rsa.n}")
                print(f"Klucz publiczny (e): {rsa.e}")
                if secret is not None:
                    print(f"Klucz prywatny (d): {rsa.d}")
                else:
                    print("Brak klucza prywatnego")
                print(f"Liczba pierwsza SSS: {sss.prime}")
                print()
            case 4:
                if secret is not None:
                    k = int(input("Podaj liczbę udziałów (części): "))
                    t = int(input(f"Podaj próg rekonstrukcji (<=  {k}): "))
                    try:
                        shares = sss.split_secret(secret, t, k)
                        print(shares)
                    except ValueError as e:
                        print(f"Błąd: {e}")
                else:
                     print("Najpierw zaszyfruj klucz (opcja 1).")
            case 5:
                if shares is not None:
                    i = int(input("Podaj liczbę udziałów (części): "))
                    reconstructed_secret = sss.reconstruct_secret(shares[:i])
                    print(f"Zrekonstruowany klucz: {reconstructed_secret}")
                    print(f"Odkodowana wiadomość: {rsa.decrypt(reconstructed_secret)}")
                else:
                    print("Brak udziałów.")
            case 6:
                if shares is not None:
                    for idx, (share_id, part) in enumerate(shares):
                        if idx < len(servers):
                            try:
                                requests.post(f"{servers[idx]}/share", json={"share": [share_id, part]})
                                print(f"Udział {share_id} wysłany do serwera {servers[idx]}")
                            except requests.exceptions.RequestException as e:
                                print(f"Błąd wysyłania do {servers[idx]}: {e}")
                        else:
                            print(f"Brak serwera dla udziału {share_id}. Zapisuję lokalnie.")
                            with open(str(share_id)+".udzial", "w") as file:
                                file.write(str(part))
                else:
                    print("Brak udziałów - najpierw użyj opcji 4.")
            case 7:
                fetched_shares = []
                for server in servers:
                    try:
                        response = requests.get(f"{server}/share")
                        if response.status_code == 200:
                            fetched_shares.append(tuple(response.json()["share"]))
                            print(f"Pobrano udział z {server}")
                    except requests.exceptions.RequestException:
                        print(f"Nie udało się połączyć z {server}")
                if fetched_shares:
                    try:
                        reconstructed = sss.reconstruct_secret(fetched_shares)
                        print(f"\nZrekonstruowany klucz z serwerów: {reconstructed}")
                        print(f"Odkodowana wiadomość: {rsa.decrypt(reconstructed)}")
                    except Exception as e:
                        print(f"Błąd przy rekonstrukcji: {e}")
                else:
                    print("Nie udało się pobrać wystarczającej liczby udziałów z serwerów.")
            case 8:
                bits = int(input("Podaj długość klucza w bitach (domyślnie 1024): ") or 1024)
                rsa = RSA(bits=bits)
                sss = SSS(prime=generate_large_prime(rsa.n.bit_length() + 1))
                secret = None
                shares = None
                print(f"Nowe klucze wygenerowane. Rozmiar: {bits} bitów.")
            case 9:
                return
            case _:
                print("Podano nieprawidłowy numer operacji")


if __name__ == "__main__":
    main()
