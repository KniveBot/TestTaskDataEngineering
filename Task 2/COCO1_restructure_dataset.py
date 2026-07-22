import json
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Set
import tempfile


class COCORestructure:
    def __init__(self, zip_path: str, output_dir: str = 'restructured_dataset'):
        self.zip_path = Path(zip_path)
        self.output_dir = Path(output_dir)
        self.temp_dir = None
        self.images_dir = None
        self.annotations_path = None

        self.output_images_dir = self.output_dir / 'images'
        self.output_annotations = self.output_dir / 'updated_annotations.json'

    def extract_zip(self):
        # Работа с ZIP
        if not self.zip_path.exists():
            raise FileNotFoundError(f"ZIP файл не найден: {self.zip_path}")

        # Создаем временную директорию
        self.temp_dir = Path(tempfile.mkdtemp(prefix='coco_temp_'))
        print(f"Извлечение {self.zip_path}...")

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

        json_files = list(self.temp_dir.rglob('*.json'))
        if not json_files:
            raise FileNotFoundError("JSON файл с аннотациями не найден в архиве")

        self.annotations_path = json_files[0]
        print(f"Найден файл аннотаций: {self.annotations_path.name}")

        possible_image_dirs = [
            self.temp_dir / 'images',
            self.temp_dir / 'train',
            self.temp_dir / 'val',
            self.temp_dir
        ]

        for img_dir in possible_image_dirs:
            if img_dir.exists() and (any(img_dir.glob('*.jpg')) or any(img_dir.glob('*.png'))):
                self.images_dir = img_dir
                break

        if not self.images_dir:
            # Ищем любые изображения в temp_dir
            img_files = list(self.temp_dir.rglob('*.jpg')) + list(self.temp_dir.rglob('*.png'))
            if img_files:
                self.images_dir = img_files[0].parent
            else:
                raise FileNotFoundError("Изображения не найдены в архиве")

        print(f"Найдена директория с изображениями: {self.images_dir.name}")

        self.output_images_dir.mkdir(parents=True, exist_ok=True)

    def load_coco(self):
        # Загрузка COCO аннотаций.
        if not self.annotations_path:
            raise ValueError("Аннотации не загружены. Сначала вызовите extract_zip()")

        with open(self.annotations_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_image_classes(image_id: int, annotations: List[Dict]) -> Set[int]:
        # Получение уникальных id классов для изображения.
        class_ids = set()
        for ann in annotations:
            if ann['image_id'] == image_id:
                class_ids.add(ann['category_id'])
        return class_ids

    @staticmethod
    def get_class_names(class_ids: Set[int], categories: List[Dict]) -> List[str]:
        # Преобразование id классов в названия.
        id_to_name = {cat['id']: cat['name'] for cat in categories}
        return sorted([id_to_name[cat_id] for cat_id in class_ids if cat_id in id_to_name])

    def restructure(self):
        self.extract_zip()

        coco_data = self.load_coco()

        images = coco_data['images']
        annotations = coco_data['annotations']
        categories = coco_data['categories']

        updated_images = []

        for img in images:
            img_id = img['id']
            class_ids = self.get_image_classes(img_id, annotations)
            class_names = self.get_class_names(class_ids, categories)

            if not class_names:
                folder_name = 'no_annotations'
            elif len(class_names) == 1:
                folder_name = class_names[0]
            else:
                folder_name = '_'.join(class_names)

            destination_dir = self.output_images_dir / folder_name
            destination_dir.mkdir(parents=True, exist_ok=True)

            src_path = self.images_dir / img['file_name']

            # Если файл не найден, пробуем поискать в поддиректориях
            if not src_path.exists():
                possible_paths = list(self.images_dir.rglob(img['file_name']))
                if possible_paths:
                    src_path = possible_paths[0]
                else:
                    print(f"Предупреждение: Файл не найден: {img['file_name']}")
                    continue

            destination_path = destination_dir / img['file_name']

            try:
                shutil.copy2(src_path, destination_path)
            except Exception as e:
                print(f"Ошибка копирования {img['file_name']}: {e}")
                continue

            # Обновляем запись об изображении
            img_copy = img.copy()
            img_copy['file_name'] = str(destination_path.relative_to(self.output_dir))
            updated_images.append(img_copy)

        # Обновляем COCO данные
        coco_data['images'] = updated_images

        # Сохраняем обновленные аннотации
        with open(self.output_annotations, 'w', encoding='utf-8') as f:
            json.dump(coco_data, f, indent=2, ensure_ascii=False)

        print(f"\nРеструктуризация завершена!")
        print(f"Обновленные аннотации сохранены в: {self.output_annotations}")
        print(f"Изображения сохранены в: {self.output_images_dir}")

    def cleanup(self):
        # Очистка временных файлов.
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"Временные файлы удалены")


def main():
    # Путь к ZIP архиву
    zip_path = '../task_train/task_train_coco 1.0.zip'
    output_dir = 'restructured_dataset'

    restructure = COCORestructure(zip_path, output_dir)
    try:
        restructure.restructure()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        restructure.cleanup()


if __name__ == "__main__":
    main()
