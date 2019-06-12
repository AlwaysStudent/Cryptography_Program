#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
from DES import des


def main():
    key = des.create_des_key()
    key = 'f' * 16
    d = des.des(key)
    m = 'abcdefg' * 10
    c = d.encrypt(m)
    c = 'c165c9f1b31055a639a8febf777017c30ff6b194ca5ba916a50d9c912e50e623d595b5294fd2e845f59ba5bfa030e5cab1339f3d0a4b61d0c165c9f1b31055a6559723e7fd992fa'
    print(type(m))
    m1 = d.decrypt(c)
    print(key)
    print('[info] The plain text:\n', m)
    print('[info] The crypt text:\n', c)
    print('[info] The decrypted crypt text:\n', m1)


if __name__ == '__main__':
    main()
