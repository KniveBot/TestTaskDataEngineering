import xml.etree.ElementTree as ETree
import os
from typing import List


class XMLAnalyzer:
    def __init__(self, xml_files: List[str]):
        # Инициализация основных переменных
        self.xml_files = xml_files
        self.stats = {
            'total_images': 0,
            'labeled_images': 0,
            'unlabeled_images': 0,
            'total_shapes': 0,
            'largest_image': {},
            'smallest_image': {}
        }
        self.image_sizes = []

    def parse_xml(self, filepath: str):
        # Парсинг файлов
        try:
            tree = ETree.parse(filepath)
            root = tree.getroot()

            for image in root.findall('image'):
                image_id = image.get('id')
                image_name = image.get('name')
                width = int(image.get('width'))
                height = int(image.get('height'))

                shapes = image.findall('.//box') + image.findall('.//polygon') + image.findall('.//points')
                shape_count = len(shapes)

                # Обновление статистики
                self.stats['total_images'] += 1
                if shape_count > 0:
                    self.stats['labeled_images'] += 1
                else:
                    self.stats['unlabeled_images'] += 1

                self.stats['total_shapes'] += shape_count

                self.image_sizes.append({
                    'id': image_id,
                    'name': image_name,
                    'width': width,
                    'height': height,
                    'area': width * height
                })

        except ETree.ParseError as e:
            print(f"Ошибка парсинга {filepath}: {e}")

    def analyze_all(self):
        for xml_file in self.xml_files:
            if os.path.exists(xml_file):
                self.parse_xml(xml_file)
            else:
                print(f"Файл не найден: {xml_file}")

        self.calculate_size_stats()

    def calculate_size_stats(self):
        # Поиск необходимой информации по размерам изображений
        if not self.image_sizes:
            return

        sorted_sizes = sorted(self.image_sizes, key=lambda x: x['area'])

        # Поиск самых больших изображений
        largest_area = sorted_sizes[-1]['area']
        largest_images = [img for img in sorted_sizes if img['area'] == largest_area]

        self.stats['largest_image'] = {
            'count': len(largest_images),
            'example': largest_images[0],
            'width': largest_images[0]['width'],
            'height': largest_images[0]['height'],
            'name': largest_images[0]['name']
        }

        # Поиск самых маленьких изображений
        smallest_area = sorted_sizes[0]['area']
        smallest_images = [img for img in sorted_sizes if img['area'] == smallest_area]

        self.stats['smallest_image'] = {
            'count': len(smallest_images),
            'example': smallest_images[0],
            'width': smallest_images[0]['width'],
            'height': smallest_images[0]['height'],
            'name': smallest_images[0]['name']
        }

    def print_statistics(self):
        # Красиыий вывод статистики.
        print("=" * 50)
        print("ОБЩАЯ СТАТИСТИКА ПО ДАТАСЕТУ")
        print("=" * 50)
        print(f"1. Общее количество изображений: {self.stats['total_images']}")
        print(f"2. Количество размеченных изображений: {self.stats['labeled_images']}")
        print(f"3. Количество неразмеченных изображений: {self.stats['unlabeled_images']}")
        print(f"4. Количество всех фигур: {self.stats['total_shapes']}")
        print("\n5. Самое большое изображение:")
        largest = self.stats['largest_image']
        print(f"   - Количество: {largest['count']}")
        if largest['count'] > 0:
            print(f"   - Название: {largest['name']}")
            print(f"   - Размер: {largest['width']}x{largest['height']}")
        print("\n6. Самое маленькое изображение:")
        smallest = self.stats['smallest_image']
        print(f"   - Количество: {smallest['count']}")
        if smallest['count'] > 0:
            print(f"   - Название: {smallest['name']}")
            print(f"   - Размер: {smallest['width']}x{smallest['height']}")
        print("=" * 50)


def main():
    xml_files = ['../task_train/annotations.xml', '../task_train/annotations-2.xml', '../task_train/annotations-3.xml']
    analyzer = XMLAnalyzer(xml_files)
    analyzer.analyze_all()
    analyzer.print_statistics()


if __name__ == "__main__":
    main()
