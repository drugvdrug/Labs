# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА №4
Тема: Маскировка вируса - запуск легитимной программы после выполнения

Студент: Быканов Дмитрий Константинович

Принцип маскировки:
1. Вирус (симуляция) выполняет свои действия
2. После завершения запускает указанную программу
3. Пользователь видит только легитимную программу, не подозревая о заражении
"""

import os
import sys
import subprocess
import time
import random

class VirusSimulator:
    """Симуляция вредоносной программы с маскировкой"""
    
    def __init__(self, target_file):
        """
        target_file - имя файла, который нужно запустить после маскировки
        """
        self.target_file = target_file
        self.infected_files = []
        self.damage_actions = []
    
    def show_banner(self):
        """Вывод информации о вирусе"""
        print("=" * 60)
        print("ВНИМАНИЕ! ЭТО УЧЕБНАЯ СИМУЛЯЦИЯ ВИРУСА")
        print("Лабораторная работа №4: Маскировка")
        print("=" * 60)
        print(f"Студент: Быканов Дмитрий Константинович")
        print("=" * 60)
    
    def infect_files(self):
        """Симуляция заражения файлов (без реального вреда)"""
        print("\n[1] Выполнение вредоносных действий...")
        print("-" * 40)
        
        # Создаём временную папку для демонстрации
        temp_dir = os.path.join(os.environ.get('TEMP', '.'), 'virus_demo')
        
        # Создаём несколько демо-файлов для "заражения"
        for i in range(1, 4):
            demo_file = os.path.join(temp_dir, f'test_file_{i}.txt')
            os.makedirs(temp_dir, exist_ok=True)
            
            with open(demo_file, 'w', encoding='utf-8') as f:
                f.write(f"Этот файл был 'заражён' вирусом-симулятором\n")
                f.write(f"Время 'заражения': {time.ctime()}\n")
                f.write(f"Студент: Быканов Дмитрий\n")
                f.write(f"Лабораторная работа №4\n")
            
            self.infected_files.append(demo_file)
            print(f"  [+] 'Заражён' файл: {demo_file}")
            time.sleep(0.3)  # Имитация процесса
        
        print(f"\n  [+] Всего 'заражено' файлов: {len(self.infected_files)}")
    
    def perform_damage_actions(self):
        """Симуляция вредоносных действий (логирование, без реального вреда)"""
        print("\n[2] Выполнение вредоносной логики...")
        print("-" * 40)
        
        actions = [
            "Сбор информации о системе...",
            "Чтение системных логов...",
            "Модификация реестра (симуляция)...",
            "Отправка данных на удалённый сервер (симуляция)...",
            "Копирование данных в скрытую папку..."
        ]
        
        for action in actions:
            print(f"  [*] {action}")
            self.damage_actions.append(action)
            time.sleep(0.5)  # Имитация работы
        
        print("\n  [+] Вредоносные действия выполнены (учебная симуляция)")
    
    def create_ransom_note(self):
        """Создание демо-записки (учебная цель)"""
        temp_dir = os.path.join(os.environ.get('TEMP', '.'), 'virus_demo')
        note_file = os.path.join(temp_dir, 'README_VIRUS_DEMO.txt')
        
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("УЧЕБНАЯ ДЕМОНСТРАЦИЯ ВИРУСА\n")
            f.write("=" * 60 + "\n")
            f.write("Это учебная лабораторная работа №4\n")
            f.write("Студент: Быканов Дмитрий Константинович\n")
            f.write("Тема: Маскировка вируса\n\n")
            f.write("Принцип маскировки:\n")
            f.write("- Вирус выполнил свои действия\n")
            f.write("- После чего запустил легитимную программу\n")
            f.write("- Пользователь видит только легитимную программу\n\n")
            f.write("Это не настоящий вирус, а учебная симуляция!\n")
            f.write("=" * 60 + "\n")
        
        self.infected_files.append(note_file)
        print(f"\n  [+] Создана демо-записка: {note_file}")
    
    def get_file_path(self):
        """Поиск указанной программы для запуска"""
        # Проверяем существование файла в текущей папке
        if os.path.exists(self.target_file):
            return os.path.abspath(self.target_file)
        
        # Проверяем в PATH
        for path in os.environ.get('PATH', '').split(';'):
            full_path = os.path.join(path, self.target_file)
            if os.path.exists(full_path):
                return full_path
        
        # Если не найден, создаём демо-файл
        return self.create_demo_program()
    
    def create_demo_program(self):
        """Создание демо-программы для запуска (если целевая не найдена)"""
        demo_path = os.path.join(os.path.dirname(__file__), 'demo_program.py')
        
        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write("""
# -*- coding: utf-8 -*-
\"\"\"Демо-программа для лабораторной работы №4\"\"\"
import time

print("=" * 50)
print("ЛЕГИТИМНАЯ ПРОГРАММА")
print("=" * 50)
print("Эта программа была запущена после выполнения вируса")
print("Пользователь видит только это окно")
print("-" * 50)
print("Выполнение легитимных действий...")

for i in range(3):
    print(f"  Работа программы... {i+1}/3")
    time.sleep(0.5)

print("-" * 50)
print("Программа завершила работу")
print("=" * 50)
input("Нажмите Enter для выхода...")
""")
        
        return demo_path
    
    def run_legitimate_program(self):
        """Запуск легитимной программы (маскировка)"""
        print("\n[3] ЗАПУСК МАСКИРУЮЩЕЙ ПРОГРАММЫ")
        print("-" * 40)
        
        program_path = self.get_file_path()
        print(f"  Запускается: {program_path}")
        print(f"  Это действие скрывает от пользователя факт заражения")
        print("  Пользователь видит только легитимную программу")
        print("-" * 40)
        
        try:
            if program_path.endswith('.py'):
                subprocess.Popen([sys.executable, program_path])
            else:
                subprocess.Popen([program_path], shell=True)
            
            print("\n  [+] Маскирующая программа успешно запущена!")
            return True
        except Exception as e:
            print(f"\n  [!] Ошибка запуска: {e}")
            return False
    
    def show_report(self):
        """Вывод отчёта о выполненной работе"""
        print("\n" + "=" * 60)
        print("ОТЧЁТ О ВЫПОЛНЕННОЙ РАБОТЕ")
        print("=" * 60)
        print("Студент: Быканов Дмитрий Константинович")
        print(f"Время выполнения: {time.ctime()}")
        print("-" * 60)
        print("Выполненные действия:")
        print(f"  1. Симуляция заражения файлов: {len(self.infected_files)} файлов")
        print(f"  2. Выполнение вредоносной логики: {len(self.damage_actions)} действий")
        print(f"  3. Запуск маскирующей программы: {self.target_file}")
        print("-" * 60)
        print("Принцип маскировки:")
        print("  После выполнения вредоносного кода вирус запускает")
        print("  легитимную программу, чтобы пользователь ничего не заподозрил")
        print("=" * 60)
    
    def clean_demo_files(self):
        """Очистка демо-файлов (только для лабораторной работы)"""
        print("\n[4] ОЧИСТКА ДЕМО-ФАЙЛОВ (учебная цель)")
        print("-" * 40)
        print("  Для учебных целей демо-файлы НЕ удаляются автоматически")
        print("  Вы можете удалить их вручную из папки TEMP/virus_demo")
        print(f"  Путь: {os.path.join(os.environ.get('TEMP', '.'), 'virus_demo')}")
    
    def run(self):
        """Основная функция запуска вируса-симулятора"""
        self.show_banner()
        
        # Симуляция вредоносных действий
        self.infect_files()
        self.perform_damage_actions()
        self.create_ransom_note()
        
        # Ключевой момент: запуск маскирующей программы
        print("\n" + "=" * 60)
        print("МАСКИРОВКА: Вирус завершил свои действия")
        print("Теперь запускается легитимная программа")
        print("Пользователь видит только её!")
        print("=" * 60)
        
        time.sleep(1)
        
        # Запуск легитимной программы (маскировка)
        self.run_legitimate_program()
        
        # Отчёт
        self.show_report()
        self.clean_demo_files()
        
        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("Это была учебная симуляция, а не настоящий вирус!")
        print("=" * 60)


def main():
    """Главная функция"""
    
    # Логическая переменная (по варианту)
    # Если True - вирус выполняет все действия
    # Если False - вирус не активируется
    ENABLE_VIRUS = True  # Логическая переменная для включения/отключения вируса
    
    # Имя файла с программой для маскировки
    TARGET_FILE = "demo_program.py"  # Можно изменить на "notepad.exe", "calc.exe" и т.д.
    
    print("\n" + "=" * 60)
    print("ЗАПУСК ПРОГРАММЫ")
    print("=" * 60)
    print(f"Логическая переменная ENABLE_VIRUS = {ENABLE_VIRUS}")
    print(f"Целевой файл для маскировки: {TARGET_FILE}")
    print("=" * 60)
    
    if ENABLE_VIRUS:
        # Вирус активирован - выполняем вредоносные действия и маскируемся
        virus = VirusSimulator(TARGET_FILE)
        virus.run()
    else:
        # Вирус деактивирован - просто запускаем легитимную программу
        print("\n[!] Вирус деактивирован (логическая переменная = False)")
        print("[*] Запуск легитимной программы без вредоносных действий...")
        
        simulator = VirusSimulator(TARGET_FILE)
        simulator.run_legitimate_program()


if __name__ == "__main__":
    main()
