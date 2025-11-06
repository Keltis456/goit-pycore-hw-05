import sys
from typing import Dict, List
from collections import defaultdict


def parse_log_line(line: str) -> Dict[str, str]:
    """
    Парсить рядок логу та повертає словник з компонентами.

    Args:
        line (str): Рядок з лог-файлу

    Returns:
        dict: Словник з ключами 'date', 'time', 'level', 'message'
    """
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        return {}

    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': parts[3]
    }


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажує та парсить лог-файл.

    Args:
        file_path (str): Шлях до файлу логів

    Returns:
        list: Список словників з розібраними логами
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Використовуємо списковий вираз (list comprehension)
            # елемент функціонального програмування
            logs = [parse_log_line(line) for line in file if line.strip()]
            # Фільтруємо порожні словники (невалідні рядки)
            logs = list(filter(lambda log: log, logs))
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except PermissionError:
        print(f"Помилка: Немає прав доступу до файлу '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(
    logs: List[Dict[str, str]], level: str
) -> List[Dict[str, str]]:
    """
    Фільтрує логи за рівнем логування.

    Args:
        logs (list): Список логів
        level (str): Рівень логування для фільтрації

    Returns:
        list: Відфільтрований список логів
    """
    # Використовуємо функцію filter - елемент функціонального програмування
    return list(
        filter(lambda log: log.get('level', '').upper() == level.upper(), logs)
    )


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Підраховує кількість записів для кожного рівня логування.

    Args:
        logs (list): Список логів

    Returns:
        dict: Словник з підрахунком записів для кожного рівня
    """
    counts = defaultdict(int)
    # Використовуємо функціональний підхід для підрахунку
    for log in logs:
        level = log.get('level', '')
        if level:
            counts[level] += 1

    return dict(counts)


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить статистику логів у вигляді таблиці.

    Args:
        counts (dict): Словник з підрахунком записів
    """
    print("\nРівень логування | Кількість")
    print("-----------------|----------")

    # Сортуємо рівні логування для красивого виведення
    # Порядок: INFO, DEBUG, ERROR, WARNING, інші
    level_order = ['INFO', 'DEBUG', 'ERROR', 'WARNING']

    # Спочатку виводимо стандартні рівні у встановленому порядку
    for level in level_order:
        if level in counts:
            print(f"{level:<17}| {counts[level]}")

    # Потім виводимо інші рівні (якщо є)
    for level, count in sorted(counts.items()):
        if level not in level_order:
            print(f"{level:<17}| {count}")


def display_log_details(logs: List[Dict[str, str]], level: str) -> None:
    """
    Виводить деталі логів для певного рівня.

    Args:
        logs (list): Список логів
        level (str): Рівень логування
    """
    filtered_logs = filter_logs_by_level(logs, level)

    if not filtered_logs:
        print(f"\nЗаписів для рівня '{level.upper()}' не знайдено.")
        return

    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    """
    Головна функція скрипту.
    """
    # Перевірка аргументів командного рядка
    if len(sys.argv) < 2:
        print("Використання: python task3.py <шлях_до_файлу_логів> "
              "[рівень_логування]")
        print("Приклад: python task3.py task3.txt")
        print("Приклад: python task3.py task3.txt error")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    # Завантаження логів
    logs = load_logs(file_path)

    if not logs:
        print("Файл логів порожній або не містить валідних записів.")
        sys.exit(1)

    # Підрахунок та виведення статистики
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Якщо вказано рівень логування, виводимо деталі
    if level_filter:
        display_log_details(logs, level_filter)


if __name__ == "__main__":
    main()
