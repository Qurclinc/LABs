#!/usr/bin/env python3
"""
Hypothesis тесты с полным отчётом.
Все тесты выполняются независимо, ошибки собираются и показываются в конце.
"""
import os
import sys
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image
import base64
import traceback
from datetime import datetime

sys.path.insert(0, '/mnt/Data/Games/LABs/APR/lab8')
from Services.crypter import Crypter

from hypothesis import given, settings, strategies as st, HealthCheck, note, seed
from hypothesis.strategies import composite, DrawFn

# ============================================================
# Стратегии генерации данных (те же)
# ============================================================

@composite
def image_keys(draw: DrawFn, min_size=5, max_size=50):
    """Генерирует случайные изображения-ключи"""
    width = draw(st.integers(min_value=min_size, max_value=max_size))
    height = draw(st.integers(min_value=min_size, max_value=max_size))
    channels = draw(st.sampled_from([1, 3, 4]))
    
    if channels == 1:
        shape = (height, width)
    else:
        shape = (height, width, channels)
    
    pixels = draw(
        st.lists(
            st.integers(0, 255),
            min_size=width * height * channels,
            max_size=width * height * channels
        )
    )
    
    img_array = np.array(pixels, dtype=np.uint8).reshape(shape)
    img = Image.fromarray(img_array)
    
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(tmp.name)
    
    return Path(tmp.name)


@composite
def file_contents(draw: DrawFn, min_size=64, max_size=10240):
    """Генерирует содержимое файлов разного размера"""
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    strategy = draw(st.sampled_from(['random', 'zeros', 'pattern', 'binary']))
    
    if strategy == 'random':
        return draw(st.binary(min_size=size, max_size=size))
    elif strategy == 'zeros':
        return b'\x00' * size
    elif strategy == 'pattern':
        pattern = draw(st.binary(min_size=1, max_size=16))
        return (pattern * (size // len(pattern) + 1))[:size]
    else:
        return (bytes(range(256)) * (size // 256 + 1))[:size]


@composite
def corrupted_encrypted_files(draw: DrawFn):
    """Генерирует повреждённые зашифрованные файлы"""
    corruption_type = draw(st.sampled_from([
        'random', 'valid_header_bad_body', 'bad_header', 
        'empty', 'huge_length', 'negative_values'
    ]))
    
    if corruption_type == 'random':
        return draw(st.binary(min_size=1, max_size=4096))
    elif corruption_type == 'valid_header_bad_body':
        iv_length = draw(st.integers(min_value=32, max_value=100))
        step = draw(st.integers(min_value=1, max_value=50))
        tag = base64.urlsafe_b64encode(os.urandom(16))
        header = f"{iv_length}0x{os.urandom(2).hex()}{step}0x{os.urandom(2).hex()}{tag.decode()}0x{os.urandom(2).hex()}\n"
        body = draw(st.binary(min_size=0, max_size=1024))
        return header.encode() + body
    elif corruption_type == 'bad_header':
        bad_headers = [
            b"abc0x1234def0x5678tag0x9abc\n",
            b"0x12340x5678tag0x9abc\n",
            b"not_a_number0x1234also_not0x5678tag0x9abc\n",
            b"9999990x12349999990x5678tag0x9abc\n",
            b"-10x1234-50x5678tag0x9abc\n",
            b"\x00\x00\x000x1234\x00\x000x5678tag0x9abc\n",
            b"",
            b"\n",
            draw(st.binary(min_size=1, max_size=200))
        ]
        return draw(st.sampled_from(bad_headers))
    elif corruption_type == 'empty':
        return b''
    elif corruption_type == 'huge_length':
        return f"9999999990x12349999999990x5678{base64.urlsafe_b64encode(os.urandom(16)).decode()}0x9abc\n".encode() + draw(st.binary(min_size=0, max_size=100))
    else:
        return f"-10x1234-50x5678{base64.urlsafe_b64encode(os.urandom(16)).decode()}0x9abc\n".encode()


# ============================================================
# Класс для сбора результатов
# ============================================================

class TestReport:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, test_name, status, details=""):
        self.results.append({
            'name': test_name,
            'status': status,
            'details': details,
            'time': datetime.now()
        })
    
    def print_summary(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("📊 TEST REPORT SUMMARY")
        print("=" * 70)
        print(f"Total time: {elapsed:.1f} seconds")
        print(f"Tests run: {len(self.results)}")
        
        passed = sum(1 for r in self.results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.results if r['status'] == 'FAILED')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        
        print("\n" + "-" * 70)
        print("DETAILED RESULTS:")
        print("-" * 70)
        
        for i, result in enumerate(self.results, 1):
            icon = {'PASSED': '✅', 'FAILED': '❌', 'ERROR': '💥'}[result['status']]
            print(f"\n{i}. {icon} {result['name']}")
            if result['details']:
                print(f"   {result['details'][:200]}")
        
        if failed > 0 or errors > 0:
            print("\n" + "=" * 70)
            print("🔍 BUGS FOUND:")
            print("=" * 70)
            for result in self.results:
                if result['status'] in ['FAILED', 'ERROR']:
                    print(f"\n• {result['name']}")
                    print(f"  {result['details']}")
        
        print("\n" + "=" * 70)


report = TestReport()


# ============================================================
# Тесты с обработкой ошибок
# ============================================================

def run_test_safely(test_name, test_func):
    """Запускает тест и собирает результаты"""
    print(f"\n🧪 Running: {test_name}")
    print("-" * 50)
    
    try:
        test_func()
        print(f"✅ PASSED")
        report.add_result(test_name, 'PASSED')
    except AssertionError as e:
        print(f"❌ FAILED: {str(e)[:200]}")
        report.add_result(test_name, 'FAILED', str(e))
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)[:200]}"
        print(f"💥 ERROR: {error_msg}")
        if hasattr(e, '__traceback__'):
            traceback.print_exc()
        report.add_result(test_name, 'ERROR', error_msg)


# ============================================================
# Property-based тесты
# ============================================================

@given(
    key_image=image_keys(),
    data=file_contents(min_size=64, max_size=1024)
)
@settings(
    max_examples=100,  # Уменьшено для скорости
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_encrypt_decrypt_cycle(key_image, data):
    """Свойство 1: Расшифровка зашифрованного = исходные данные"""
    crypter = Crypter()
    crypter.set_key(key_image)
    
    src = Path(tempfile.mktemp(suffix='.src'))
    enc = Path(tempfile.mktemp(suffix='.enc'))
    dec = Path(tempfile.mktemp(suffix='.dec'))
    
    try:
        src.write_bytes(data)
        
        success, msg = crypter.encrypt(src, enc)
        assert success, f"Encryption failed: {msg}"
        assert enc.stat().st_size > 0, "Encrypted file is empty"
        
        success, msg = crypter.decrypt(enc, dec)
        assert success, f"Decryption failed: {msg}"
        
        original = src.read_bytes()
        decrypted = dec.read_bytes()
        assert original == decrypted, \
            f"Data corruption! Original: {len(original)}B, Decrypted: {len(decrypted)}B"
            
    finally:
        for p in [src, enc, dec]:
            p.unlink(missing_ok=True)
        key_image.unlink(missing_ok=True)


@given(
    key_image=image_keys(),
    data=file_contents(min_size=64, max_size=10240)
)
@settings(max_examples=50, deadline=None)
def test_encrypt_different_sizes(key_image, data):
    """Свойство 2: Шифрование работает с файлами разного размера"""
    crypter = Crypter()
    crypter.set_key(key_image)
    
    src = Path(tempfile.mktemp(suffix='.src'))
    enc = Path(tempfile.mktemp(suffix='.enc'))
    
    try:
        src.write_bytes(data)
        success, msg = crypter.encrypt(src, enc)
        assert success, f"Failed for {len(data)} bytes: {msg}"
        assert enc.stat().st_size >= src.stat().st_size, \
            f"Encrypted ({enc.stat().st_size}B) smaller than original ({src.stat().st_size}B)"
    finally:
        src.unlink(missing_ok=True)
        enc.unlink(missing_ok=True)
        key_image.unlink(missing_ok=True)


@given(
    key_image=image_keys(),
    data=file_contents(min_size=64, max_size=1024)
)
@settings(max_examples=50, deadline=None)
def test_encrypt_idempotent(key_image, data):
    """Свойство 3: Два шифрования дают разные результаты"""
    crypter = Crypter()
    crypter.set_key(key_image)
    
    src = Path(tempfile.mktemp(suffix='.src'))
    enc1 = Path(tempfile.mktemp(suffix='.enc1'))
    enc2 = Path(tempfile.mktemp(suffix='.enc2'))
    
    try:
        src.write_bytes(data)
        crypter.encrypt(src, enc1)
        crypter.encrypt(src, enc2)
        assert enc1.read_bytes() != enc2.read_bytes(), \
            "Two encryptions produced identical files!"
    finally:
        for p in [src, enc1, enc2]:
            p.unlink(missing_ok=True)
        key_image.unlink(missing_ok=True)


@given(
    key_image=image_keys(),
    corrupted=corrupted_encrypted_files()
)
@settings(max_examples=100, deadline=None)
def test_decrypt_corrupted_data(key_image, corrupted):
    """Свойство 4: Повреждённые данные не должны крашить"""
    crypter = Crypter()
    
    corrupt = Path(tempfile.mktemp(suffix='.corrupt'))
    out = Path(tempfile.mktemp(suffix='.out'))
    
    try:
        corrupt.write_bytes(corrupted)
        crypter.set_key(key_image)
        
        try:
            result = crypter.decrypt(corrupt, out)
            if not result[0]:
                assert "MAC check failed" in result[1]
        except (ValueError, KeyError, IndexError, FileNotFoundError):
            pass
        except Exception as e:
            raise AssertionError(f"Unexpected {type(e).__name__}: {e}")
    finally:
        corrupt.unlink(missing_ok=True)
        out.unlink(missing_ok=True)
        key_image.unlink(missing_ok=True)


@given(st.binary(min_size=1, max_size=1000))
@settings(max_examples=50)
def test_encrypt_without_key(data):
    """Свойство 5: Без ключа должно быть KeyError"""
    crypter = Crypter()
    
    src = Path(tempfile.mktemp(suffix='.src'))
    dst = Path(tempfile.mktemp(suffix='.dst'))
    
    try:
        src.write_bytes(data)
        try:
            crypter.encrypt(src, dst)
            assert False, "Should have raised KeyError!"
        except KeyError:
            pass
        except Exception as e:
            assert False, f"Wrong exception: {type(e).__name__}"
    finally:
        src.unlink(missing_ok=True)
        dst.unlink(missing_ok=True)


@given(
    key_image=image_keys(),
    data=file_contents(min_size=100, max_size=1000)
)
@settings(max_examples=30, deadline=None)
def test_mac_check_on_modification(key_image, data):
    """Свойство 6: Модификация файла = ошибка MAC"""
    crypter = Crypter()
    crypter.set_key(key_image)
    
    src = Path(tempfile.mktemp(suffix='.src'))
    enc = Path(tempfile.mktemp(suffix='.enc'))
    dec = Path(tempfile.mktemp(suffix='.dec'))
    
    try:
        src.write_bytes(data)
        success, msg = crypter.encrypt(src, enc)
        assert success, f"Encryption failed: {msg}"
        
        encrypted_data = bytearray(enc.read_bytes())
        mid = len(encrypted_data) // 2
        encrypted_data[mid] = (encrypted_data[mid] + 1) % 256
        enc.write_bytes(encrypted_data)
        
        success, msg = crypter.decrypt(enc, dec)
        assert not success, "MAC check should have failed!"
        assert "MAC check failed" in msg, f"Wrong error: {msg}"
    finally:
        for p in [src, enc, dec]:
            p.unlink(missing_ok=True)
        key_image.unlink(missing_ok=True)


# ============================================================
# Главный запуск
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🔍 HYPOTHESIS PROPERTY-BASED TESTING FOR PIXCRYPT")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Encrypt-Decrypt Cycle", test_encrypt_decrypt_cycle),
        ("Different File Sizes", test_encrypt_different_sizes),
        ("Idempotent Encryption", test_encrypt_idempotent),
        ("Corrupted Data Handling", test_decrypt_corrupted_data),
        ("Encrypt Without Key", test_encrypt_without_key),
        ("MAC Check on Modification", test_mac_check_on_modification),
    ]
    
    for test_name, test_func in tests:
        run_test_safely(test_name, test_func)
    
    # Показываем полный отчёт
    report.print_summary()
    
    # Сохраняем отчёт в файл
    report_file = Path(f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_file, 'w') as f:
        f.write(f"PixCrypt Hypothesis Test Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write("=" * 70 + "\n\n")
        for result in report.results:
            f.write(f"[{result['status']}] {result['name']}\n")
            if result['details']:
                f.write(f"  {result['details']}\n")
            f.write("\n")
    
    print(f"\n📄 Report saved to: {report_file}")