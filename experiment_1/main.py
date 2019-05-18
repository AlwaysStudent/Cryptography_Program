#!/opt/anaconda
# -*- coding = utf-8 -*-
from .Vigenere import vigenere


def main():
    # key = [2, 14, 3, 4, 18]
    c = 'Vvhqwvvrhmusgjgthkihtssejchlsfcbgvwcrlr' \
        'yqtfsvgahwkcuhwauglqhnslrljshbltspisprd' \
        'xljsveeGhlqwkasskuwepwqtwvspgoelkcqyfns' \
        'vwljsniqkgnrgybwlwgoviokhkazkqkxzgyhcec' \
        'meiujoqkwfwvefqhkijrclrlkbienqfrjljsdhg' \
        'rhlsfqtwlauqrhwdmwlgusgikkflryvcwvspgpm' \
        'lkassjvoqxeggveyggzmljcxxljsvpaivwikvrd' \
        'rygfrjljslveggveyggeiapuuisfpbtgnwwmucz' \
        'rvtwglrwugumnczvile'
    k = vigenere.vigenere('')
    vigenere.display(k.try_to_decode(c))


if __name__ == '__main__':
    main()
