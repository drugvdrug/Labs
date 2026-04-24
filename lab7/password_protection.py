# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА №7
Тема: Методы парольной защиты - Простой пароль

Студент: Быканов Дмитрий Константинович

Функции:
1. Установка и проверка простого пароля
2. Проверка сложности пароля
3. Защита от подбора (ограничение попыток)
4. Смена пароля
"""

import hashlib
import time
import getpass

class PasswordProtection:
    """Класс для реализации парольной защиты"""
    
    def __init__(self):
        self.password_hash = None
        self.max_attempts = 3
        self.lock_time = 30
        self.failed_attempts = 0
        self.lock_until = 0
    
    def hash_password(self, password):
        """Хэширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_password(self):
        """Установка нового пароля"""
        print("\n[УСТАНОВКА ПАРОЛЯ]")
        print("-" * 40)
        
        while True:
            password = getpass.getpass("Введите новый пароль: ")
            confirm = getpass.getpass("Подтвердите пароль: ")
            
            strength, msg = self.check_password_strength(password)
            print(f"Сложность пароля: {msg}")
            
            if password != confirm:
                print("Ошибка: Пароли не совпадают!\n")
            elif strength < 2:
                print("Пароль слишком простой. Попробуйте другой.\n")
            else:
                self.password_hash = self.hash_password(password)
                print("\n[+] Пароль успешно установлен!")
                break
    
    def check_password_strength(self, password):
        """Проверка сложности пароля"""
        score = 0
        messages = []
        
        if len(password) >= 8:
            score += 1
        else:
            messages.append("минимум 8 символов")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            messages.append("заглавные буквы")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            messages.append("строчные буквы")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            messages.append("цифры")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            score += 1
        else:
            messages.append("спецсимволы")
        
        if score >= 4:
            strength = "Высокая"
        elif score >= 2:
            strength = "Средняя"
        else:
            strength = "Низкая"
        
        if messages:
            msg = f"{strength} (рекомендуется добавить: {', '.join(messages)})"
        else:
            msg = f"{strength} (отлично!)"
        
        return score, msg
    
    def is_locked(self):
        """Проверка блокировки"""
        if self.lock_until > time.time():
            remaining = int(self.lock_until - time.time())
            print(f"Аккаунт заблокирован на {remaining} секунд")
            return True
        return False
    
    def verify_password(self, password):
        """Проверка пароля"""
        if self.password_hash is None:
            print("Пароль не установлен!")
            return False
        
        input_hash = self.hash_password(password)
        return input_hash == self.password_hash
    
    def login(self):
        """Вход с защитой от подбора"""
        if self.password_hash is None:
            print("Сначала установите пароль!")
            self.set_password()
            return True
        
        print("\n[ВХОД В СИСТЕМУ]")
        print("-" * 40)
        
        while self.failed_attempts < self.max_attempts:
            if self.is_locked():
                time.sleep(self.lock_until - time.time())
                self.failed_attempts = 0
                continue
            
            password = getpass.getpass("Введите пароль: ")
            
            if self.verify_password(password):
                print("\n[+] ДОСТУП РАЗРЕШЁН!")
                self.failed_attempts = 0
                return True
            else:
                self.failed_attempts += 1
                remaining = self.max_attempts - self.failed_attempts
                print(f"[-] Неверный пароль! Осталось попыток: {remaining}")
                
                if self.failed_attempts >= self.max_attempts:
                    self.lock_until = time.time() + self.lock_time
                    print(f"Аккаунт заблокирован на {self.lock_time} секунд")
        
        return False
    
    def change_password(self):
        """Смена пароля"""
        if not self.login():
            print("Невозможно сменить пароль: доступ запрещён")
            return False
        
        print("\n[СМЕНА ПАРОЛЯ]")
        print("-" * 40)
        self.set_password()
        return True
    
    def show_info(self):
        """Информация о системе"""
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О СИСТЕМЕ ЗАЩИТЫ")
        print("=" * 50)
        print(f"Метод защиты: Простой пароль")
        print(f"Алгоритм хэширования: SHA-256")
        print(f"Максимум попыток входа: {self.max_attempts}")
        print(f"Время блокировки: {self.lock_time} сек")
        print("Требования к паролю:")
        print("  - Минимум 8 символов")
        print("  - Заглавные и строчные буквы")
        print("  - Цифры")
        print("  - Специальные символы")
        print("=" * 50)
    
    def run(self):
        """Основная функция"""
        print("=" * 60)
        print("ЛАБОРАТОРНАЯ РАБОТА №7")
        print("Метод парольной защиты: ПРОСТОЙ ПАРОЛЬ")
        print("=" * 60)
        print(f"Студент: Быканов Дмитрий Константинович")
        print("=" * 60)
        
        while True:
            print("\n" + "=" * 40)
            print("МЕНЮ:")
            print("1 - Установить/сменить пароль")
            print("2 - Вход в систему")
            print("3 - Информация о системе")
            print("4 - Выход")
            print("=" * 40)
            
            choice = input("Выберите действие (1-4): ").strip()
            
            if choice == '1':
                if self.password_hash:
                    self.change_password()
                else:
                    self.set_password()
            
            elif choice == '2':
                if self.login():
                    print("\n[ДОСТУП ПОЛУЧЕН]")
                    print("Вы вошли в защищённую систему!")
                    input("\nНажмите Enter для продолжения...")
            
            elif choice == '3':
                self.show_info()
            
            elif choice == '4':
                print("До свидания!")
                break
            
            else:
                print("Неверный выбор!")


def demo_mode():
    """Демонстрационный режим"""
    print("=" * 60)
    print("ДЕМОНСТРАЦИОННЫЙ РЕЖИМ")
    print("=" * 60)
    
    pwd = PasswordProtection()
    
    pwd.password_hash = pwd.hash_password("Admin123!")
    print("Установлен тестовый пароль: Admin123!")
    
    test_passwords = ["123", "qwerty", "Admin123", "Admin123!", "StrongP@ssw0rd2024"]
    print("\n[ПРОВЕРКА СЛОЖНОСТИ ПАРОЛЕЙ]")
    print("-" * 40)
    for p in test_passwords:
        score, msg = pwd.check_password_strength(p)
        print(f"Пароль '{p}': {msg}")
    
    print("\n[ПРОВЕРКА ВХОДА]")
    print("-" * 40)
    
    test_inputs = ["wrong", "Admin123!"]
    for inp in test_inputs:
        result = pwd.verify_password(inp)
        print(f"Пароль '{inp}': {'ДОПУЩЕН' if result else 'ОТКАЗАНО'}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("Выберите режим:")
    print("1 - Интерактивный режим (с защитой)")
    print("2 - Демонстрационный режим (показ возможностей)")
    mode = input("Ваш выбор (1-2): ").strip()
    
    if mode == '2':
        demo_mode()
    else:
        pwd = PasswordProtection()
        pwd.run()
    
    input("\nНажмите Enter для выхода...")