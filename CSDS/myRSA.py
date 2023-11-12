import random


# right->left
def GCD(a, b):
    while b:
        r = a % b
        a = b
        b = r
    return a



def ModPow(x, degree, n):
    # left <-right
    u, v = 1, x
    degree_bin = bin(degree)[2:][::-1]  # reverse

    for el in degree_bin:
        if int(el) & 1:
            u = (u * v) % n
        v = (v * v) % n

    return u


# Якоби: https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB_%D0%AF%D0%BA%D0%BE%D0%B1%D0%B8
# def jacob(a, n):
#     if GCD(a, n) != 1:
#         return 0
#     r = 1
#
#     #if a < 0:
#     #    a = -a
#     #    if n % 4 == 3:
#     #        r = -r
#
#     while True:
#         t = 0
#         while not a & 1:  # a % 2 == 0
#             t += 1
#             a >>= 1
#         if not t & 1:  # t % 2 != 0
#             n_mod = n % 8
#             if n_mod == 3 or n_mod == 5:
#                 r = -r
#
#         if a % 4 == n % 4 == 3:
#             r = -r
#
#         c = a
#         b = c
#         a = b % c
#
#         if a == 0:
#             return r

# https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%B2%D1%8B%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D0%B0_%D0%AF%D0%BA%D0%BE%D0%B1%D0%B8
def jacob(a, n):
    r = 1

    while True:
        if a < 0:
            a = -a
            r *= -1 if ((n - 1) >> 1) % 2 == 1 else 1
            continue
        if a % 2 == 0:
            a >>= 1
            r *= -1 if ((n * n - 1) >> 3) % 2 == 1 else 1
            continue
        if a == 1:
            return r
        if a < n:
            t = a
            a = n
            n = t
            r *= -1 if (((a - 1) * (n - 1)) >> 2) % 2 == 1 else 1
            continue
        a = a % n


def IsPrime(n):
    round = 100

    if n % 2 == 0:
        return False

    # F: a^(n-1) mod n = 1 => ok
    for _ in range(round):
        #flag = False
        a = random.randrange(1, n - 1)
        if ExEu(a, n)[0] != 1:
            return False
        if ModPow(a, n - 1, n) != 1:
            return False

    ##########################################
    # Miller-Rabin

    d = n - 1
    s = 0
    # n-1 = d*2^s
    while not d & 1:  # d % 2 == 0
        # d = b*q + r
        d >>= 1
        s += 1

    def MRCond(v, n, s):
        if v % n == 1:
            return True
        for i in range(s):
            if v % n == n - 1:
                return True
            v = ModPow(v, 2, n)
        return False

    for _ in range(round):
        a = random.randrange(1, n - 1)
        if ExEu(a, n)[0] != 1:
            return False
        v = ModPow(a, d, n)
        if not MRCond(v, n, s):
            return False

    ###############################
    # print(n)
    # Solovay–Strassen
    degree = (n - 1) >> 1
    for _ in range(round):
        a = random.randint(2, n - 1)
        if GCD(a, n) != 1:
            return False
        a_degree = ModPow(a, degree, n)
        a_jacob = jacob(a, n) % n
        if a_degree != a_jacob:
            return False

    return True


def GenPrime(l):
    flag = False
    while not flag:
        mn = pow(2, l - 1) + 1
        mx = pow(2, l) - 1
        num = random.randint(mn, mx)
        flag = IsPrime(num)

    return num


def ExEu(a, b):
    q, r0, r1 = 0, b, a
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    if y0 < 0:
        y0 = (y0 + b) % b
    return r0, y0  # gcd, a^-1


# def Enc(x, e, n):
#     return ModPow(x, e, n)


def MessageEnc(message, n, e):
    #encrypt = []
    #for letter in message:
    cipher = ModPow(message, e, n)
    return cipher


# def Dec(x, d, n):
#    return ModPow(x, d, n)

def MessageDec(message, p, q, d, n):
    q_ = ExEu(q, p)[1]

    #decrypt = []
    #for letter in message:
    x1 = ModPow(message, d % (p - 1), p)
    x2 = ModPow(message, d % (q - 1), q)
    plaintext = (x2 + q * (q_ * (x1 - x2) % p)) % n


    return plaintext


def Gen(l): # l = 2048
    e = 65537

    while True:
        p = GenPrime(l >> 1)
        q = GenPrime(l >> 1)

        if p == q:
            continue
        if GCD(e, p - 1) != 1:
            continue
        if GCD(e, q - 1) != 1:
            continue
        break

    n = p * q
    fi = (p - 1) * (q - 1)
    d = ExEu(e, fi)[1]
    # print("Check: ", e*d % fi)
    return n, e, d, p, q


# l = 2048
# n, e, d = Gen(l)
# #message = 'Hello'
# print('n =', n)
# print('e =', e)
# print('d =', d)


if __name__ == '__main__':
    l = 2048
    message = 'Hello'
    n, e, d, p, q = Gen(l)
    enc = MessageEnc(message, n, e)
    dec = MessageDec(enc, n, d)
    print(enc)
    print(dec)

    # b = Gen(l)
    # print(17, b, n)
    # print(ModPow(17, b, n))
