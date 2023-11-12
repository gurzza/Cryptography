from random import sample, randint

import numpy as np

from main import caesar_cipher, affine_cipher, simple_replacement_cipher, hill_cipher, permutation_cipher, \
    vigenere_cipher


def generate_alpha():
    lst = np.arange(65, 91)  # english alpha
    lst = [chr(i) for i in lst]
    lst = sample(lst, randint(4, 26))
    return lst


def generate_text(alphabet):
    text = sample(alphabet, randint(4, len(alphabet)))
    return "".join(text)


def generate_cipher():
    ciphers = ['CAESAR CIPHER', 'AFFINE CIPHER', 'SIMPLE REPLACEMENT CIPHER', 'HILL CIPHER',
               'PERMUTATION CIPHER', 'VIGENERE CIPHER']
    return ciphers[randint(0, len(ciphers) - 1)]


def generate_operation():
    oper = ['DECRYPT', 'ENCRYPT']
    return oper[randint(0, 1)]


def run(text, alphabet, operation, cipher):
    key = ''
    ans = ''
    if cipher == 'CAESAR CIPHER':
        key = "".join(sample(alphabet, 1))
        print('Key:', key)
        ans = caesar_cipher(text, alphabet, key, operation)

    elif cipher == 'AFFINE CIPHER':
        key = "".join(sample(alphabet, 2))
        print('Key:', key)
        ans = affine_cipher(text, alphabet, key, operation)

    elif cipher == 'SIMPLE REPLACEMENT CIPHER':
        key = "".join(sample(alphabet, len(alphabet)))
        print('Key:', key)
        ans = simple_replacement_cipher(text, alphabet, key, operation)

    elif cipher == 'HILL CIPHER':
        key = "".join(sample(alphabet, 4))
        ans = hill_cipher(text, alphabet, key, operation)

    elif cipher == 'PERMUTATION CIPHER':
        key = "".join(sample(alphabet, randint(3, len(alphabet))))
        print('Key:', key)
        ans = permutation_cipher(text, alphabet, key, operation)

    elif cipher == 'VIGENERE CIPHER':
        key = "".join(sample(alphabet, randint(3, len(alphabet))))
        ans = vigenere_cipher(text, alphabet, key, operation)

    return ans

for i in range(10):
    alphabet = "".join(sorted(generate_alpha()))
    text = generate_text(alphabet)
    cipher = generate_cipher()
    operation = generate_operation()
    print('Text: ', text)
    print('Alphabet: ', alphabet)
    print('Cipher: ', cipher)
    print('Operation: ', operation)
    # print('Key: ', key)
    ans = run(text, alphabet, operation, cipher)
    #ans = run('RYDB', 'BDRY', 'ENCRYPT', 'PERMUTATION CIPHER')
    print('Answer: ', ans)
    print()