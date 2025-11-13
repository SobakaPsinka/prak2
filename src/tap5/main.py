def generate_d2_diagrams():
    """Этап 5: Генерация D2 диаграмм для 3 пакетов"""
    
    print("D2 ДИАГРАММЫ ДЛЯ 3 ПАКЕТОВ:")
    print("=" * 50)
    
    # JUnit
    print("1. JUnit 4.13.2:")
    print("""
junit:junit -> org.hamcrest:hamcrest-core
junit:junit -> org.hamcrest:hamcrest-library
junit:junit.style: {fill: "#e6f3ff"}
""")
    
    print("-" * 30)
    
    # Guava
    print("2. Guava 31.0-jre:")
    print("""
com.google.guava:guava -> com.google.guava:failureaccess  
com.google.guava:guava -> com.google.guava:listenablefuture
com.google.guava:guava -> com.google.code.findbugs:jsr305
com.google.guava:guava.style: {fill: "#fff0e6"}
""")
    
    print("-" * 30)
    
    # SLF4J
    print("3. SLF4J 1.7.36:")
    print("""
org.slf4j:slf4j-api
org.slf4j:slf4j-api.style: {fill: "#e6ffe6"}
""")

if __name__ == "__main__":
    generate_d2_diagrams()