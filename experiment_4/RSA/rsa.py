#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
import random


class rsa:
    """
    RSA encryption algorithm
    """
    def __init__(self, bit_length):
        self.bit_length = bit_length
        self.p = 0
        self.q = 0
        self.public_key = self.create_public_key()
        self.private_key = self.create_private_key()

    def create_public_key(self):


    def create_private_key(self):
        pass
