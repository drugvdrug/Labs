# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА №6 - Упрощённая версия
LSB Стеганография (без внешних библиотек)
Студент: Быканов Дмитрий Константинович
"""

import struct

class SimpleLSB:
    def __init__(self):
        self.bits_to_use = 1
    
    def text_to_bits(self, text):
        bits = []
        if isinstance(text, str):
            text = text.encode('utf-8')
        for byte in text:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def bits_to_text(self, bits):
        bytes_list = []
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                val = 0
                for j in range(8):
                    val = (val << 1) | bits[i + j]
                bytes_list.append(val)
        return bytes(bytes_list).decode('utf-8', errors='replace')
    
    def create_test_image(self):
        """Создание тестового PBM изображения"""
        width, height = 400, 300
        # Создаём PBM формат (Portable BitMap)
        header = f"P1\n{width} {height}\n"
        pixels = []
        
        # Создаём узор
        for y in range(height):
            row = []
            for x in range(width):
                val = (x + y) % 2
                row.append(str(val))
            pixels.append("".join(row))
        
        with open("test_image.pbm", "w") as f:
            f.write(header)
            f.write("\n".join(pixels))
        
        print(f"Создано: test_image.pbm ({width}x{height})")
        return "test_image.pbm"
    
    def encode_lsb(self, image_path, message, output_path):
        """Сокрытие сообщения в PBM изображении"""
        print("\n[1] ШИФРОВАНИЕ (СОКРЫТИЕ)")
        print("-" * 40)
        
        with open(image_path, 'r') as f:
            lines = f.readlines()
        
        # Читаем заголовок PBM
        if lines[0].startswith("P1"):
            width, height = map(int, lines[1].split())
            pixels = []
            for line in lines[2:]:
                pixels.extend(line.strip())
        
        print(f"Размер: {width}x{height}")
        print(f"Пикселей: {len(pixels)}")
        
        # Подготовка сообщения
        msg_bits = self.text_to_bits(message)
        len_bits = [int(b) for b in format(len(msg_bits), '032b')]
        all_bits = len_bits + msg_bits
        
        print(f"Сообщение: {len(message)} символов")
        print(f"Всего битов: {len(all_bits)}")
        
        # Проверка вместимости
        if len(all_bits) > len(pixels):
            print("ОШИБКА: Сообщение слишком большое!")
            return False
        
        # Встраивание
        for i, bit in enumerate(all_bits):
            if i < len(pixels):
                pixels[i] = str(bit)
        
        # Сохранение
        with open(output_path, 'w') as f:
            f.write(f"P1\n{width} {height}\n")
            for i in range(0, len(pixels), width):
                f.write("".join(pixels[i:i+width]) + "\n")
        
        print(f"Сохранено: {output_path}")
        return True
    
    def decode_lsb(self, image_path):
        """Извлечение сообщения из PBM изображения"""
        print("\n[2] ДЕШИФРОВАНИЕ (ИЗВЛЕЧЕНИЕ)")
        print("-" * 40)
        
        with open(image_path, 'r') as f:
            lines = f.readlines()
        
        if lines[0].startswith("P1"):
            pixels = []
            for line in lines[2:]:
                pixels.extend([int(p) for p in line.strip()])
        
        # Извлечение длины (32 бита)
        len_bits = pixels[:32]
        msg_len = 0
        for bit in len_bits:
            msg_len = (msg_len << 1) | bit
        
        print(f"Длина сообщения: {msg_len} бит")
        
        # Извлечение сообщения
        msg_bits = pixels[32:32 + msg_len]
        message = self.bits_to_text(msg_bits)
        
        print(f"Извлечено символов: {len(message)}")
        return message
    
    def run(self):
        print("=" * 60)
        print("ЛАБОРАТОРНАЯ РАБОТА №6")
        print("LSB СТЕГАНОГРАФИЯ (упрощённая версия)")
        print("=" * 60)
        print("Студент: Быканов Дмитрий Константинович")
        print("=" * 60)
        
        # Создание тестового изображения
        original = self.create_test_image()
        
        # Сообщение
        msg = "Быканов Дмитрий Константинович - ЛР6 LSB"
        print(f"\nСООБЩЕНИЕ: {msg}")
        
        # Кодирование
        encoded = "encoded.pbm"
        self.encode_lsb(original, msg, encoded)
        
        # Декодирование
        decoded = self.decode_lsb(encoded)
        
        print(f"\nИЗВЛЕЧЕНО: {decoded}")
        
        # Проверка
        print("\n[3] РЕЗУЛЬТАТ")
        print("-" * 40)
        if msg == decoded:
            print("✅ УСПЕХ! Сообщения совпадают!")
        else:
            print("❌ ОШИБКА! Сообщения не совпадают!")
        
        print("\n" + "=" * 60)
        input("Нажмите Enter...")

if __name__ == "__main__":
    SimpleLSB().run()