#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import base64


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
        key_atfer_pc_switch_1 = switch_by_matrix(hex2bin(self.key), pc_switch_1)
        key_c = key_atfer_pc_switch_1[:28]
        key_d = key_atfer_pc_switch_1[28:]

        # get 16 rounds key
        key_list = []
        for i in range(1, 17):
            key_c = bin_text_shift(key_c)
            each_round_key



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
    try:
        assert len(text) % number == 0
    except AssertionError:
        print("[info] wrong split input")
        exit(0)
    else:
        pass
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
    return hex(int(bin_text, 2)).replace('0b', '')
