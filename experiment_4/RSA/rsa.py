#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import random


class rsa:
    """
    RSA encryption algorithm
    """
    def __init__(self, bit_length, flag=0):
        """
        init rsa
        :param bit_length: give the bit_length for rsa to auto create the public key and private key
        :param flag:
        if flag == 0, means that use auto created key
        if flag == 0, means that use your key
        """
        self.check_bit_length(bit_length)
        self.bit_length = bit_length
        self.p = 0
        self.q = 0
        self.n = 0
        self.e = 0
        self.d = 0
        self.n_length = 0
        if flag == 0:
            self.create_key()
            self.public_key = self.create_public_key()
            self.private_key = self.create_private_key()
        elif flag == 1:
            pass

    def add_public_key(self, public_key):
        """
        add a public key in tuple
        :param public_key: a tuple include (n, e)
        :return: nothing
        """
        self.n, self.e = public_key
        self.n_length = len(bin(self.n)) - 2
        self.public_key = public_key

    def add_private_key(self, private_key):
        """
        add a private key in tuple
        :param private_key: a tuple include (n, d)
        :return: nothing
        """
        self.n, self.d = private_key
        self.n_length = len(bin(self.n)) - 2
        self.private_key = private_key

    def check_bit_length(self, bit_length):
        """
        check the bit_length
        :param bit_length: bit_length
        :return:
        """
        try:
            assert bit_length % 8 == 0
        except AssertionError:
            print('[info] the bit length is illegal')
            exit(0)
        else:
            pass

    def create_key(self):
        """
        1.use miller_rabin_test to create p, q
        2.calculate n = p * q and f_n = (p - 1)(q - 1)
        3.random select e which make gcd(e, f_n) == 1 and calculate d which make e * d == 1 (mod f_n)
        :return: nothing
        """
        p = create_prime(self.bit_length)
        q = create_prime(self.bit_length)
        while p == q:
            p = create_prime(self.bit_length)
            q = create_prime(self.bit_length)
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.n_length = len(bin(self.n)) - 2
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
        """
        just return public key
        :return: public key in tuple
        """
        return self.n, self.e

    def create_private_key(self):
        """
        just return private key
        :return: private key in tuple
        """
        return self.n, self.d

    def check_crypt(self):
        """
        check whether you have n or not
        :return: nothing
        """
        try:
            assert self.n != 0
        except AssertionError:
            print('[info] need public key or private key')
            exit(0)
        else:
            pass

    def encrypt(self, plain_text):
        """
        use public key to encrypt the plain_text
        :param plain_text: plain_text which use ASCII code
        :return: crypto_text coded by hex
        """
        self.check_crypt()
        # encode and group the plain_text
        plain_text_list = encoding(plain_text, self.bit_length)
        crypt_text = ''
        # encrypt every element in plain_text_list
        for i in plain_text_list:
            temp = pow(i, self.e, self.n)
            temp = add_zero(bin(temp).replace('0b', ''), self.n_length, 0)
            crypt_text += temp
        # return crypt_text coded by hex
        return hex(int(crypt_text, 2)).replace('0x', '')

    def decrypt(self, crypt_text):
        """
        use private key to decrypt the crypt_text
        :param crypt_text: crypt_text which use hex
        :return: plain_text coded by ASCII
        """
        self.check_crypt()
        # decode and group the crypt_text
        crypt_text_list = decoding(crypt_text, self.n_length)
        plain_text = ''
        # decrypt every element in crypt_text_list
        for i in crypt_text_list:
            temp = pow(i, self.d, self.n)
            plain_text += num2str(temp)
        # return plain_text coded by ASCII
        return plain_text


def str2num(string):
    # change string to number
    # string must be ASCII string
    result = ''
    for i in string:
        temp = add_zero(bin(ord(i)).replace('0b', ''), 8, 0)
        result += temp
    return int(result, 2)


def num2str(number):
    # change number to string
    # the string must be ASCII string
    result = ''
    number_bin = bin(number).replace('0b', '')[::-1]
    temp = ''
    for i in range(len(number_bin)):
        temp += number_bin[i]
        if (i + 1) % 8 == 0:
            result += chr(int(temp[::-1], 2))
            temp = ''
    if len(temp) > 0:
        result += chr(int(temp[::-1], 2))
    return result[::-1]


def encoding(text, bit_length):
    """
    encode and group the plain_text coded by ASCII
    :param text: ASCII string
    :param bit_length: rsa public_key bit length
    :return: bit_text_list
    """
    bit_len = int((bit_length / 8) - 11)
    bit_text = bin(str2num(text)).replace('0b', '0')
    bit_text_list = text_split(bit_text, bit_len * 8)
    bit_text_list = [int(i, 2) for i in bit_text_list]
    return bit_text_list


def decoding(text, bit_length):
    """
    decode and group the crypt_text coded by hex
    :param text: hex string
    :param bit_length: bit length of n in rsa
    :return: bit_text_list
    """
    bit_text = bin(int(text, 16)).replace('0b', '')
    temp_text = bit_text[::-1]
    temp_text_list = text_split(temp_text, bit_length)
    temp_text_list = [int(i[::-1], 2) for i in temp_text_list][::-1]
    return temp_text_list


def add_zero(bit_text, text_length, flag):
    # add zero to help encode and decode
    # if flag == 0, means that add zero in the front of bit text
    # if flag == 1, means that add zero in the last of bit text
    if flag == 0:
        return (text_length - len(bit_text)) * '0' + bit_text
    elif flag == 1:
        return bit_text + (text_length - len(bit_text)) * '0'


def text_split(text, length_each_element):
    # split text in a list, each element in list have the same length
    temp = ''
    result_list = []
    for i in range(len(text)):
        temp += text[i]
        if (i + 1) % length_each_element == 0:
            result_list.append(temp)
            temp = ''
    if len(temp) > 0:
        result_list.append(temp)
    return result_list


def ex_gcd(a, b):
    # extended Euclidean algorithm
    if b == 0:
        return 1, 0, a
    x, y, r = ex_gcd(b, a % b)
    temp = x
    x = y
    y = temp - (a // b) * y
    return x, y, r


def gcd(a, b):
    # Euclidean algorithm
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def miller_rabin_test(n, times):
    # miller_rabin_test to test whether n is a prime number or not
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
            continue
            # print("Passed Miller-Rabin Test Round " + str(i))
    return True


def primality_test(n):
    # test whether n is a prime number or not
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
    # print("Passed small prime test")
    return miller_rabin_test(n, 50)


def create_prime(bit_length):
    # create prime number by bit_length
    number = random.getrandbits(bit_length)
    while primality_test(number) is False:
        number = random.getrandbits(bit_length)
    return number


def test():
    # test
    k1 = rsa(512)
    print(k1.public_key)
    print(k1.private_key)
    m = 'abcdefghijklmnopqrstuvwxyz' * 10
    print(k1.encrypt(m))
    print(k1.decrypt(k1.encrypt(m)))
    c = '374b8516a6fd5adfc42f047e2dbb686a52295be98f08f833d5d842812eedbcabfec45244384aafbba119f8770acc40777e06d8aac9d1462e5db70f8b9a528ee99f740c998d8976bb4d907ff45d115c32b231d469b6c1a92af07e23604fea8227c492b2316b727228a0be964593f8d3290b646225b7332cd6e0a36dd687e0706133cf0e01c475d78e0b8dc9ae91b718fba9d3024bb96aaf6417a72e8699692643407cbc3fbc57fdacddc2a2f698fe156bc929933b5dd4b928b68e2e221ee923ff4312a54b230c2b05ef35a1263276d976ad5c5a9dbd5f8ded08476ed29f08e918cc48936453cbec939c8146b5359550f37f68b37cbf2c403de948b58ba131f365761ce78b284154013cc7e22fa32dd9dfb21f1c6a0f827dd9b1e289bb6ff76de10bbfd0ad2bdfad4ae192aa2b7dc2c7284039d96d598640abf75bdf5ed0a326c49cedaaaf297352e7a683765a37e89d6be0e3bf3984c3ca2cd600657189dfc480d049d002614da8641e177a4a1a2f7d04ce92a1d14d0e99b80fe4b90eb95d85ecd2e4abec04b9aed7bb15c50aae8acbd6b458f7a8ac1d136ad56f11f4acb9899de5777b1e07c8416b7dedac27e2190d249de71a4c9bd6a800ee99dfe17cffa3475527de9e4a259a8c112e18ac12a1b60c0793fbb399091ee5d68494470d51e0fd12e8e57252f04d010f9cc125495dcf130b35c39bf2d96ff4cd726c0e4b9698f9a3ab927e80f4d011bdfd38274843f1883e859824a0ab4d005e82597fbd755caab79e26ef0853227ee1ee91c06fd6646255c7c34ff9dbefbdc774211936d9c1e63986e84b4d0929b775ccc98d8f6eb4cd0b35f6f7f6a95c14be5c4c1111413bffc0672822c32a6d950767a56d2f0c4381b8158de2a91864509f71e147e73ae7c'
    p_k = (66178137859947552294398775255802548131934535631352006996001768150973805789119926110454870176327677268631949099257033283723185302659618363275275761532415743102822176613384047900391045477262069197380449587134929546173719276767726845022806267579748687327002433086729059218158505544514907284650347186194039945319, 9761466745653204245928392454340672992415807153030803224276936131364484637778515883235181156356068176172939587781492786324996509680805313365540043874880574708820757382450790625765509381638050412780570426803821247188292498760873872404858533182202090795600387228109319361972870957945179536022489733176256775451)
    k2 = rsa(512, flag=1)
    k2.add_private_key(p_k)
    print(k2.decrypt(c))

if __name__ == '__main__':
    test()
