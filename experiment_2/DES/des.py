#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import base64
import random


class des:
    """
    DES encryption algorithm
    """
    def __init__(self, key):
        """
        init des
        the list, key and text all using hex to store
        :param key:a hex key which has a 16 bits length
        """
        # check key length
        try:
            assert len(key) == 16
        except AssertionError:
            print('[info] key length is illegal')
            exit(0)
        else:
            pass
        self.key = key
        self.check_key()
        self.key_list = self.create_key_list()
        self.crypto_text = ''
        self.plain_text = ''

    def check_key(self):
        """
        check key with its check bits
        """
        key_list = group_text(self.key, 2)
        key_list_bin = [hex2bin(each) for each in key_list]
        for i in key_list_bin:
            temp = 0
            for j in i:
                temp = temp ^ int(j)
            try:
                assert temp == 0
            except AssertionError:
                print('[info] key is illegal')
                exit(0)
            else:
                pass

    def create_key_list(self):
        """
        use pc_switch_1 and pc_switch_2 to make key to a key list
        :return: key list
        """
        pc_switch_1 = [[57, 49, 41, 33, 25, 17, 9],
                       [1, 58, 50, 42, 34, 26, 18],
                       [10, 2, 59, 51, 43, 35, 27],
                       [19, 11, 3, 60, 52, 44, 36],
                       [63, 55, 47, 39, 31, 23, 15],
                       [7, 62, 54, 46, 38, 30, 22],
                       [14, 6, 61, 53, 45, 37, 29],
                       [21, 13, 5, 28, 20, 12, 4]]
        pc_switch_2 = [[14, 17, 11, 24, 1, 5],
                       [3, 28, 15, 6, 21, 10],
                       [23, 19, 12, 4, 26, 8],
                       [16, 7, 27, 20, 13, 2],
                       [41, 52, 31, 37, 47, 55],
                       [30, 40, 51, 45, 33, 48],
                       [44, 49, 39, 56, 34, 53],
                       [46, 42, 50, 36, 29, 32]]
        # use pc_switch_1 to get key_c and key_d
        key_after_pc_switch_1 = switch_by_matrix(hex2bin(self.key), pc_switch_1)
        key_c = key_after_pc_switch_1[:28]
        key_d = key_after_pc_switch_1[28:]

        # get 16 rounds key
        key_list = []
        for i in range(1, 17):
            key_c = bin_text_shift(key_c, i)
            key_d = bin_text_shift(key_d, i)
            temp_key = key_c + key_d
            each_round_key = switch_by_matrix(temp_key, pc_switch_2)
            key_list.append(bin2hex(each_round_key))
        return key_list

    def encrypt(self, plain_text):
        """
        using this function to encrypt the plain_text
        :param plain_text: plain_text
        :return:
        """
        # coding by 'utf-8'
        self.plain_text = encoding(plain_text)
        print(self.plain_text)
        # group plain_text into list
        # each element in list has 64 bits
        plain_text_list = group_text(self.plain_text, 16)
        plain_text_list = [add_zero_last(i, 16) for i in plain_text_list]
        crypto_text = ''
        # using run_coding to encode each piece of plain_text
        for each in range(len(plain_text_list)):
            temp = self.run(plain_text_list[each], 1)
            crypto_text += temp
        self.crypto_text = bin2hex(crypto_text)
        return self.crypto_text

    def decrypt(self, crypto_text):
        self.crypto_text = crypto_text
        # group plain_text into list
        # each element in list has 64 bits
        crypto_text_list = group_text(self.crypto_text, 16)
        print(crypto_text_list)
        plain_text = ''
        # using run_coding to encode each piece of plain_text
        for each in range(len(crypto_text_list)):
            temp = self.run(crypto_text_list[each], -1)
            plain_text += temp
        self.plain_text = bin2hex(plain_text)
        return self.plain_text

    def run(self, part_text, number):
        """
        run feistel net to crypto part_text
        :param part_text: a part of text in plain_text
        :param number: number is a flag to show that run for encrypt or decrypt
        :return: return encrypted part text
        """
        temp_text = add_zero_front(hex2bin(part_text), 64)
        # use ip_switch to switch the text by ip(1)
        atfer_ip_switch_text = ip_switch(temp_text, 1)
        # run feistel net with key_list to coding the text
        atfer_feistel_text = feistel_net(atfer_ip_switch_text, self.key_list, number)
        # use ip_switch to switch the text by ip(-1)
        final_text = ip_switch(atfer_feistel_text, -1)
        return final_text


def feistel_net(bin_text, key_list, number):
    """
    16 rounds feistel net to encrypt bin text
    :param bin_text: bin_text just use '0' and '1'
    :param key_list: key_list is create by create_key_list
    :param number: number is a flag to show that run for encrypting or decrypting
    :return: after feistel net text
    """
    temp_text = bin_text
    for i in list(range(0, 16))[::number]:
        print(i, '', end='')
        left_text = temp_text[:32]
        right_text = temp_text[32:]
        temp = function_f(right_text, key_list[i])
        temp_text = right_text + xor(left_text, temp, 32)
    print()
    return temp_text


def function_f(right_bin_text, key):
    """
    use e_switch, s-box and p_switch to switch text with key
    :param right_bin_text: right_bin_text
    :param key: key
    :return: after function_f text
    """
    e_switch = [[32, 1, 2, 3, 4, 5],
                [4, 5, 6, 7, 8, 9],
                [8, 9, 10, 11, 12, 13],
                [12, 13, 14, 15, 16, 17],
                [16, 17, 18, 19, 20, 21],
                [20, 21, 22, 23, 24, 25],
                [24, 25, 26, 27, 28, 29],
                [28, 29, 30, 31, 32, 1]]
    p_switch = [[16, 7, 20, 21, 29, 12, 28, 17],
                [1, 15, 23, 26, 5, 18, 31, 10],
                [2, 8, 24, 14, 32, 27, 3, 9],
                [19, 13, 30, 6, 22, 11, 4, 25]]
    temp_key = hex2bin(key)
    after_e_switch_text = switch_by_matrix(right_bin_text, e_switch)
    after_xor_key = xor(after_e_switch_text, temp_key, 48)
    after_s_box_text = s_box_switch(after_xor_key)
    after_p_switch_text = switch_by_matrix(after_s_box_text, p_switch)
    return after_p_switch_text


def s_box_switch(bin_text):
    s_box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
              [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
              [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
              [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

             [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
              [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
              [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
              [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

             [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
              [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
              [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
              [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

             [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
              [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
              [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
              [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

             [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
              [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
              [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
              [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

             [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
              [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
              [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
              [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

             [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
              [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
              [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
              [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

             [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
              [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
              [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
              [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    text_list = group_text(bin_text, 6)
    result_text = ''
    for i in range(len(text_list)):
        result_text += s_switch(text_list[i], s_box[i])
    return result_text


def s_switch(bin_text, part_s_box):
    a = int('0b' + (bin_text[0] + bin_text[5]), 2)
    b = int('0b' + bin_text[1:5], 2)
    result = part_s_box[a][b]
    return add_zero_front(bin(result).replace('0b', ''), 4)


def xor(bin_text_a, bin_text_b, length):
    temp_a = int(bin_text_a, 2)
    temp_b = int(bin_text_b, 2)
    temp = bin(temp_a ^ temp_b).replace('0b', '')
    return add_zero_front(temp, length)


def ip_switch(bin_text, ip_choose):
    """
    use two ip_switch_matrix(s) to switch text
    :param text: bin_text
    :param ip_choose:
    ip_choose is equal to 1 means make ip_switch to text by using ip_switch_matrix
    ip_choose is equal to -1 means make inverse_ip_switch to text by using ip_switch_matrix
    :return:
    """
    # ip_choose is equal to 1 means make ip_switch to text by using ip_switch_matrix
    # ip_choose is equal to -1 means make inverse_ip_switch to text by using ip_switch_matrix
    ip_switch_matrix = [[58, 50, 42, 34, 26, 18, 10, 2],
                        [60, 52, 44, 36, 28, 20, 12, 4],
                        [62, 54, 46, 38, 30, 22, 14, 6],
                        [64, 56, 48, 40, 32, 24, 16, 8],
                        [57, 49, 41, 33, 25, 17, 9, 1],
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
                          [33, 1, 41, 9, 49, 17, 57, 25]]
    result_text = ''
    if ip_choose == 1:
        result_text = switch_by_matrix(bin_text, ip_switch_matrix)
    if ip_choose == -1:
        result_text = switch_by_matrix(bin_text, ip_switch_matrix_1)
    return result_text


def encoding(text):
    temp1 = base64.b64encode(text.encode('utf-8'))
    temp2 = base64.b16encode(temp1)
    return temp2.decode('utf-8')


def add_zero_front(bin_text, number):
    # add zero in the front of the source_text until the length of it is equal to number
    if len(bin_text) < number:
        result_text = '0' * (number - len(bin_text)) + bin_text
    else:
        result_text = bin_text
    return result_text


def add_zero_last(bin_text, number):
    # add zero in the last of the source_text until the length of it is equal to number
    if len(bin_text) < number:
        result_text = bin_text + '0' * (number - len(bin_text))
    else:
        result_text = bin_text
    return result_text


def bin_text_shift(bin_text, times):
    """
    shift bin_text to create key list
    :param bin_text:
    :param times:
    :return:
    """
    time_one_list = [1, 2, 9, 16]
    if times in time_one_list:
        temp = bin_text[1:] + bin_text[:1]
    else:
        temp = bin_text[2:] + bin_text[:2]
    return temp


def switch_by_matrix(bin_text, switch_matrix):
    """
    switch bin_text by using switch_matrix
    :param bin_text: bin_text which just have '0' and '1' without '0b'
    :param switch_matrix: the switching rules
    :return: after switching bin_text
    """
    result_bin_text = ''
    for i in switch_matrix:
        for j in i:
            result_bin_text += bin_text[j - 1]
    return result_bin_text


def group_text(text, number):
    """
    split the text into list which has number of character
    :param text:hex or bin
    :param number:character number of each piece
    :return:list of split
    """
    # check the length of text and number legal or not
    result_list = []
    temp = ''
    for i in range(len(text)):
        temp += text[i]
        if (i + 1) % number == 0:
            result_list.append(temp)
            temp = ''
    if len(temp) != 0:
        result_list.append(temp)
    return result_list


def hex2bin(hex_text):
    """
    change hex_text to bin_text
    :param hex_text: hex_text which just have '0' to 'f' without '0x'
    :return: bin_text which just have '0' and '1' without '0b'
    """
    return bin(int(hex_text, 16)).replace('0b', '')


def bin2hex(bin_text):
    """
    change bin_text to hex_text
    :param bin_text which just have '0' and '1' without '0b'
    :return: hex_text: hex_text which just have '0' to 'f' without '0x'
    """
    return hex(int(bin_text, 2)).replace('0x', '')


def create_des_key():
    """
    create des key by package random
    :return: return created legal des key
    """
    temp_key = '1'
    for i in range(55):
        temp_key += random.choice(['0', '1'])
    key = ''
    temp = 0
    for i in range(len(temp_key)):
        key += temp_key[i]
        temp = temp ^ int(temp_key[i])
        if (i + 1) % 7 == 0:
            key += str(temp)
            temp = 0
    return bin2hex(key)


def test():
    key = 'f'*16
    x = des(key)
    m = '111111'
    c = '22a4794110fcf47a'
    print(x.encrypt(m))
    print(x.decrypt(c))


if __name__ == '__main__':
    test()
