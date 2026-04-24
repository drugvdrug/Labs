#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DigitalSignature:
    def __init__(self, private_key=0b1010101010101010):
        self.private_key = private_key & 0xFFFF
        self.public_key = self._derive_public_key(private_key)
    
    def _derive_public_key(self, private_key):
        return ((private_key << 3) | (private_key >> 13)) & 0xFFFF
    
    def cyclic_left_shift(self, value, shift=1):
        value &= 0xFFFF
        return ((value << shift) | (value >> (16 - shift))) & 0xFFFF
    
    def compute_hash(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        hash_value = 0x0000
        
        for i in range(0, len(message), 2):
            block = 0
            for j in range(2):
                if i + j < len(message):
                    block |= (message[i + j] << (8 * (1 - j)))
            
            hash_value ^= block
            hash_value = self.cyclic_left_shift(hash_value, 1)
        
        return hash_value & 0xFFFF
    
    def sign(self, message):
        h = self.compute_hash(message)
        signature = h ^ self.private_key
        return signature & 0xFFFF
    
    def verify(self, message, signature):
        h = self.compute_hash(message)
        decrypted_hash = signature ^ self.public_key
        return h == decrypted_hash


if __name__ == "__main__":
    dsa = DigitalSignature(private_key=0b1010101010101010)
    
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА: ЭЛЕКТРОННО-ЦИФРОВАЯ ПОДПИСЬ")
    print("Алгоритм: 16-битные блоки, XOR, циклический сдвиг влево")
    print("=" * 70)
    
    # Исходное сообщение
    original_message = "Договор №45 от 15.03.2026. Сумма: 12750 руб. Подпись клиента: Петров"
    print(f"\n[1] ИСХОДНОЕ СООБЩЕНИЕ:")
    print(f"    {original_message}")
    
    # Вычисление хэша и подписи
    hash_original = dsa.compute_hash(original_message)
    signature = dsa.sign(original_message)
    print(f"    Хэш сообщения: 0x{hash_original:04X} ({hash_original})")
    print(f"    ЭЦП: 0x{signature:04X} ({signature})")
    
    # Проверка подписи
    is_valid = dsa.verify(original_message, signature)
    print(f"\n[2] ПРОВЕРКА ПОДЛИННОСТИ (оригинал):")
    print(f"    Результат: {'✓ ПОДЛИННАЯ' if is_valid else '✗ НЕПОДЛИННАЯ'}")
    
    # Изменённое сообщение
    modified_message = "Договор №45 от 15.03.2026. Сумма: 12750 руб. Подпись клиента: Сидоров"
    print(f"\n[3] ИЗМЕНЁННОЕ СООБЩЕНИЕ (изменена фамилия):")
    print(f"    {modified_message}")
    
    # Проверка с той же подписью
    is_valid_modified = dsa.verify(modified_message, signature)
    hash_modified = dsa.compute_hash(modified_message)
    print(f"    Хэш изменённого сообщения: 0x{hash_modified:04X} ({hash_modified})")
    print(f"    Проверка со СТАРОЙ подписью: {'✓ ПОДЛИННАЯ' if is_valid_modified else '✗ НЕПОДЛИННАЯ'}")
    
    # Создание новой подписи
    new_signature = dsa.sign(modified_message)
    print(f"    Новая ЭЦП: 0x{new_signature:04X} ({new_signature})")
    
    # Проверка новой подписи
    is_valid_new = dsa.verify(modified_message, new_signature)
    print(f"    Проверка с НОВОЙ подписью: {'✓ ПОДЛИННАЯ' if is_valid_new else '✗ НЕПОДЛИННАЯ'}")
    
    print("\n" + "=" * 70)
    print("ВЫВОД: При изменении сообщения подпись становится недействительной")
    print("=" * 70)
    
    input("\nНажмите Enter для выхода...")
