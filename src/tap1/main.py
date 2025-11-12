#Этап 1: Конфигурация через CLI

import argparse
import sys
from typing import Dict, Any

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description='Визуализатор графа зависимостей пакетов - Этап 1',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--package',
        type=str,
        required=True,
        help='Имя анализируемого пакета'
    )
    
    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='URL-адрес репозитория или путь к файлу тестового репозитория'
    )
    
    parser.add_argument(
        '--test-mode',
        type=str,
        choices=['local', 'remote'],
        default='local',
        help='Режим работы с тестовым репозиторием (local/remote)'
    )
    
    parser.add_argument(
        '--version',
        type=str,
        default='latest',
        help='Версия пакета'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Максимальная глубина анализа зависимостей'
    )
    
    return vars(parser.parse_args())

def validate_parameters(params: Dict[str, Any]) -> None:
    
    # Проверка имени пакета
    if not params['package'] or not params['package'].strip():
        raise ValueError("Имя пакета не может быть пустым")
    
    # Проверка источника
    if not params['source'] or not params['source'].strip():
        raise ValueError("Источник не может быть пустым")
    
    # Проверка максимальной глубины
    if params['max_depth'] <= 0:
        raise ValueError("Максимальная глубина должна быть положительным числом")
    
    if params['max_depth'] > 10:
        raise ValueError("Максимальная глубина не может превышать 10")

def main():
    try:
        params = parse_arguments()
        validate_parameters(params)
        print("=== Параметры конфигурации ===")
        for key, value in params.items():
            print(f"{key}: {value}")
        print("==============================")
        print(f"\nАнализ пакета '{params['package']}' версии '{params['version']}'")
        print(f"Источник: {params['source']} (режим: {params['test_mode']})")
        print(f"Максимальная глубина анализа: {params['max_depth']}")
        
    except argparse.ArgumentError as e:
        print(f"Ошибка в аргументах командной строки: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка валидации параметров: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#Входные данные: python src/tap1/main.py --package "requests" --source "/test/path" --max-depth 2 