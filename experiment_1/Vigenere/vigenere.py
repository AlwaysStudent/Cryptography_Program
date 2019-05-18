#!/opt/anaconda
# -*- coding = utf-8 -*-


class vigenere:
    """
    Vigenere encryption algorithm
    """
    def __init__(self, key):
        # set key
        self.key = key
        self.key_len = len(key)
        self.ciphertext = ''
        self.plaintext = ''
        self.ciphertext_list = []

    def reset_key(self, key):
        # just reset key
        self.key = key
        self.key_len = len(key)

    def encode(self, plaintext):
        # input plaintext, and encrypt the plaintext with known key
        self.plaintext = plaintext
        self.ciphertext = ''
        # loop through plaintext and key to encrypt
        for i in range(len(self.plaintext)):
            j = i % self.key_len
            self.ciphertext += enciphering(self.plaintext[i], self.key[j])
        # output info and return ciphertext
        print('[info] Encode successfully !')
        return self.ciphertext

    def decode(self, ciphertext):
        # input ciphertext, and decrypt ciphertext with known ke
        self.ciphertext = ciphertext
        self.plaintext = ''
        # loop through ciphertext and key to decrypt
        for i in range(len(self.ciphertext)):
            j = i % self.key_len
            self.plaintext += deciphering(self.ciphertext[i], self.key[j])
        # output info and return plaintext
        print('[info] Decode successfully !')
        return self.plaintext

    def try_to_decode(self, ciphertext):
        # try to decrypt ciphertext without key and find key
        assert self.key == ''
        self.ciphertext = ciphertext.lower()
        self.plaintext = ''
        self.get_key_len()
        self.get_key()
        return self.decode(ciphertext)

    def get_key_len(self):
        # use index of coincidence to get key length
        self.ciphertext_list = [ord(i) - ord('a') for i in list(self.ciphertext)]
        # use ioc_list to store average of each guess_key_len
        ioc_list = []
        for guess_key_len in range(1, 15):
            ioc_list.append(index_of_coincidence(self.ciphertext_list, guess_key_len))
        # the index of ioc_list max member has the largest possibility to be the key_len
        sorted_ioc_list = sorted([abs(i - 0.065) for i in ioc_list])
        ioc_list = [abs(i - 0.065) for i in ioc_list]
        possibility_key_len = []
        for i in range(2):
            possibility_key_len.append(ioc_list.index(sorted_ioc_list[i]) + 1)
        self.key_len = gcd(possibility_key_len[0], possibility_key_len[1])
        print('[info] guess key length is : %d' % self.key_len)

    def list_cipher_by_key_len(self):
        # change ciphertext to many part by key_len
        result = []
        for i in range(self.key_len):
            result.append(self.ciphertext[i::self.key_len])
        return result

    def get_key(self):
        # use mutual_index_of_coincidence to get key
        cipher_list = self.list_cipher_by_key_len()
        key_list = []
        for each in cipher_list:
            key_list.append(mutual_index_of_coincidence(each))
        print("[info] guess key is : ", key_list)
        self.key = key_list


def gcd(m, n):
    if m % n == 0:
        return n
    else:
        return gcd(n, m % n)


def mutual_index_of_coincidence(part):
    # mutual_index_of_coincidence is to get key
    # AlphaRate for 'a' to 'z'
    AlphaRate = [0.08167, 0.01492, 0.02782, 0.04253, 0.12705, 0.02228, 0.02015, 0.06094, 0.06996,
                 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.0009, 0.05987,
                 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.0015, 0.01974, 0.00074]
    # store 26 kinds of mutual_index_of_coincidence
    mioc_list = []
    # loop through 26 kinds
    for i in range(26):
        # use enciphering to change part
        temp_part = [enciphering(j, i) for j in part]
        # store 26 kinds of alpha count
        each_list = []
        sum_of_each_mioc = 0
        # use AlphaRate and changed-part calculate mutual_index_of_coincidence
        for j in range(26):
            each = temp_part.count(chr(ord('a') + j))
            each_list.append(each)
            sum_of_each_mioc += ((float(each) * AlphaRate[j]) / len(temp_part))
        mioc_list.append(sum_of_each_mioc)
    # find the closest member to 0.065 and return
    temp_mioc_list = [abs(i - 0.0655) for i in mioc_list]
    return (26 - temp_mioc_list.index(min(temp_mioc_list))) % 26


def index_of_coincidence(ciphertext_list, guess_key_len):
    # using cipherlist and guessing length of key to calculate the index_of_coincidence
    sum_of_ioc = 0
    for i in range(guess_key_len):
        sum_of_pk = 0
        single_list = ciphertext_list[i::guess_key_len]
        for j in range(26):
            sum_of_pk = sum_of_pk + single_list.count(j) * (single_list.count(j) - 1)
        ioc = float(sum_of_pk)/(len(single_list) * (len(single_list) - 1))
        sum_of_ioc = sum_of_ioc + ioc
    # return average of all index_of_coincidence
    return sum_of_ioc / guess_key_len


def enciphering(letter, key):
    # encipher the single letter and single key
    if letter.islower() == 1:
        result = chr((ord(letter) + key - ord('a')) % 26 + ord('a'))
    elif letter.isupper() == 1:
        result = chr((ord(letter) + key - ord('A')) % 26 + ord('A'))
    else:
        result = letter
    return result


def deciphering(letter, key):
    # decipher the single letter and single key
    if letter.islower() == 1:
        result = chr((ord(letter) - key - ord('a')) % 26 + ord('a'))
    elif letter.isupper() == 1:
        result = chr((ord(letter) - key - ord('A')) % 26 + ord('A'))
    else:
        result = letter
    return result


def display(text, number=50):
    count = 1
    for i in text:
        print(i, end='')
        count += 1
        if count % number == 0:
            print()


def test():
    # key = [2, 14, 3, 4, 18]
    c = 'Vvhqwvvrhmusgjgthkihtssejchlsfcbgvwcrlr' \
        'yqtfsvgahwkcuhwauglqhnslrljshbltspisprd' \
        'xljsveeGhlqwkasskuwepwqtwvspgoelkcqyfns' \
        'vwljsniqkgnrgybwlwgoviokhkazkqkxzgyhcec' \
        'meiujoqkwfwvefqhkijrclrlkbienqfrjljsdhg' \
        'rhlsfqtwlauqrhwdmwlgusgikkflryvcwvspgpm' \
        'lkassjvoqxeggveyggzmljcxxljsvpaivwikvrd' \
        'rygfrjljslveggveyggeiapuuisfpbtgnwwmucz' \
        'rvtwglrwugumnczvile'
    k = vigenere('')
    display(k.try_to_decode(c))


if __name__ == '__main__':
    test()
