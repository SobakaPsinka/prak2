#Этап 2: Сбор данных о зависимостях Maven пакетов

import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import sys

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='Сбор зависимостей Maven пакетов - Этап 2')
    
    parser.add_argument('--package', type=str, required=True, help='Имя анализируемого пакета (groupId:artifactId)')
    parser.add_argument('--source', type=str, required=True, help='URL Maven репозитория')
    parser.add_argument('--version', type=str, required=True, help='Версия пакета')
    parser.add_argument('--test-mode', choices=['local', 'remote'], default='remote', help='Режим работы')
    parser.add_argument('--max-depth', type=int, default=3, help='Максимальная глубина анализа')
    
    return vars(parser.parse_args())

def get_maven_pom(repo_url: str, group_id: str, artifact_id: str, version: str) -> str:
    group_path = group_id.replace('.', '/')
    pom_url = f"{repo_url}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    
    print(f"Загружаем POM из: {pom_url}")
    
    try:
        req = urllib.request.Request(pom_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            pom_content = response.read().decode('utf-8')
            print("POM успешно загружен!")
            return pom_content
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP ошибка {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise Exception(f"Ошибка URL: {e.reason}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки: {e}")

def parse_dependencies(pom_content: str) -> List[Dict[str, str]]:
    dependencies = []
    
    try:
        root = ET.fromstring(pom_content)
        
        # Находим все зависимости в тегах <dependency>
        # Обрабатываем неймспейс Maven POM
        namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
        
        for dependency in root.findall('.//maven:dependency', namespace):
            group_id = dependency.find('maven:groupId', namespace)
            artifact_id = dependency.find('maven:artifactId', namespace)
            version_elem = dependency.find('maven:version', namespace)
            
            if group_id is not None and artifact_id is not None:
                dep = {
                    'groupId': group_id.text,
                    'artifactId': artifact_id.text,
                    'version': version_elem.text if version_elem is not None else 'не указана'
                }
                dependencies.append(dep)
                
    except ET.ParseError as e:
        raise Exception(f"Ошибка парсинга POM: {e}")
    
    return dependencies

def main():
    try:
        params = parse_arguments()
        
        if ':' not in params['package']:
            raise ValueError("Пакет должен быть в формате groupId:artifactId")
        
        group_id, artifact_id = params['package'].split(':', 1)
        
        print("=== Параметры конфигурации ===")
        for key, value in params.items():
            print(f"{key}: {value}")
        print("==============================")
        
        pom_content = get_maven_pom(params['source'], group_id, artifact_id, params['version'])
        dependencies = parse_dependencies(pom_content)
        print(f"\n=== Прямые зависимости пакета {params['package']}:{params['version']} ===")
        if dependencies:
            for i, dep in enumerate(dependencies, 1):
                print(f"{i}. {dep['groupId']}:{dep['artifactId']}:{dep['version']}")
        else:
            print("Зависимости не найдены")
        print("=========================================")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#Входные данные: python src/tap2/main.py --package "org.springframework.boot:spring-boot-starter-web" --source "https://repo1.maven.org/maven2" --version "2.7.0"