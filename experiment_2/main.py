#!/opt/anaconda/python3
# -*- coding=utf-8 -*-
from DES import des


def main():
    key = 'f' * 16
    x = des.des(key)
    m = 'abcdefghijklmnopqrstuvwxyz' * 10
    c = 'bb6bf1593cf73c70c1673e5be89590cc32e17fdd754986fdd86f02077756939b2b7a3366f394c370423ce8914d6614d3d7fec14f0a2694ab7fced134d0b47cfc10560b1726d3f5b96535434ff055c583a59b73fdfa30724e9f924975cfc0c9a971eef488169229acbb6bf1593cf73c70c1673e5be89590cc32e17fdd754986fdd86f02077756939b2b7a3366f394c370423ce8914d6614d3d7fec14f0a2694ab7fced134d0b47cfc10560b1726d3f5b96535434ff055c583a59b73fdfa30724e9f924975cfc0c9a971eef488169229acbb6bf1593cf73c70c1673e5be89590cc32e17fdd754986fdd86f02077756939b2b7a3366f394c370423ce8914d6614d347489a56a69c9690'
    print(des.bin2hex(des.str2num(m)))
    print(x.encrypt(m))
    print(x.decrypt(c))


if __name__ == '__main__':
    main()
