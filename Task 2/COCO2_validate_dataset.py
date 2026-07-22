import json
from pathlib import Path
from typing import Dict, List


class COCOValidator:
    def __init__(self, annotations_path: str, images_base_dir: str):
        self.annotations_path = annotations_path
        self.images_base_dir = Path(images_base_dir)
        self.errors = []
        self.warnings = []
        self.stats = {}

    def load_annotations(self):
        # Загрузка COCO аннотаций.
        with open(self.annotations_path, 'r') as f:
            return json.load(f)

    def validate(self):
        # Валидация
        coco_data = self.load_annotations()

        images = coco_data['images']
        annotations = coco_data['annotations']
        categories = coco_data['categories']

        for img in images:
            file_path = self.images_base_dir / img['file_name']
            if not file_path.exists():
                self.errors.append(f"Image file not found: {img['file_name']}")

        image_ids = {img['id'] for img in images}
        for ann in annotations:
            if ann['image_id'] not in image_ids:
                self.errors.append(f"Annotation references unknown image_id: {ann['image_id']}")

        category_ids = {cat['id'] for cat in categories}
        for ann in annotations:
            if ann['category_id'] not in category_ids:
                self.errors.append(f"Annotation references unknown category_id: {ann['category_id']}")

        # Расчет статистики
        self.stats = {
            'total_images': len(images),
            'total_annotations': len(annotations),
            'total_categories': len(categories),
            'images_without_annotations': self.count_images_without_annotations(images, annotations),
            'errors': len(self.errors)
        }

    @staticmethod
    def count_images_without_annotations(images: List[Dict], annotations: List[Dict]) -> int:
        annotated_ids = {ann['image_id'] for ann in annotations}
        image_ids = {img['id'] for img in images}
        empty_images = image_ids - annotated_ids
        return len(empty_images)

    def save_report(self, output_path: str):
        # Сохранение отчета
        report = {
            'timestamp': str(Path.cwd()),
            'summary': self.stats,
            'warnings': self.warnings,
            'errors': self.errors
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        # Красиыий вывод статистики.
        self.print_summary()

    def print_summary(self):
        # Красиыий вывод статистики.
        print("=" * 50)
        print("ВАЛИДАЦИЯ ДАТАСЕТА")
        print("=" * 50)
        print(f"1. Количество изображений: {self.stats['total_images']}")
        print(f"2. Количество аннотаций: {self.stats['total_annotations']}")
        print(f"3. Количество категорий: {self.stats['total_categories']}")
        print(f"4. Пустых изображений: {self.stats['images_without_annotations']}")
        print(f"5. Найденных ошибок: {self.stats['errors']}")

        if self.errors:
            print("=" * 50)
            print("Статус: Обнаружены ошибки, требующие исправления")
            print("\nСписок ошибок:")
            for error in self.errors[:10]:  # Show first 10
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... и еще {len(self.errors) - 10} ошибок")
        else:
            print("=" * 50)
            print("Статус: Валидация прошла успешно")

        print("=" * 50)


def main():
    annotations_path = 'restructured_dataset/updated_annotations.json'
    images_base_dir = 'restructured_dataset'
    report_path = 'restructured_dataset/dataset_report.json'

    validator = COCOValidator(annotations_path, images_base_dir)
    validator.validate()
    validator.save_report(report_path)


if __name__ == "__main__":
    main()
