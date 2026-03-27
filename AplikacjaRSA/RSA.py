class RSA:
    """
    Klasa RSA.
        :param n: Maksymalny zakres szyfrowania
        :param p: Liczba pierwsza (do szyfrowania)

        :ivar q:  Druga liczba pierwsza
        :ivar e:  Klucz publiczny
        :ivar d:  Klucz prywatny
    """
    def __init__(self, n, p):
        """
        Konstruktor klasy RSA
        :param n: Maksymalny zakres szyfrowania
        :param p: Liczba pierwsza (do szyfrowania)
        """
        self.n = n
        self.p = p
        self.q = n // p
        self.e = 65537
        self.d = pow(self.e, -1, (self.p - 1) * (self.q - 1))

    def encrypt(self, plaintext):
        """
        Funkcja szyfrująca wiadomość
        :param plaintext: wiadomość podana jako liczba z zakresu od 0 do n
        :return: zaszyfrowana wiadomość
        """
        return pow(plaintext, self.e, self.n)
    def decrypt(self, ciphertext):
        """
        Funkcja odszyfrowująca wiadomość
        :param ciphertext: zaszyfrowana wiadomość
        :return: odszyfrowana wiadomość
        """
        return pow(ciphertext, self.d, self.n)