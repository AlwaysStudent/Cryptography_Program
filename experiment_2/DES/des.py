#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import time


class des:
    """
    DES encryption algorithm
    """
    def __init__(self, key):
        # check key len
        try:
            assert len(key) == 14
        except AssertionError:
            print('[info] key is illegal')
            print('[info] the process will exit')
            time.sleep(1)
            exit(0)
        else:
            pass
        # make key to 64 bit
        self.key = key
        self.key_create()
        self.key_len = len(self.key)
        self.key_list = []
        self.crypto_text = ''
        self.plain_text = ''

    def encode(self, plain_text):
        self.plain_text = plain_text


        return self.crypto_text

    def decode(self, crypto_text):
        self.crypto_text = crypto_text


        return self.plain_text

    def create_key_list(self):
        pass

    def key_create(self):
        key_bins = int('0x' + self.key, 16)
        key_bins = bin(key_bins).replace('0b', '')
        key_bins = '0' * (56 - len(key_bins)) + key_bins
        key_temp = ''
        temp = []
        for i in range(len(key_bins)):
            temp.append(key_bins[i])
            if len(temp) == 7:
                temp_bit = 1
                for j in temp:
                    temp_bit = temp_bit ^ int(j)
                temp.append(temp_bit)
                key_temp += ''.join([str(k) for k in temp])
                temp = []
        self.key = key_temp







def test():
    key1 = 'ffffffffffffff'
    key2 = 'fafffbffffffff'
    x = des(key1)
    print(x.key)
    print(x.key_len)
    y = des(key2)
    print(y.key)
    print(y.key_len)


if __name__ == '__main__':
    test()
