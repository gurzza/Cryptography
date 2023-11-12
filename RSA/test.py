import time
import main
import rsa

print('ExEu algo:')
a = 11
n = 31
a_reverse = main.ExEu(a, n)[1]
print('a =', a, ', n =', n, ', a^-1 =', a_reverse)
print('CHECK is a*(a^-1) mod n = 1: ', a * a_reverse % n == 1)
print('_________________________________')

print('a^b mod n = ...')
a = 121
b = 15
n = 13
res = main.ModPow(a, b, n)
print('CHECK is ModPow(a, b, n) == pow(a, b, n):', res == pow(a, b, n))
print('___________________________')

print('Generating prime numbers')
prime = main.GenPrime(1024)
print('Prime number:', prime)
print('____________________________')

print('Primes checker')
p1 = 121
p2 = 103
print('Answer for', p1, main.IsPrime(p1))
print('Answer for', p2, main.IsPrime(p2))
print('_____________________________')


start = time.time()
print('Generate n, e, d, p, q')
n, e, d, p, q = main.Gen(2048)
print('Generated numbers n =', n, '\ne =', e, '\nd =', d, '\np =', p, '\nq =', q)
print('Checking conditions\nIsPrime(p), IsPrime(q):', main.IsPrime(p), main.IsPrime(q))
print('n == p*q', n == p*q)
print('ExEu(e, (p-1)*(q-1)) == d:', main.ExEu(e, (p-1)*(q-1))[1] == d)
print('e*d mod fi(n) == 1:', e*d % (p-1)*(q-1) == 1)
print('(e, p-1) == (e, q-1) == 1:', main.GCD(e, p-1) == 1, main.GCD(e, q-1) == 1)
print('____________________________')



print('Checking Enc&Dec:')
message = 'Hello, World!'

print('Message:', message)
encrypted = main.MessageEnc(message, n, e)
print('Encrypted: ', encrypted)
decryted = main.MessageDec(encrypted, p, q, d, n)
print('Message == decrypted:', decryted == message)

end = time.time() - start
print('Work time:', end)


