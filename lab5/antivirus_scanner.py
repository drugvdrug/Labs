# -*- coding: utf-8 -*-
"""
ЛАБОРАТОРНАЯ РАБОТА №5
Тема: Обнаружение признаков заражения вирусом
Студент: Быканов Дмитрий Константинович
"""

import os
import hashlib
from datetime import datetime

class AntivirusScanner:
    def __init__(self, scan_directory):
        self.scan_directory = scan_directory
        self.detected_files = []
    
    def show_banner(self):
        print("=" * 70)
        print("ЛАБОРАТОРНАЯ РАБОТА №5 - АНТИВИРУСНЫЙ СКАНЕР")
        print("=" * 70)
        print(f"Студент: Быканов Дмитрий Константинович")
        print(f"Каталог сканирования: {self.scan_directory}")
        print("=" * 70)
    
    def scan_by_filename(self, filename):
        suspicious_names = ['virus', 'infected', 'malware', 'trojan', 'worm', 'ransom']
        for suspicious in suspicious_names:
            if suspicious in filename.lower():
                return True, f"Подозрительное имя: {suspicious}"
        return False, ""
    
    def scan_by_content(self, filepath):
        signatures = {
            "simple_virus": b"VIRUS_SIGNATURE_123",
            "ransomware": b"ENCRYPTED_BY_RANSOM",
            "trojan": b"TROJAN_BACKDOOR"
        }
        try:
            with open(filepath, 'rb') as f:
                content = f.read(1024)
                for virus_name, signature in signatures.items():
                    if signature in content:
                        return True, f"Сигнатура вируса: {virus_name}"
        except:
            pass
        return False, ""
    
    def get_file_hash(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return "N/A"
    
    def scan(self):
        print("\n[1] СКАНИРОВАНИЕ...")
        print("-" * 70)
        
        if not os.path.exists(self.scan_directory):
            print(f"Создаю каталог: {self.scan_directory}")
            os.makedirs(self.scan_directory)
        
        files_scanned = 0
        for root, dirs, files in os.walk(self.scan_directory):
            for file in files:
                filepath = os.path.join(root, file)
                files_scanned += 1
                threats = []
                
                is_suspicious, reason = self.scan_by_filename(file)
                if is_suspicious:
                    threats.append(reason)
                
                has_virus, vreason = self.scan_by_content(filepath)
                if has_virus:
                    threats.append(vreason)
                
                if threats:
                    self.detected_files.append({
                        'path': filepath,
                        'name': file,
                        'threats': threats,
                        'hash': self.get_file_hash(filepath)
                    })
                    print(f"\n[ОБНАРУЖЕНО] {file}")
                    print(f"  Путь: {filepath}")
                    print(f"  Угрозы: {', '.join(threats)}")
        
        print(f"\nПроверено файлов: {files_scanned}")
        print(f"Обнаружено угроз: {len(self.detected_files)}")
    
    def show_detected(self):
        if not self.detected_files:
            print("\nУгроз не обнаружено!")
            return True
        
        print("\n[2] СПИСОК ОБНАРУЖЕННЫХ ФАЙЛОВ")
        print("-" * 70)
        for i, f in enumerate(self.detected_files, 1):
            print(f"{i}. {f['name']} - {', '.join(f['threats'])}")
            print(f"   Путь: {f['path']}")
            print(f"   MD5: {f['hash']}")
        return False
    
    def delete_files(self):
        if not self.detected_files:
            return
        
        print("\n[3] ДЕЙСТВИЯ С ФАЙЛАМИ")
        print("-" * 70)
        print("1 - Удалить все")
        print("2 - Удалить выбранные")
        print("3 - Не удалять")
        
        choice = input("Ваш выбор (1-3): ").strip()
        
        if choice == '1':
            for f in self.detected_files:
                try:
                    os.remove(f['path'])
                    print(f"Удалён: {f['name']}")
                except Exception as e:
                    print(f"Ошибка: {f['name']} - {e}")
        elif choice == '2':
            for f in self.detected_files:
                ans = input(f"Удалить {f['name']}? (д/н): ").lower()
                if ans in ['д', 'да', 'y', 'yes']:
                    os.remove(f['path'])
                    print(f"  Удалён")
                else:
                    print(f"  Оставлен")
        else:
            print("Файлы не удалены")
    
    def create_test_files(self):
        test_dir = os.path.join(self.scan_directory, "test_files")
        os.makedirs(test_dir, exist_ok=True)
        
        test_data = [
            ("clean.txt", "Обычный текстовый файл"),
            ("virus_infected.exe", "VIRUS_SIGNATURE_123 вредоносный код"),
            ("document.txt", "Важные документы"),
            ("trojan.exe", "TROJAN_BACKDOOR бэкдор"),
            ("ransomware.exe", "ENCRYPTED_BY_RANSOM шифровальщик"),
            ("clean_data.txt", "Безопасные данные")
        ]
        
        for name, content in test_data:
            path = os.path.join(test_dir, name)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"\nТестовые файлы созданы в: {test_dir}")
    
    def run(self):
        self.show_banner()
        self.create_test_files()
        self.scan()
        has_no = self.show_detected()
        if not has_no:
            self.delete_files()
        
        print("\n" + "=" * 70)
        print("ОТЧЁТ СФОРМИРОВАН")
        print(f"Обнаружено: {len(self.detected_files)} угроз")
        print("=" * 70)

if __name__ == "__main__":
    scanner = AntivirusScanner("scan_test")
    scanner.run()
    input("\nНажмите Enter для выхода...")