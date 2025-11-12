#Этап 5: Визуализация графа зависимостей

import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import sys
import ssl

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей - Этап 5')
    
    parser.add_argument('--package', type=str, required=True, help='Имя анализируемого пакета (groupId:artifactId)')
    parser.add_argument('--source', type=str, required=True, help='URL Maven репозитория')
    parser.add_argument('--version', type=str, required=True, help='Версия пакета')
    parser.add_argument('--max-depth', type=int, default=2, help='Максимальная глубина анализа')
    
    return vars(parser.parse_args())

def get_maven_pom(repo_url: str, group_id: str, artifact_id: str, version: str) -> str:
#Получаем POM файл из Maven репозитория
    group_path = group_id.replace('.', '/')
    pom_url = f"{repo_url}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    
    print(f"Загружаем: {pom_url}")
    
    try:
        # Создаем SSL контекст который игнорирует проверки сертификатов
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(pom_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            print("POM успешно загружен")
            return response.read().decode('utf-8')
    except Exception as e:
        raise Exception(f"Ошибка загрузки POM: {e}")

def parse_dependencies(pom_content: str) -> List[Dict[str, str]]:
    dependencies = []
    
    try:
        root = ET.fromstring(pom_content)
        for namespace in [{'maven': 'http://maven.apache.org/POM/4.0.0'}, None]:
            try:
                deps = root.findall('.//dependency') if namespace is None else root.findall('.//maven:dependency', namespace)
                for dep in deps:
                    group_id = dep.find('groupId') if namespace is None else dep.find('maven:groupId', namespace)
                    artifact_id = dep.find('artifactId') if namespace is None else dep.find('maven:artifactId', namespace)
                    version_elem = dep.find('version') if namespace is None else dep.find('maven:version', namespace)
                    
                    if group_id is not None and artifact_id is not None:
                        dependencies.append({
                            'groupId': group_id.text,
                            'artifactId': artifact_id.text,
                            'version': version_elem.text if version_elem is not None else 'N/A'
                        })
            except:
                continue
                
    except ET.ParseError as e:
        raise Exception(f"Ошибка парсинга XML: {e}")
    
    return dependencies

def build_dependency_graph(package: str, version: str, repo_url: str, max_depth: int) -> Dict[str, List[str]]:
    graph = {}
    visited = set()
    
    def explore_deps(current_package: str, current_version: str, depth: int):
        if depth > max_depth or current_package in visited:
            return
            
        visited.add(current_package)
        
        if ':' not in current_package:
            return
            
        group_id, artifact_id = current_package.split(':', 1)
        
        try:
            pom_content = get_maven_pom(repo_url, group_id, artifact_id, current_version)
            dependencies = parse_dependencies(pom_content)
            
            graph[current_package] = []
            for dep in dependencies:
                dep_key = f"{dep['groupId']}:{dep['artifactId']}"
                graph[current_package].append(dep_key)
                explore_deps(dep_key, dep['version'], depth + 1)
        except Exception as e:
            print(f"Пропускаем {current_package}: {e}")
            graph[current_package] = ["[ошибка загрузки]"]
    
    explore_deps(package, version, 0)
    return graph

def visualize_graph(graph: Dict[str, List[str]], root_package: str):
#Визуализация графа в текстовом виде
    print(f"\n=== ГРАФ ЗАВИСИМОСТЕЙ ===")
    
    visited = set()
    
    def print_deps(package: str, level: int = 0):
        if package in visited:
            print("  " * level + f"└── {package} [...]")
            return
            
        visited.add(package)
        indent = "  " * level
        
        if level == 0:
            print(f"Пак{package}")
        else:
            print(f"{indent}└── {package}")
        
        if package in graph:
            for dep in graph[package]:
                print_deps(dep, level + 1)
    
    print_deps(root_package)
    print("========================")

def main():
    try:
        args = parse_arguments()
        
        print("=== Параметры конфигурации ===")
        for key, value in args.items():
            print(f"{key}: {value}")
        
        graph = build_dependency_graph(args['package'], args['version'], args['source'], args['max_depth'])
        visualize_graph(graph, args['package'])
        
        print(f"\n📊 Статистика:")
        print(f"Пакетов: {len(graph)}")
        print(f"Зависимостей: {sum(len(deps) for deps in graph.values())}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#Входные данные: python src/tap5/main.py --package "com.google.guava:guava" --source "https://repo1.maven.org/maven2" --version "31.0-jre" --max-depth 1