from RSA import RSA


def main():
    print("---------- Witaj w programie szyfrującym ----------")
    privateKey = None
    rsa = RSA(n=3233, p=61)
    while True:
        print("Wybierz operację\n"
              "\t1. Szyfrowanie klucza\n"
              "\t2. Rozszyfrowywanie klucza\n"
              "\t3. Wyjście")
        try:
            i = int(input("Podaj numer: "))
        except ValueError:
            print("Proszę podać prawidłowy numer operacji (liczbę).")
            continue
        match i:
            case 1:
                try:
                    privateKey = rsa.encrypt(int(input("Podaj klucz: ")))
                    print("Klucz został zaszyfrowany.")
                except ValueError:
                    print("Niepoprawny klucz — podaj liczbę.")
            case 2:
                if privateKey is not None:
                    message = rsa.decrypt(privateKey)
                    print("Odszyfrowana wiadomość:", message)
                else:
                    print("Brak klucza")
            case 3:
                return
            case _:
                print("Podano nieprawidłowy numer operacji")


if __name__ == "__main__":
    main()
