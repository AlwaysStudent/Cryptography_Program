#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import random
import base64


class rsa:
    """
    RSA encryption algorithm
    """
    def __init__(self, bit_length):
        self.bit_length = bit_length
        self.p = 0
        self.q = 0
        self.n = 0
        self.e = 0
        self.d = 0
        self.create_key()
        self.public_key = self.create_public_key()
        self.private_key = self.create_private_key()

    def create_key(self):
        p = create_prime(self.bit_length)
        q = create_prime(self.bit_length)
        while p == q:
            p = create_prime(self.bit_length)
            q = create_prime(self.bit_length)
        self.p = p
        self.q = q
        self.n = self.p * self.q
        e = random.getrandbits(64)
        f_n = (self.p - 1) * (self.q - 1)
        while gcd(f_n, e) > 1:
            e = random.getrandbits(64)
        self.e = e
        d = ex_gcd(f_n, e)[1] % f_n
        self.d = d
        try:
            assert (e * d) % f_n == 1
        except AssertionError:
            print('[info] wrong in count d!')
            exit(0)
        else:
            pass

    def create_public_key(self):
        return self.n, self.e

    def create_private_key(self):
        return self.n, self.d

    def encrypt(self, plain_text):
        plain_text_list = coding(plain_text, self.bit_length)

def coding(text, bit_length):
    bit_len = (bit_length / 8) - 11



def text_split(text, length_each_element)

def ex_gcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, r = ex_gcd(b, a % b)
    temp = x
    x = y
    y = temp - (a // b) * y
    return x, y, r


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def miller_rabin_test(n, times):
    m = n - 1
    k = 0
    while m % 2 == 0:
        m = m // 2
        k += 1
    for i in range(0, times):
        isprime = False
        a = random.randint(1, n - 1)
        b = pow(a, m, n)
        b = b % n
        if b == 1:
            isprime = True
        for j in range(0, k):
            if b == n - 1:
                isprime = True
                break
            b = (b * b) % n
        if not isprime:
            return False
        else:
            print("Passed Miller-Rabin Test Round " + str(i))
    return True


def primality_test(n):
    small_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
                        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
                        151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
                        317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                        419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
                        607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                        701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
                        811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                        911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
                        1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093,
                        1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193,
                        1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289,
                        1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399,
                        1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483,
                        1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571,
                        1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663,
                        1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759,
                        1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
                        1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987,
                        1993, 1997, 1999]
    for prime in small_prime_list:
        if n % prime == 0:
            return False
    print("Passed small prime test")
    return miller_rabin_test(n, 50)


def create_prime(bit_length):
    number = random.getrandbits(bit_length)
    while primality_test(number) is False:
        number = random.getrandbits(bit_length)
    return number


def test():
    k = rsa(512)
    print(k.public_key)
    print(k.private_key)


if __name__ == '__main__':
    test()
