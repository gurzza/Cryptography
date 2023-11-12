import math
import random
import numpy as np


def modify_input(text, alphabet, key, operation, cipher=""):
    return text.upper().strip().replace(' ', ''), alphabet.upper().strip().replace(' ', ''), \
           key.upper().strip().replace(' ', ''), operation.upper().strip().replace(' ', ''), cipher.upper().strip()


def isinalphabet(alphabet, word):  # are all letters in the alphabet?
    status = True
    for i in word:
        if i not in alphabet:
            status = False
            break

    return status


def check_parameters(text, alphabet, key, operation, cipher):  # are parameters empty?
    status = True
    if text == '' or alphabet == '' or key == '' or operation not in ['DECRYPT', 'ENCRYPT']:
        status = False

    elif cipher not in ['CAESAR CIPHER', 'AFFINE CIPHER', 'SIMPLE REPLACEMENT CIPHER', 'HILL CIPHER',
                        'PERMUTATION CIPHER', 'VIGENERE CIPHER']:
        status = False

    elif not isinalphabet(alphabet, text) or not isinalphabet(alphabet, key):
        status = False

    return status


def letters(word):
    status = True
    for i in word:
        if not i.isalpha():
            status = False
            break

    return status


def isrepeat(word):
    status = True

    for letter in word:
        num = word.count(letter)
        if num != 1:
            status = False
            break
    return status


#########################


def co_prime(a, m):
    while m:
        r = a % m
        a = m
        m = r
    return a


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0

    while a != 0:
        q = b // a
        r = b % a
        m = x - u * q
        n = y - v * q
        b = a
        a = r
        x = u
        y = v
        u = m
        v = n
    gcd = b
    return gcd, x


def mod_inv(a, m):
    if a < 0:
        a += m

    return egcd(a, m)  # gcd, x


########################


def caesar_cipher(text, alphabet, key, operation):
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'CAESAR CIPHER'):
        ans = 'ERROR! Check parameters!'

    elif len(key) != 1:
        ans = 'ERROR! Check your key/alphabet/text!'

    if ans == '':
        l_alpha = len(alphabet)
        shift = alphabet.index(key)

        if operation == 'ENCRYPT':
            for i in text:
                pos = alphabet.index(i)
                new_pos = (pos + shift) % l_alpha
                ans += alphabet[new_pos]

        elif operation == 'DECRYPT':
            for i in text:
                pos = alphabet.index(i)
                new_pos = (pos - shift) % l_alpha
                ans += alphabet[new_pos]

    return ans


# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# print(caesar_cipher('ZABCD', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1', '5', 'DECRYPT'))


def affine_cipher(text, alphabet, key, operation):
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'AFFINE CIPHER'):
        ans = 'ERROR! Check parameters!'

    elif len(key) != 2:
        ans = 'ERROR! Check your key/alphabet/text!'

    if ans == '':
        a = alphabet.index(key[0])
        b = alphabet.index(key[1])
        l_alpha = len(alphabet)

        if (co_prime(a, l_alpha)) != 1:
            ans = 'ERROR! NUMBERS IN KEY (AFFINE CIPHER) AREN\'T COPRIME NUMBERS'

        elif operation == 'ENCRYPT':
            for i in text:
                x = alphabet.index(i)
                new_pos = (a * x + b) % l_alpha
                ans += alphabet[new_pos]

        elif operation == 'DECRYPT':
            gcd, x = mod_inv(a, l_alpha)
            if gcd != 1:
                ans = 'ERROR! INVERSE NUMBER ISN\'T EXIST!'
            else:
                a_inv = x % l_alpha
                for i in text:
                    y = alphabet.index(i)
                    new_pos = (a_inv * (y - b)) % l_alpha
                    ans += alphabet[new_pos]

    return ans


#print(affine_cipher('СЕКРЕТНОГО', 'АБВГЯ', 'ПЮ', 'ENCRYPT'))


def simple_replacement_cipher(text, alphabet, key, operation):
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'SIMPLE REPLACEMENT CIPHER'):
        ans = 'ERROR! Check parameters!'

    if len(key) != len(alphabet) or not isrepeat(key):
        ans = 'ERROR! Incorrect key!'

    if ans == '':
        if operation == 'ENCRYPT':
            for i in text:
                ans += key[alphabet.index(i)]

        else:
            for i in text:
                ans += alphabet[key.index(i)]

    return ans


# print(simple_replacement_cipher('XLBTF', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'XLBTFSDGWOREPCZVHNQYUAMIJK', 'DECRYPT'))


def hill_cipher(text, alphabet, key, operation):
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'HILL CIPHER'):
        ans = 'ERROR! Check parameters!'

    elif len(key) != 4 or not letters(key):
        ans = 'ERROR! Check your key/alphabet/text!'

    if ans == '':
        key_matrix = np.array([[alphabet.index(key[0]), alphabet.index(key[1])],
                               [alphabet.index(key[2]), alphabet.index(key[3])]], dtype=np.int64)
        l_alpha = len(alphabet)

        det = key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]
        if det == 0:
            ans = 'ERROR! DETERMINANT IN HILL CIPHER IS ZERO'

        else:
            if co_prime(abs(det), l_alpha) != 1:
                ans = 'ERROR! KEY AND ALPHABET LENGTH AREN\'T COPRIME NUMBERS IN HILL CIPHER'

            else:
                if len(text) % 2 == 1:
                    text += alphabet[random.randint(0, l_alpha-1)]
                    # last_letter = True

                blocks = len(text) // 2
                j = 0

                if operation == 'ENCRYPT':
                    for i in range(blocks):
                        text_vector = np.array([alphabet.index(text[j]), alphabet.index(text[j + 1])])
                        cipher_text = np.dot(text_vector, key_matrix) % l_alpha
                        ans += alphabet[cipher_text[0]] + alphabet[cipher_text[1]]
                        j += 2
                ####
                else:
                    gcd, x = mod_inv(det, l_alpha)
                    if gcd != 1:
                        ans = 'ERROR! INVERSE NUMBER ISN\'T EXIST!'
                    else:
                        multiplier = x % l_alpha

                    if ans == '':
                        inverse_key_matrix = np.array([[key_matrix[1][1], (-key_matrix[0][1] + l_alpha)],
                                                       [(-key_matrix[1][0] + l_alpha), key_matrix[0][0]]],
                                                      dtype=np.int64)

                        for i in range(2):
                            for j in range(2):
                                inverse_key_matrix[i][j] = (inverse_key_matrix[i][j] * multiplier) % l_alpha

                        j = 0
                        for i in range(blocks):
                            text_vector = np.array([alphabet.index(text[j]), alphabet.index(text[j + 1])])
                            cipher_text = np.dot(text_vector, inverse_key_matrix) % l_alpha
                            ans += alphabet[cipher_text[0]] + alphabet[cipher_text[1]]
                            j += 2

    return ans


# print(hill_cipher('НЕ ДОВЕРЯЙ ВИКТОРУ', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'АГБВ', 'ENCRYPT'))


def permutation_cipher(text, alphabet, key, operation): #перестановки
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'PERMUTATION CIPHER'):
        ans = 'ERROR! Check parameters!'

    elif len(key) > len(alphabet):
        ans = 'ERROR! Check your key/alphabet/text!'

    if ans == '':
        key_letter = [alphabet.index(i) for i in key]
        order = [0] * len(key)
        l_alpha = len(alphabet)

        if len(text) % len(key) != 0:  # add last letters
            symb = alphabet[random.randint(0, l_alpha-1)]
            diff = len(key) - (len(text) % len(key))
            text += symb * diff

        ans = [' '] * len(text)
        for i in range(len(key)):  # sort keys
            pos = -1
            num = len(alphabet) + 5
            for j in range(len(key)):
                if num > key_letter[j]:
                    num = key_letter[j]
                    pos = j
            order[pos] = i
            key_letter[pos] = len(alphabet) + 5
        blocks = len(text) // len(key)

        if operation == 'ENCRYPT':
            for i in range(blocks):
                k = 0
                for j in range(len(key)):
                    ans[i * len(key) + order[j]] = text[i * len(key) + k]
                    k += 1
        ##############
        else:
            for i in range(blocks):
                k = 0
                for j in range(len(key)):
                    ans[i * len(key) + k] = text[i * len(key) + order[j]]
                    k += 1
        ans = ''.join(ans)

    return ans


# print(permutation_cipher('НЕДОВЕРЯЙВИКТОРУСР', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'ПРИВЕТ', 'ENCRYPT'))


def vigenere_cipher(text, alphabet, key, operation):
    ans = ''
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher="")
    if not check_parameters(text, alphabet, key, operation, 'VIGENERE CIPHER'):
        ans = 'ERROR! Check parameters!'

    if ans == '':
        l_alpha = len(alphabet)
        # make key longer
        full_keys = len(text) // len(key)
        rest = len(text) % len(key)
        key = key * full_keys + key[:rest]

        if operation == 'ENCRYPT':
            for i in range(len(text)):
                ans += alphabet[(alphabet.index(text[i]) + alphabet.index(key[i])) % l_alpha]

        else:
            for i in range(len(text)):
                ans += alphabet[(alphabet.index(text[i]) - alphabet.index(key[i])) % l_alpha]
        # ans_str = ''.join(ans)

    return ans

# print(vigenere_cipher('НЕДОВЕРЯЙВИКТОРУ', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'КЛЮЧ', 'ENCRYPT'))
# ЦЩЗПЕЩНУЙНЩЧЙЬИ
# ЦЩЗПЕЩНУЙЬЩЧЙЬИ
# ЦЩЗПЕЩНУЙНФЧЙЬИ


if __name__ == '__main__':
    # Read&Check
    ans = ''
    alphabet = open('alphabet.txt', 'r', encoding='utf-8').read()
    text = open('text.txt', 'r', encoding='utf-8').read()
    key = open('key.txt', 'r', encoding='utf-8').read()
    operation = open('operation.txt', 'r', encoding='utf-8').read()
    cipher = open('cipher.txt', 'r').read()
    text, alphabet, key, operation, cipher = modify_input(text, alphabet, key, operation, cipher)

    if not check_parameters(text, alphabet, key, operation, cipher): #text, alphabet, key, operation, cipher
        ans = 'ERROR! Check your parameters!'

    #if not isinalphabet(alphabet, text):
    #    ans = 'ERROR! Your alphabet doesn\'t contain such letter(-s) that is(are) in your text!'

    if ans == '':
        print('Alphabet: ', alphabet, '\nText: ', text, '\nKey: ', key, '\nOperation: ', operation, '\nCipher: ',
              cipher)

        # __ Caesar
        '''
        if cipher == 'CAESAR CIPHER' and len(key) != 1:
            raise Exception('ERROR! The key in the Caesar cipher should have length equal 1!')
        if cipher == 'CAESAR CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in the Caesar cipher should be in your alphabet!')
        if cipher == 'CAESAR CIPHER' and not letters(key):
            raise Exception('ERROR! The key in the Caesar cipher should contain just letters!')


        # __Affine

        if cipher == 'AFFINE CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in affine cipher should be in your alphabet!')
        if cipher == 'AFFINE CIPHER' and len(key) != 2:
            raise Exception('ERROR! The key in affine cipher should length equal 2!')
        if cipher == 'AFFINE CIPHER' and not letters(key):
            raise Exception('ERROR! The key in affine cipher should contain just letters!')
        



         __SIMPLE REPLACEMENT CIPHER
        if cipher == 'SIMPLE REPLACEMENT CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in the simple replacement cipher should be in your alphabet!')
        if cipher == 'SIMPLE REPLACEMENT CIPHER' and not isrepeat(key):
            raise Exception('ERROR! The key in thesimple replacement cipher contains repeat!')
        if cipher == 'SIMPLE REPLACEMENT CIPHER' and not letters(key):
            raise Exception('ERROR! The key in the simple replacement cipher should contain just letters!')


        # __HILL

        if cipher == 'HILL CIPHER' and len(key) != 4:
            raise Exception('ERROR! The key in the Hill cipher should have length equal 4!')
        if cipher == 'HILL CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in the Hill cipher should contain letters from alphabet')
        if cipher == 'HILL CIPHER' and not letters(key):
            raise Exception('ERROR! The key in the Hill cipher should contain just letters!')


        # __PERMUTATION CIPHER

        if cipher == 'PERMUTATION CIPHER' and len(key) > len(alphabet):
            raise Exception('ERROR! The key in the permutation cipher should have length <= length alphabet')
        if cipher == 'PERMUTATION CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in the permutation cipher should contain letters from alphabet')
        if cipher == 'PERMUTATION CIPHER' and not letters(key):
            raise Exception('ERROR! The key in the permutation cipher should contain just letters!')


        # __VIGENERE
        
        if cipher == 'VIGENERE CIPHER' and not isinalphabet(alphabet, key):
            raise Exception('ERROR! The key in the Vigenere cipher should contain letters from alphabet!')
        if cipher == 'VIGENERE CIPHER' and not letters(key):
            raise Exception('ERROR! The key in the Vigenere cipher should contain just letters!')
        '''

        # __run__

        if cipher == 'CAESAR CIPHER':
            ans = caesar_cipher(text, alphabet, key, operation)
        elif cipher == 'AFFINE CIPHER':
            ans = affine_cipher(text, alphabet, key, operation)
        elif cipher == 'SIMPLE REPLACEMENT CIPHER':
            ans = simple_replacement_cipher(text, alphabet, key, operation)
        elif cipher == 'HILL CIPHER':
            ans = hill_cipher(text, alphabet, key, operation)
        elif cipher == 'PERMUTATION CIPHER':  # HERE
            ans = permutation_cipher(text, alphabet, key, operation)
        elif cipher == 'VIGENERE CIPHER':
            ans = vigenere_cipher(text, alphabet, key, operation)

    if operation == 'ENCRYPT':
        open('encrypt.txt', 'w', encoding='utf-8').write(ans)
    else:
        open('decrypt.txt', 'w', encoding='utf-8').write(ans)
