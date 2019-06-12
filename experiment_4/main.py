#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
from RSA import rsa


def main():
    m = 'A password, sometimes called a passcode, is a memorized secret used to confirm the identity of a user. ' \
        'Using the terminology of the NIST Digital Identity Guidelines, the secret is memorized by a party called ' \
        'the claimant while the party verifying the identity of the claimant is called the verifier.'
    k1 = rsa.rsa(512)
    c = k1.encrypt(m)
    m1 = k1.decrypt(c)
    print('[info] The public key pair:\n', k1.create_public_key(), '\n')
    print('[info] The private key pair:\n', k1.create_private_key(), '\n')
    print('[info] The plain text:\n', m, '\n')
    print('[info] The crypt text:\n', c, '\n')
    print('[info] The decrypted crypt text:\n', m1, '\n')


if __name__ == '__main__':
    main()
