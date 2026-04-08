from RSA import RSA
from SSS import SSS


def main():
    print("---------- Witaj w programie szyfrującym ----------")
    secret = None
    shares = None
    rsa = RSA(q=7919, p=1009)
    sss = SSS()
    while True:
        print("Wybierz operację\n"
              "\t1. Szyfrowanie klucza\n"
              "\t2. Rozszyfrowywanie klucza\n"
              "\t3. Wyświetl informację o kluczach RSA\n"
              "\t4. Podziel klucz na części\n"
              "\t5. Rekonstruuj klucz\n"
              "\t6. Zapisz udziały do pliku\n"
              "\t7. Wyjście")
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
                print()
            case 4:
                if secret is not None:
                    k = int(input("Podaj liczbę udziałów (części): "))
                    t = int(input(f"Podaj próg rekonstrukcji (<=  {k}): "))
                    shares = sss.split_secret(secret, t, k)
                    print(shares)
            case 5:
                if shares is not None:
                    i = int(input("Podaj liczbę udziałów (części): "))
                    reconstructed_secret = sss.reconstruct_secret(shares[:i])
                    print(f"Zrekonstruowany klucz: {reconstructed_secret}")
                    print(f"Odkodowana wiadomość: {rsa.decrypt(reconstructed_secret)}")
            case 6:
                if shares is not None:
                    i = 1
                    for _, part in shares:
                        with open(str(i)+".udzial", "w") as file:
                            file.write(str(part))
                        i += 1
            case 7:
                return
            case _:
                print("Podano nieprawidłowy numer operacji")


if __name__ == "__main__":
    main()
