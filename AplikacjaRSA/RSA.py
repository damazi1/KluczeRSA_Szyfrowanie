import random

def is_prime(n, k=5):
    """Test pierwszości Millera-Rabina"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits):
    """Generuje dużą liczbę pierwszą o podanej liczbie bitów."""
    while True:
        # Generowanie losowej liczby z ustawionymi najwyższymi i najniższymi bitami
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p

class RSA:
    """
    Klasa RSA.
        :param q: Liczba Pierwsza (do szyfrowania)
        :param p: Liczba pierwsza (do szyfrowania)
        :param bits: (Opcjonalnie) Ilość bitów, jeżeli chcemy automatycznie wygenerować liczby p i q

        :ivar n:  Zakres szyfrowania
        :ivar e:  Klucz publiczny
        :ivar d:  Klucz prywatny
    """
    def __init__(self, p=None, q=None, bits=1024):
        """
        Konstruktor klasy RSA
        :param p: Liczba pierwsza (do szyfrowania)
        :param q: Druga liczba pierwsza (do szyfrowania)
        :param bits: Ilość bitów do generacji losowej liczby
        :ivar n: Maksymalny zakres szyfrowania (n = p * q)
        :ivar e: Klucz publiczny (domyślnie 65537)
        :ivar d: Klucz prywatny (obliczany automatycznie)
        """
        if p is None or q is None:
            self.p = generate_large_prime(bits)
            self.q = generate_large_prime(bits)
        else:
            self.p = p
            self.q = q
            
        self.n = self.p * self.q
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