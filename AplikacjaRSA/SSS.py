class SSS:
    """
    Klasa implementująca algorytm Shamir Secret Sharing (SSS).
    Umożliwia podział sekretu na części tak, że dowolne k części
    można użyć do rekonstrukcji sekretu.
    """

    def __init__(self, prime=None):
        """
        Konstruktor klasy SSS
        :param prime: Liczba pierwsza dla arytmetyki modularnej (opcjonalne)
        :ivar secret: Przechowywany sekret
        :ivar shares: Lista części sekretu
        :ivar prime: Liczba pierwsza dla operacji modularnych
        """
        self.secret = None
        self.shares = []
        self.prime = prime if prime else 2147483647  # Duża liczba pierwsza
        self.coefficients = []

    def create_polynomial(self, secret, k):
        """
        Tworzy wielomian o stopniu k-1 z wyrazem wolnym równym sekretowi.
        Używany do generowania części sekretu.

        :param secret: Sekret do podzielenia
        :param k: Minimalna liczba części potrzebna do rekonstrukcji
        :return: Lista współczynników wielomianu [a0, a1, ..., a(k-1)]
        """
        import random
        self.coefficients = [secret]
        for _ in range(k - 1):
            self.coefficients.append(random.randint(1, self.prime - 1))
        return self.coefficients

    def evaluate_polynomial(self, x):
        """
        Oblicza wartość wielomianu w punkcie x.
        Używa schematu Hornera dla wydajności.

        :param x: Punkt, w którym obliczamy wartość
        :return: Wartość wielomianu f(x) mod prime
        """
        result = 0
        for coefficient in reversed(self.coefficients):
            result = (result * x + coefficient) % self.prime
        return result

    def split_secret(self, secret, k, n):
        """
        Dzieli sekret na n części, z których każde k wystarczy do rekonstrukcji.

        :param secret: Sekret do podzielenia
        :param k: Minimalna liczba części do rekonstrukcji (threshold)
        :param n: Całkowita liczba generowanych części
        :return: Lista części sekretu jako krotki (x, y)
        """
        if k > n:
            raise ValueError("k (threshold) nie może być większe niż n (liczba części)")
        if secret >= self.prime:
            raise ValueError("Sekret musi być mniejszy niż liczba pierwsza")

        self.secret = secret
        self.create_polynomial(secret, k)

        self.shares = []
        for x in range(1, n + 1):
            y = self.evaluate_polynomial(x)
            self.shares.append((x, y))

        return self.shares

    def lagrange_coefficient(self, x_values, x, i):
        """
        Oblicza współczynnik Lagrange'a dla interpolacji Lagrange'a.

        :param x_values: Lista współrzędnych x części sekretu
        :param x: Punkt, w którym obliczamy współczynnik
        :param i: Indeks współczynnika
        :return: Współczynnik Lagrange'a
        """
        numerator = 1
        denominator = 1

        for j, xj in enumerate(x_values):
            if i != j:
                numerator = (numerator * (x - xj)) % self.prime
                denominator = (denominator * (x_values[i] - xj)) % self.prime

        # Odwrotność modułowa: denominator^(-1) mod prime
        inv_denominator = pow(denominator, -1, self.prime)
        return (numerator * inv_denominator) % self.prime

    def reconstruct_secret(self, shares, k=None):
        """
        Rekonstruuje sekret z k części sekretu.
        Używa interpolacji wielomianów Lagrange'a.

        :param shares: Lista części sekretu jako krotki (x, y)
        :param k: Liczba części do użycia (jeśli None, używa wszystkich)
        :return: Zrekonstruowany sekret
        """
        if k is None:
            k = len(shares)

        if len(shares) < k:
            raise ValueError(f"Potrzebujesz co najmniej {k} części do rekonstrukcji")

        # Weź pierwsze k części
        used_shares = shares[:k]
        x_values = [x for x, y in used_shares]
        y_values = [y for x, y in used_shares]

        # Oblicz sekret dla x=0 używając interpolacji Lagrange'a
        secret = 0
        for i, (xi, yi) in enumerate(used_shares):
            li = self.lagrange_coefficient(x_values, 0, i)
            secret = (secret + yi * li) % self.prime

        return secret

    def get_shares_info(self):
        """
        Zwraca informacje o wygenerowanych częściach sekretu.

        :return: Słownik z informacjami o sekretach
        """
        return {
            "liczba_czesci": len(self.shares),
            "czesci": self.shares,
            "sekret": self.secret
        }
