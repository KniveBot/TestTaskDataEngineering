import xml.etree.ElementTree as ETree
import os
from collections import Counter


class ClassAnalyzer:
    def __init__(self, xml_files):
        self.xml_files = xml_files
        self.class_counter = Counter()

    def parse_xml(self, filepath):
        # Парсинг файлов
        try:
            tree = ETree.parse(filepath)
            root = tree.getroot()

            for image in root.findall('image'):
                # Проверка типов фигур
                for shape in image.findall('.//box'):
                    label = shape.get('label')
                    self.class_counter[label] += 1
                for shape in image.findall('.//polygon'):
                    label = shape.get('label')
                    self.class_counter[label] += 1
                for shape in image.findall('.//points'):
                    label = shape.get('label')
                    self.class_counter[label] += 1

        except ETree.ParseError as e:
            print(f"Ошибка парсинга {filepath}: {e}")

    def analyze_all(self):
        for xml_file in self.xml_files:
            if os.path.exists(xml_file):
                self.parse_xml(xml_file)
            else:
                print(f"Файл не найден: {xml_file}")

    def print_statistics(self):
        # Красиыий вывод статистики.
        print("=" * 50)
        print("СТАТИСТИКА ПО КЛАССАМ")
        print("=" * 50)
        for class_name, count in self.class_counter.items():
            print(f"{class_name}: {count}")
        print("=" * 50)


def main():
    xml_files = ['../task_train/annotations.xml', '../task_train/annotations-2.xml', '../task_train/annotations-3.xml']
    analyzer = ClassAnalyzer(xml_files)
    analyzer.analyze_all()
    analyzer.print_statistics()


if __name__ == "__main__":
    main()
