
"""
ЛАБОРАТОРНАЯ РАБОТА №1
Тема: Применение алгоритмов шифрования

Студент: Быканов Дмитрий Константинович

Часть 1: Симметричное шифрование (алгоритм XOR)
Часть 2: Асимметричное шифрование (RSA)
"""

# ============================================================
# ЧАСТЬ 1: СИММЕТРИЧНОЕ ШИФРОВАНИЕ (XOR)
# ============================================================

class XORCipher:
    """Симметричное шифрование XOR"""
    
    def __init__(self, key=0xAA):
        self.key = key
    
    def encrypt(self, text):
        """Шифрование текста"""
        if isinstance(text, str):
            text = text.encode('utf-8')
        
        result = bytearray()
        for byte in text:
            result.append(byte ^ self.key)
        return result
    
    def decrypt(self, data):
        """Дешифрование (XOR симметричен)"""
        if isinstance(data, bytes):
            result = bytearray()
            for byte in data:
                result.append(byte ^ self.key)
            return result
        return data
    
    def encrypt_text(self, text):
        """Шифрование текста в hex строку"""
        return self.encrypt(text).hex().upper()
    
    def decrypt_text(self, hex_string):
        """Дешифрование из hex строки"""
        data = bytes.fromhex(hex_string)
        decrypted = self.decrypt(data)
        return decrypted.decode('utf-8', errors='replace')


# ============================================================
# ЧАСТЬ 2: АСИММЕТРИЧНОЕ ШИФРОВАНИЕ RSA
# ============================================================

class RSACipher:
    """Алгоритм RSA"""
    
    def __init__(self, p, q, e, d):
        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.n = p * q
        self.phi = (p-1) * (q-1)
    
    def encrypt(self, m):
        """Шифрование сообщения m: c = m^e mod n"""
        return pow(m, self.e, self.n)
    
    def decrypt(self, c):
        """Дешифрование сообщения c: m = c^d mod n"""
        return pow(c, self.d, self.n)
    
    def get_public_key(self):
        return (self.n, self.e)
    
    def get_private_key(self):
        return (self.n, self.d)


# ============================================================
# ОСНОВНАЯ ПРОГРАММА
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №1")
    print("Студент: Быканов Дмитрий Константинович")
    print("=" * 70)
    
    # ЧАСТЬ 1
    print("\n" + "=" * 70)
    print("ЧАСТЬ 1: Симметричное шифрование (алгоритм XOR)")
    print("=" * 70)
    
    my_full_name = "БЫКАНОВ ДМИТРИЙ КОНСТАНТИНОВИЧ"
    
    print(f"\nИсходные данные (ФИО): {my_full_name}")
    
    xor_cipher = XORCipher(key=0xAA)
    encrypted_hex = xor_cipher.encrypt_text(my_full_name)
    print(f"\nЗашифрованное сообщение (HEX):")
    print(f"  {encrypted_hex}")
    
    decrypted_text = xor_cipher.decrypt_text(encrypted_hex)
    print(f"\nРасшифрованное сообщение:")
    print(f"  {decrypted_text}")
    
    print()
    if decrypted_text == my_full_name:
        print("РЕЗУЛЬТАТ: Расшифрование выполнено УСПЕШНО")
    else:
        print("РЕЗУЛЬТАТ: ОШИБКА расшифрования")
    
    # ЧАСТЬ 2
    print("\n" + "=" * 70)
    print("ЧАСТЬ 2: Асимметричное шифрование (RSA)")
    print("=" * 70)
    
    p = 3
    q = 11
    e = 7
    d = 3
    n = p * q
    
    print(f"\nЗаданные параметры RSA:")
    print(f"  p = {p}, q = {q}")
    print(f"  n = {n}")
    print(f"  e = {e}, d = {d}")
    print(f"  φ(n) = {(p-1)*(q-1)}")
    
    rsa = RSACipher(p, q, e, d)
    messages = [8, 13, 25]
    
    print(f"\nИсходные сообщения: {messages}")
    print("\nРезультаты шифрования и дешифрования:")
    print("-" * 50)
    
    for m in messages:
        c = rsa.encrypt(m)
        m_dec = rsa.decrypt(c)
        status = "ДА" if m == m_dec else "НЕТ"
        print(f"m={m} -> c={c} -> m={m_dec} (совпадение: {status})")
    
    print("\n" + "=" * 70)
    print("ВЫВОД: Алгоритмы шифрования работают корректно")
    print("=" * 70)
