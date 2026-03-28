class RSA:
    """
    Klasa RSA.
        :param q: Liczba Pierwsza (do szyfrowania)
        :param p: Liczba pierwsza (do szyfrowania)

        :ivar n:  Zakres szyfrowania
        :ivar e:  Klucz publiczny
        :ivar d:  Klucz prywatny
    """
    def __init__(self, p, q):
        """
        Konstruktor klasy RSA
        :param p: Liczba pierwsza (do szyfrowania)
        :param q: Druga liczba pierwsza (do szyfrowania)
        :ivar n: Maksymalny zakres szyfrowania (n = p * q)
        :ivar e: Klucz publiczny (domyślnie 65537)
        :ivar d: Klucz prywatny (obliczany automatycznie)
        """
        self.n = p * q
        self.p = p
        self.q = q
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