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
        # group plain_text into list
        # each element in list has 64 bits
        plain_text_list = group(self.plain_text)
        crypto_text = ''
        # using run_coding to encode each piece of plain_text
        for each in range(len(plain_text_list)):
            temp = self.run_coding(plain_text_list[each], each)
            crypto_text += temp
        self.crypto_text = crypto_text
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

    def run_coding(self, text, number):
        # use ip_switch to switch the text by ip(1)
        atfer_ip_switch_text = ip_switch(text, 1)
        # run feistel net with key_list to coding the text
        atfer_feistel_text = feistel_net(atfer_ip_switch_text, self.key_list, number)
        # use ip_switch to switch the text by ip(-1)
        final_text = ip_switch(atfer_feistel_text, -1)
        return final_text


def feistel_net(text, key_list, number):
    # run feistel net
    # 16 round coding
    # number is equal to 1 means encode and -1 means decode
    temp_text = text
    for i in range(16)[::number]:
        left_text = temp_text[:32]
        right_text = temp_text[32:]
        temp = function_f(right_text, key_list[i])
        temp_text = right_text + xor(left_text, temp)
    return temp_text


def function_f(text, key):
    # use s-box to switch text with key
    pass


def group(text):
    # group text into list
    # each element in list has 64 bits
    text_list = [bin(ord(i)).replace('0b', '') for i in list(text)]
    result_list = []
    temp = []
    for i in range(len(text_list)):
        temp.append((text_list[i]))
        if i % 8 == 7:
            result_list.append(''.join(temp))
            temp = []
    result_list.append(add_zero_last(''.join(temp), 64))
    return result_list


def ip_switch(text, ip_choose):
    # use two ip_switch_matrix(s) to switch text
    # ip_choose is equal to 1 means make ip_switch to text by using ip_switch_matrix
    # ip_choose is equal to -1 means make inverse_ip_switch to text by using ip_switch_matrix
    ip_switch_matrix = [[58, 50, 42, 34, 26, 18, 10, 2],
                        [60, 52, 44, 36, 28, 20, 12, 4],
                        [62, 54, 46, 38, 30, 22, 14, 6],
                        [64, 56, 48, 40, 32, 24, 16, 8],
                        [57, 49, 41, 33, 25, 17, 9 , 1],
                        [59, 51, 43, 35, 27, 19, 11, 3],
                        [61, 53, 45, 37, 29, 21, 13, 5],
                        [63, 55, 47, 39, 31, 23, 15, 7]]
    ip_switch_matrix_1 = [[40, 8, 48, 16, 56, 24, 64, 32],
                          [39, 7, 47, 15, 55, 23, 63, 31],
                          [38, 6, 46, 14, 54, 22, 62, 30],
                          [37, 5, 45, 13, 53, 21, 61, 29],
                          [36, 4, 44, 12, 52, 20, 60, 28],
                          [35, 3, 43, 11, 51, 19, 59, 27],
                          [34, 2, 42, 10, 50, 18, 58, 26],
                          [33, 1, 41,  9, 49, 17, 57, 25]]
    result_text = ''
    if ip_choose == 1:
        result_text = switch_by_matrix(text, ip_switch_matrix)
    if ip_choose == -1:
        result_text = switch_by_matrix(text, ip_switch_matrix_1)
    return result_text


def xor(a, b):
    return a ^ b


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


def add_zero_last(source_text, number):
    # add zero in the last of the source_text until the length of it is equal to number
    if len(source_text) < number:
        result_text = source_text + '0' * (number - len(source_text))
    else:
        result_text = source_text
    return result_text


def test():
    # test des
    key1 = 'e'*14
    x = des(key1)
    print('\n\n')
    print(x.real_key)
    print(x.key)
    print(x.key_len)
    print(x.key_list)


if __name__ == '__main__':
    test()
