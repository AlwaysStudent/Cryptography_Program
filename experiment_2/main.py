#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
from DES import des


def main():
    key = des.create_des_key()
    d = des.des(key)
    m = 'A password, sometimes called a passcode, is a memorized secret used to confirm the identity of a user. ' \
        'Using the terminology of the NIST Digital Identity Guidelines, the secret is memorized by a party called ' \
        'the claimant while the party verifying the identity of the claimant is called the verifier.'
    c = d.encrypt(m)
    m1 = d.decrypt(c)
    print('[info] the created key:\n', key, '\n')
    print('[info] The plain text:\n', m, '\n')
    print('[info] The crypt text:\n', c, '\n')
    print('[info] The decrypted crypt text:\n', m1, '\n')


if __name__ == '__main__':
    main()
