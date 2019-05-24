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
        # the real key is 56 bit
        self.real_key = key
        # make key to 64 bit
        self.key = key
        self.key_create()
        # mark the length of key
        self.key_len = len(self.key)
        # use function create_key_list to create 16 keys for each round
        self.key_list = []
        self.create_key_list()
        # mark crypto_text and plain_text
        self.crypto_text = ''
        self.plain_text = ''

    def encode(self, plain_text):
        # use plain_text and key to encode
        self.plain_text = plain_text


        return self.crypto_text

    def decode(self, crypto_text):
        # use plain_text and key to decode
        self.crypto_text = crypto_text


        return self.plain_text

    def create_key_list(self):
        # use pc_switch_1 and pc_switch_2 to make key to a key list
        pc_switch_1 = [[57, 49, 41, 33, 25, 17, 9],
                       [1, 58, 50, 42, 34, 26, 18],
                       [10, 2, 59, 51, 43, 35, 27],
                       [19, 11, 3, 60, 52, 44, 36],
                       [63, 55, 47, 39, 31, 23, 15],
                       [7, 62, 54, 46, 38, 30, 22],
                       [14, 6, 61, 53, 45, 37, 29],
                       [21, 13, 5, 28, 20, 12, 4]]
        pc_switch_2 = [[14, 17, 11, 24, 1, 5],
                       [3, 28, 15,  6, 21, 10],
                       [23, 19, 12,  4, 26, 8],
                       [16,  7, 27, 20, 13,  2],
                       [41, 52, 31, 37, 47, 55],
                       [30, 40, 51, 45, 33, 48],
                       [44, 49, 39, 56, 34, 53],
                       [46, 42, 50, 36, 29, 32]]

        # use pc_switch_1 to get key_c and key_d
        key_temp = switch_by_matrix(add_zero(hex2bin(self.key), 64), pc_switch_1)
        key_c = key_temp[:28]
        key_d = key_temp[28:]

        # get 16 rounds key
        for i in range(1, 17):
            key_c = ls_shift(key_c, i)
            key_d = ls_shift(key_d, i)

            # add each key to key_list
            self.key_list.append(bin2hex(switch_by_matrix(key_c + key_d, pc_switch_2)))

    def key_create(self):
        # use real_key to create the key with check bits
        key_bins = hex2bin(self.key)
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
        self.key = bin2hex(key_temp)


def add_zero(source_text, number):
    # add zero in the front of the source_text until the length of it is equal to number
    if number > len(source_text):
        return '0' * (number - len(source_text)) + source_text
    else:
        return source_text


def ls_shift(key, number):
    # shift the key_c and key_d
    number_list = [1, 2, 9, 16]
    if number in number_list:
        return key[1:] + key[:1]
    else:
        return key[2:] + key[:2]


def bin2hex(bin_str):
    # make bin to hex without '0x'
    return hex(int('0b'+bin_str, 2)).replace('0x', '')


def hex2bin(hex_str):
    # make hex to bin without '0b'
    return bin(int('0x'+hex_str, 16)).replace('0b', '')


def switch_by_matrix(source_text, matrix):
    # switch source_text to result_text with a matrix
    result_text = ''
    for i in matrix:
        for j in i:
            result_text += source_text[j - 1]
    return result_text


def split_the_text(source_text, number):
    text_list = []
    temp = ''
    for i in range(len(source_text)):
        temp += source_text[i]
        if (i + 1) % number == 0:
            text_list.append(temp)
            temp = []
    text_list = [add_zero_last(i, 64) for i in text_list]
    return text_list


def add_zero_last(source_text, number):
    if len(source_text) < number:
        result_text = source_text + '0' * (number - len(source_text))
    else:
        result_text = source_text
    return result_text


def test():
    # test des
    key1 = 'f'*14
    x = des(key1)
    print('\n\n')
    print(x.real_key)
    print(x.key)
    print(x.key_len)
    print(x.key_list)


if __name__ == '__main__':
    test()
