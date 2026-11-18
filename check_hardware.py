import os
import sys
import serial

SDR_PORT = '/dev/sdr_primary'
COMPASS_PORT = '/dev/uart_compass'


def check_device_access(device_path):
    """Перевіряє наявність файлу пристрою та права доступу до нього."""
    if not os.path.exists(device_path):
        print(f"[ПОМИЛКА] Пристрій {device_path} не знайдено. Перевірте udev-правила.")
        return False

    if not os.access(device_path, os.R_OK | os.W_OK):
        print(f"[ПОМИЛКА] Немає прав на читання/запис для {device_path}. Перевірте MODE='0666' в udev.")
        return False

    print(f"[ОК] Пристрій {device_path} присутній, права доступу налаштовані правильно.")
    return True


def test_compass_connection(port_path, baudrate=9600):
    """Спроба відкрити порт компаса та зчитати тестові байти."""
    print(f"\n--- Спроба зв'язку з компасом через {port_path} ---")
    try:
        # Відкриваємо порт із таймаутом, щоб скрипт не завис, якщо пристрій не передає дані
        with serial.Serial(port_path, baudrate, timeout=2) as ser:
            print(f"[ІНФО] Порт {port_path} успішно відкрито на швидкості {baudrate} бод.")

            # Якщо компас вимагає команди-запиту для відправки даних, розкоментуйте рядок нижче:
            # ser.write(b'R')

            # Читаємо 10 байт (кількість можна змінити залежно від протоколу компаса)
            raw_data = ser.read(10)

            if raw_data:
                print(f"[ОК] Отримано тестові дані від компаса (Hex): {raw_data.hex()}")
                return True
            else:
                print("[ПОПЕРЕДЖЕННЯ] Порт відкрито, але дані не отримано (пристрій підключений, але мовчить).")
                return False

    except serial.SerialException as e:
        print(f"[ПОМИЛКА] Помилка роботи з послідовним портом: {e}")
        return False


if __name__ == '__main__':
    print("=== Перевірка апаратного комплексу радіомоніторингу ===\n")

    # 1. Перевірка наявності та прав доступу
    sdr_ok = check_device_access(SDR_PORT)
    compass_ok = check_device_access(COMPASS_PORT)

    # 2. Якщо компас доступний на рівні ОС, перевіряємо фізичний потік даних
    if compass_ok:
        test_compass_connection(COMPASS_PORT)

    print("\n=== Перевірку завершено ===")
