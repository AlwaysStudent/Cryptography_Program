#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
from RSA import rsa


def main():
    m = 'abcdefghijklmnopqrstuvwxyz' * 20
    k1 = rsa.rsa(512)
    print('[info] The public key:\n', k1.create_public_key())
    print('[info] The private key:\n', k1.create_private_key())
    c = k1.encrypt(m)
    print('[info] The crypt text:\n', c)
    m1 = k1.decrypt(c)
    print('[info] The plain text:\n', m1)


if __name__ == '__main__':
    main()
