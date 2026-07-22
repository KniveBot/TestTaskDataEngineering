import xml.etree.ElementTree as ETree
import os


class ShapeTypeAnalyzer:
    def __init__(self, xml_files):
        self.xml_files = xml_files
        self.shape_types = {'box': 0, 'polygon': 0, 'points': 0}

    def parse_xml(self, filepath):
        # Парсинг файлов
        try:
            tree = ETree.parse(filepath)
            root = tree.getroot()

            for image in root.findall('image'):
                self.shape_types['box'] += len(image.findall('.//box'))
                self.shape_types['polygon'] += len(image.findall('.//polygon'))
                self.shape_types['points'] += len(image.findall('.//points'))

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
        print("СТАТИСТИКА ПО ТИПАМ ФИГУР")
        print("=" * 50)
        for shape_type, count in self.shape_types.items():
            print(f"{shape_type}: {count}")
        print("=" * 50)


def main():
    xml_files = ['../task_train/annotations.xml', '../task_train/annotations-2.xml', '../task_train/annotations-3.xml']
    analyzer = ShapeTypeAnalyzer(xml_files)
    analyzer.analyze_all()
    analyzer.print_statistics()


if __name__ == "__main__":
    main()
