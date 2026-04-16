# tbh Vibe-Coded
import os
import re
from typing import Optional
from aes import SAES
from logger import logger

class TUI:
    def __init__(self):
        self.saes = SAES()
        self.width = 60
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, title: str):
        print("╔" + "═" * (self.width - 2) + "╗")
        print("║" + title.center(self.width - 3) + "║")
        print("╠" + "═" * (self.width - 2) + "╣")
        
    def print_footer(self):
        print("╚" + "═" * (self.width - 2) + "╝")
        
    def print_boxed(self, text: str):
        lines = text.split('\n')
        print("╔" + "═" * (self.width - 2) + "╗")
        for line in lines:
            print("║" + line.center(self.width - 2) + "║")
        print("╚" + "═" * (self.width - 2) + "╝")
        
    def print_menu(self):
        self.clear_screen()
        self.print_header("🔐 S-AES CRYPTO SYSTEM")
        print("║" + " " * (self.width - 2) + "║")
        
        line1 = "[1] 🔒 Зашифровать"
        print("║  " + line1 + " " * (self.width - 5 - len(line1)) + "║")
        
        line2 = "[2] 🔓 Расшифровать"
        print("║  " + line2 + " " * (self.width - 5 - len(line2)) + "║")
        
        line3 = "[3] 🧹 Очистить консоль"
        print("║  " + line3 + " " * (self.width - 5 - len(line3)) + "║")
        
        print("║" + " " * (self.width - 2) + "║")
        
        line0 = "[0] 🚪 Выход"
        print("║  " + line0 + " " * (self.width - 5 - len(line0)) + "║")
        
        print("║" + " " * (self.width - 2) + "║")
        self.print_footer()
        
    def validate_hex_string(self, value: str) -> Optional[str]:
        if not value:
            return None
            
        # Приводим к нижнему регистру
        value = value.lower()
            
        # Проверяем что только hex символы
        if not re.match(r'^[0-9a-f]+$', value):
            return None
            
        # Дополняем нулями справа если меньше 4
        if len(value) < 4:
            value = value.ljust(4, '0')
            
        # Обрезаем если больше 4
        if len(value) > 4:
            value = value[:4]
            
        return value
        
    def read_input(self, prompt: str) -> str:
        while True:
            print("║  " + prompt + " " * (self.width - 5 - len(prompt) + 1) + "║")
            print("╠" + "─" * (self.width - 2) + "╣")
            print("║  > ", end="", flush=True)
            
            value = input().strip()
            validated = self.validate_hex_string(value)
            
            if validated is not None:
                return validated
            
            print("╠" + "─" * (self.width - 2) + "╣")
            error_msg = "❌ ОШИБКА: только hex-символы [0-9a-f]!"
            print("║  " + error_msg + " " * (self.width - 5 - len(error_msg)) + "║")
            print("╠" + "═" * (self.width - 2) + "╣")
    
    def print_logs(self):
        """Красивый вывод логов"""
        logs = logger.get_logs()
        if not logs:
            return
            
        print("╠" + "═" * (self.width - 2) + "╣")
        title = "📋 ЛОГИ ОПЕРАЦИИ"
        print("║  " + title + " " * (self.width - 5 - len(title)) + "║")
        print("╠" + "─" * (self.width - 2) + "╣")
        
        for log_line in logs:
            # Разбиваем длинные строки если нужно
            max_line_width = self.width - 7
            if len(log_line) <= max_line_width:
                print("║  " + log_line + " " * (self.width - 4 - len(log_line)) + "║")
            else:
                # Для очень длинных строк - перенос
                words = log_line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_line_width:
                        current_line += (" " if current_line else "") + word
                    else:
                        print("║  " + current_line + " " * (self.width - 5 - len(current_line)) + "║")
                        current_line = word
                if current_line:
                    print("║  " + current_line + " " * (self.width - 5 - len(current_line)) + "║")
        
        logger.clear()
            
    def print_result(self, operation: str, input_data: str, key: str, result: str):
        """Красивый вывод результата"""
        print("╠" + "═" * (self.width - 2) + "╣")
        
        title = "📊 РЕЗУЛЬТАТ"
        print("║  " + title + " " * (self.width - 5 - len(title)) + "║")
        
        print("╠" + "─" * (self.width - 2) + "╣")
        
        op_line = f"Операция: {operation}"
        print("║  " + op_line + " " * (self.width - 4 - len(op_line)) + "║")
        
        data_line = f"Данные:   {input_data}"
        print("║  " + data_line + " " * (self.width - 4 - len(data_line)) + "║")
        
        key_line = f"Ключ:     {key}"
        print("║  " + key_line + " " * (self.width - 4 - len(key_line)) + "║")
        
        print("╠" + "─" * (self.width - 2) + "╣")
        
        result_line = f"РЕЗУЛЬТАТ: {result}"
        print("║  " + result_line + " " * (self.width - 4 - len(result_line)) + "║")
        
    def wait_for_enter(self):
        """Ожидание нажатия Enter"""
        print("╠" + "═" * (self.width - 2) + "╣")
        msg = "Нажмите Enter для продолжения..."
        print("║  " + msg + " " * (self.width - 4 - len(msg)) + "║")
        self.print_footer()
        input()
        
    def encrypt_mode(self):
        """Режим шифрования"""
        self.clear_screen()
        self.print_header("🔒 ШИФРОВАНИЕ")
        print("║" + " " * (self.width - 2) + "║")
        
        plaintext = self.read_input("Введите открытый текст (hex, макс. 4 символа):")
        print("║" + " " * (self.width - 2) + "║")
        key = self.read_input("Введите ключ (hex, макс. 4 символа):")
        
        try:
            result = self.saes.encrypt(plaintext, key)
            self.print_logs()  # Выводим логи перед результатом
            self.print_result("Шифрование", plaintext, key, result)
        except Exception as e:
            print("╠" + "─" * (self.width - 2) + "╣")
            error_msg = f"❌ ОШИБКА: {str(e)}"
            print("║  " + error_msg + " " * (self.width - 5 - len(error_msg)) + "║")
            
        self.wait_for_enter()
        
    def decrypt_mode(self):
        """Режим расшифрования"""
        self.clear_screen()
        self.print_header("🔓 РАСШИФРОВАНИЕ")
        print("║" + " " * (self.width - 2) + "║")
        
        ciphertext = self.read_input("Введите шифротекст (hex, макс. 4 символа):")
        print("║" + " " * (self.width - 2) + "║")
        key = self.read_input("Введите ключ (hex, макс. 4 символа):")
        
        try:
            result = self.saes.decrypt(ciphertext, key)
            self.print_logs()  # Выводим логи перед результатом
            self.print_result("Расшифрование", ciphertext, key, result)
        except Exception as e:
            print("╠" + "─" * (self.width - 2) + "╣")
            error_msg = f"❌ ОШИБКА: {str(e)}"
            print("║  " + error_msg + " " * (self.width - 5 - len(error_msg)) + "║")
            
        self.wait_for_enter()
        
    def run(self):
        """Главный цикл программы"""
        while True:
            self.print_menu()
            print("║  > ", end="", flush=True)
            choice = input().strip()
            
            if choice == "1":
                self.encrypt_mode()
            elif choice == "2":
                self.decrypt_mode()
            elif choice == "3":
                self.clear_screen()
            elif choice == "0":
                self.clear_screen()
                self.print_boxed("👋 До свидания!")
                break
            else:
                print("╠" + "─" * (self.width - 2) + "╣")
                error_msg = "❌ Неверный выбор! Попробуйте снова."
                print("║  " + error_msg + " " * (self.width - 5 - len(error_msg)) + "║")
                print("╠" + "═" * (self.width - 2) + "╣")
                self.wait_for_enter()