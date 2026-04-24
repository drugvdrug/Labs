@"
# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА №5
Тема: Обнаружение признаков заражения вирусом

Студент: Быканов Дмитрий Константинович

Функции:
1. Поиск файлов по имени в заданном каталоге
2. Поиск по содержимому (сигнатуры вирусов)
3. Информирование пользователя
4. Предложение действий с обнаруженными файлами
"""

import os
import sys
import hashlib
from datetime import datetime

class AntivirusScanner:
    """Сканер для обнаружения подозрительных файлов"""
    
    # Сигнатуры вирусов (учебные)
    VIRUS_SIGNATURES = {
        "simple_virus": b"VIRUS_SIGNATURE_123",
        "ransomware": b"ENCRYPTED_BY_RANSOM",
        "worm": b"WORM_REPLICATION_CODE",
        "trojan": b"TROJAN_BACKDOOR",
        "boot_virus": b"BOOT_SECTOR_INFECT"
    }
    
    # Подозрительные имена файлов
    SUSPICIOUS_NAMES = [
        "virus", "infected", "malware", "trojan", "worm",
        "ransom", "bootkit", "rootkit", "backdoor"
    ]
    
    def __init__(self, scan_directory):
        self.scan_directory = scan_directory
        self.detected_files = []
        self.scan_results = []
    
    def show_banner(self):
        """Вывод баннера программы"""
        print("=" * 70)
        print("ЛАБОРАТОРНАЯ РАБОТА №5")
        print("Антивирусный сканер - Обнаружение признаков заражения")
        print("=" * 70)
        print(f"Студент: Быканов Дмитрий Константинович")
        print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Каталог сканирования: {self.scan_directory}")
        print("=" * 70)
    
    def scan_by_filename(self, filename):
        """Проверка имени файла на подозрительность"""
        filename_lower = filename.lower()
        for suspicious in self.SUSPICIOUS_NAMES:
            if suspicious in filename_lower:
                return True, f"Подозрительное имя: содержит '{suspicious}'"
        return False, ""
    
    def scan_by_content(self, filepath):
        """Проверка содержимого файла на наличие вирусных сигнатур"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read(1024)  # Читаем первые 1KB
                
                for virus_name, signature in self.VIRUS_SIGNATURES.items():
                    if signature in content:
                        return True, f"Обнаружена сигнатура вируса: {virus_name}"
        except Exception:
            pass
        return False, ""
    
    def calculate_hash(self, filepath):
        """Вычисление MD5 хэша файла"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "N/A"
    
    def scan_directory(self):
        """Сканирование каталога"""
        print("\n[1] СКАНИРОВАНИЕ КАТАЛОГА...")
        print("-" * 70)
        
        if not os.path.exists(self.scan_directory):
            print(f"ОШИБКА: Каталог '{self.scan_directory}' не существует!")
            return
        
        files_scanned = 0
        
        for root, dirs, files in os.walk(self.scan_directory):
            for file in files:
                filepath = os.path.join(root, file)
                files_scanned += 1
                threats = []
                
                # Проверка по имени
                is_suspicious_name, name_reason = self.scan_by_filename(file)
                if is_suspicious_name:
                    threats.append(name_reason)
                
                # Проверка по содержимому
                has_virus, virus_reason = self.scan_by_content(filepath)
                if has_virus:
                    threats.append(virus_reason)
                
                # Если обнаружены угрозы
                if threats:
                    file_hash = self.calculate_hash(filepath)
                    self.detected_files.append({
                        'path': filepath,
                        'name': file,
                        'threats': threats,
                        'hash': file_hash,
                        'size': os.path.getsize(filepath)
                    })
                    
                    print(f"\n[ОБНАРУЖЕНО] {file}")
                    print(f"  Путь: {filepath}")
                    print(f"  Размер: {os.path.getsize(filepath)} байт")
                    print(f"  MD5: {file_hash}")
                    print(f"  Угрозы:")
                    for threat in threats:
                        print(f"    - {threat}")
        
        print("\n" + "-" * 70)
        print(f"СТАТИСТИКА СКАНИРОВАНИЯ:")
        print(f"  Всего файлов проверено: {files_scanned}")
        print(f"  Обнаружено угроз: {len(self.detected_files)}")
        print("=" * 70)
    
    def create_test_files(self):
        """Создание тестовых файлов для демонстрации"""
        print("\n[СОЗДАНИЕ ТЕСТОВЫХ ФАЙЛОВ]")
        print("-" * 70)
        
        test_dir = os.path.join(self.scan_directory, "test_files")
        os.makedirs(test_dir, exist_ok=True)
        
        # Создаём тестовые файлы
        test_files = [
            ("clean_file.txt", "Это обычный текстовый файл без вирусов"),
            ("virus_infected.exe", "VIRUS_SIGNATURE_123" + " Вредоносный код"),
            ("document_normal.doc", "Обычный документ пользователя"),
            ("trojan_downloader.exe", "TROJAN_BACKDOOR Установка бэкдора"),
            ("ransomware.exe", "ENCRYPTED_BY_RANSOM Ваши файлы зашифрованы"),
            ("worm_replication.py", "WORM_REPLICATION_CODE Код для распространения"),
            ("important_data.txt", "Важные данные без вирусов")
        ]
        
        for filename, content in test_files:
            filepath = os.path.join(test_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Создан: {filename}")
        
        print(f"\n  Тестовые файлы созданы в: {test_dir}")
        return test_dir
    
    def show_detected_files(self):
        """Вывод списка обнаруженных файлов"""
        if not self.detected_files:
            print("\n[РЕЗУЛЬТАТ] Угроз не обнаружено!")
            return True
        
        print("\n[2] СПИСОК ОБНАРУЖЕННЫХ ФАЙЛОВ")
        print("-" * 70)
        
        for i, file in enumerate(self.detected_files, 1):
            print(f"\n{i}. Имя: {file['name']}")
            print(f"   Путь: {file['path']}")
            print(f"   Размер: {file['size']} байт")
            print(f"   MD5: {file['hash']}")
            print(f"   Угрозы: {', '.join(file['threats'])}")
        
        return False
    
    def delete_files_prompt(self):
        """Запрос на удаление обнаруженных файлов"""
        if not self.detected_files:
            return
        
        print("\n[3] ВЫБОР ДЕЙСТВИЙ")
        print("-" * 70)
        print("Выберите действие с обнаруженными файлами:")
        print("  1 - Удалить все обнаруженные файлы")
        print("  2 - Удалить выбранные файлы")
        print("  3 - Не удалять файлы (только отчёт)")
        print("  0 - Выйти без действий")
        
        while True:
            try:
                choice = input("\nВаш выбор (0-3): ").strip()
                
                if choice == '0':
                    print("Действия не выполнены.")
                    return
                elif choice == '1':
                    self.delete_all_files()
                    break
                elif choice == '2':
                    self.delete_selected_files()
                    break
                elif choice == '3':
                    print("Файлы не будут удалены.")
                    break
                else:
                    print("Неверный ввод. Пожалуйста, выберите 0, 1, 2 или 3.")
            except Exception:
                print("Ошибка ввода. Попробуйте снова.")
    
    def delete_all_files(self):
        """Удаление всех обнаруженных файлов"""
        print("\n[УДАЛЕНИЕ ВСЕХ ОБНАРУЖЕННЫХ ФАЙЛОВ]")
        print("-" * 70)
        
        deleted_count = 0
        for file in self.detected_files:
            try:
                os.remove(file['path'])
                print(f"  Удалён: {file['name']}")
                deleted_count += 1
            except Exception as e:
                print(f"  Ошибка удаления {file['name']}: {e}")
        
        print(f"\n  Удалено файлов: {deleted_count} из {len(self.detected_files)}")
    
    def delete_selected_files(self):
        """Удаление выбранных файлов"""
        print("\n[УДАЛЕНИЕ ВЫБРАННЫХ ФАЙЛОВ]")
        print("-" * 70)
        
        for i, file in enumerate(self.detected_files, 1):
            print(f"\n{i}. {file['name']} - {', '.join(file['threats'])}")
            
            while True:
                choice = input(f"  Удалить этот файл? (д/н): ").strip().lower()
                if choice in ['д', 'да', 'y', 'yes']:
                    try:
                        os.remove(file['path'])
                        print(f"    Файл удалён: {file['name']}")
                        break
                    except Exception as e:
                        print(f"    Ошибка удаления: {e}")
                        break
                elif choice in ['н', 'нет', 'n', 'no']:
                    print(f"    Файл сохранён: {file['name']}")
                    break
                else:
                    print("    Введите 'д' для удаления или 'н' для сохранения")
    
    def show_report(self):
        """Вывод отчёта о работе"""
        print("\n" + "=" * 70)
        print("ОТЧЁТ О ВЫПОЛНЕННОЙ РАБОТЕ")
        print("=" * 70)
        print(f"Студент: Быканов Дмитрий Константинович")
        print(f"Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        print("ВЫПОЛНЕННЫЕ ФУНКЦИИ:")
        print("  1. Сканирование каталога на наличие файлов")
        print("  2. Поиск по имени файла (подозрительные имена)")
        print("  3. Поиск по содержимому (вирусные сигнатуры)")
        print("  4. Информирование пользователя об угрозах")
        print("  5. Предложение действий с обнаруженными файлами")
        print("-" * 70)
        print("ОБНАРУЖЕНО УГРОЗ: {len(self.detected_files)}")
        
        if self.detected_files:
            print("\nСПИСОК ОБНАРУЖЕННЫХ КОПИЙ:")
            for file in self.detected_files:
                print(f"  - {file['name']} ({', '.join(file['threats'])})")
        
        print("=" * 70)
    
    def run(self):
        """Основная функция запуска"""
        self.show_banner()
        
        # Создаём тестовые файлы
        self.create_test_files()
        
        # Сканируем каталог (включая тестовые файлы)
        self.scan_directory()
        
        # Показываем обнаруженные файлы
        has_no_threats = self.show_detected_files()
        
        # Если есть угрозы, предлагаем действия
        if not has_no_threats:
            self.delete_files_prompt()
        
        # Показываем отчёт
        self.show_report()
        
        print("\n" + "=" * 70)
        print("РАБОТА ЗАВЕРШЕНА")
        print("=" * 70)


def main():
    """Главная функция"""
    
    # Заданный каталог для сканирования
    SCAN_DIRECTORY = os.path.join(os.path.dirname(__file__), "scan_test")
    
    # Имя файла для поиска (по варианту)
    TARGET_FILENAME = "*.exe"  # Поиск всех .exe файлов
    
    print(f"Имя файла/каталога для поиска: {TARGET_FILENAME}")
    print(f"Каталог сканирования: {SCAN_DIRECTORY}")
    print()
    
    # Запуск сканера
    scanner = AntivirusScanner(SCAN_DIRECTORY)
    scanner.run()


if __name__ == "__main__":
    main()
"@ | Out-File -Encoding UTF8 lab5/antivirus_scanner.py