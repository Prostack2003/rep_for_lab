import random
from sympy import isprime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y

    if temp_phi == 1:
        return d + phi
    else:
        return None  # Обратного не существует


def generate_prime(bits):
    while True:
        num = random.randrange(2**(bits-1), 2**bits)
        if isprime(num):
            return num

def generate_keypair(bits):
    while True:
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)
        if p != q:
            n = p * q
            phi = (p - 1) * (q - 1)

            e = random.randrange(1, phi)
            g = gcd(e, phi)
            while g != 1:
                e = random.randrange(1, phi)
                g = gcd(e, phi)

            d = mod_inverse(e, phi)
            if d is not None:
                return ((e, n), (d, n))


def encrypt(public_key, plaintext):
    key, n = public_key
    cipher = [(pow(ord(char), key, n)) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    key, n = private_key
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

# Пример использования
if __name__ == "__main__":
    print("Генерация ключей...")
    bits = 16  # Размер ключа в битах
    public_key, private_key = generate_keypair(bits)
    print("Открытый ключ:", public_key)
    print("Закрытый ключ:", private_key)

    message = "Hello RSA!"
    print("\nСообщение для шифрования:", message)
    encrypted_msg = encrypt(public_key, message)
    print("Зашифрованное сообщение:", encrypted_msg)

    decrypted_msg = decrypt(private_key, encrypted_msg)
    print("Расшифрованное сообщение:", decrypted_msg)
