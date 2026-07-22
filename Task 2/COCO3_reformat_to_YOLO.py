import json
from pathlib import Path
import shutil


class COCOtoYOLO:
    def __init__(self, annotations_path: str, images_base_dir: str, output_dir: str = 'yolo_dataset'):
        self.annotations_path = annotations_path
        self.images_base_dir = Path(images_base_dir)
        self.output_dir = Path(output_dir)
        self.coco_data = None
        self.class_mapping = {}

    def get_image_size_simple(self, img_path):
        # Попытка найти размеры в COCO аннотации
        for img in self.coco_data['images']:
            if Path(img['file_name']).name == img_path.name:
                return img.get('width', 0), img.get('height', 0)

        return 0, 0

    def load_coco(self):
        # Загрузка COCO аннотаций
        with open(self.annotations_path, 'r', encoding='utf-8') as f:
            self.coco_data = json.load(f)

        for idx, cat in enumerate(self.coco_data['categories']):
            self.class_mapping[cat['id']] = idx

    @staticmethod
    def convert_bbox_to_yolo(bbox, img_width, img_height):
        # Конвертация COCO в YOLO формат
        x, y, width, height = bbox

        x_center = (x + width / 2) / img_width
        y_center = (y + height / 2) / img_height
        width_norm = width / img_width
        height_norm = height / img_height

        return [x_center, y_center, width_norm, height_norm]

    def convert(self):
        # Основной блок конвертации
        self.load_coco()

        images = self.coco_data['images']
        annotations = self.coco_data['annotations']

        image_sizes = {}
        for img in images:
            image_sizes[img['id']] = (img.get('width', 0), img.get('height', 0))

        img_annotations = {}
        for ann in annotations:
            img_id = ann['image_id']
            if img_id not in img_annotations:
                img_annotations[img_id] = []
            img_annotations[img_id].append(ann)

        classes_file = self.output_dir / 'classes.txt'
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with open(classes_file, 'w', encoding='utf-8') as f:
            for cat in self.coco_data['categories']:
                f.write(f"{cat['name']}\n")

        print(f"Создан файл классов: {classes_file}")

        for img in images:
            img_id = img['id']
            img_path = self.images_base_dir / img['file_name']

            if not img_path.exists():
                print(f"Предупреждение: Изображение не найдено: {img_path}")
                continue

            width, height = image_sizes.get(img_id, (0, 0))

            if width == 0 or height == 0:
                print(f"Предупреждение: Нет размеров в COCO для {img_path}")
                continue

            class_folder = img_path.parent.name
            yolo_img_dir = self.output_dir / class_folder
            yolo_img_dir.mkdir(parents=True, exist_ok=True)

            img_destination = yolo_img_dir / img_path.name
            shutil.copy2(img_path, img_destination)

            # Создание файла аннотации в YOLO формате
            txt_filename = img_path.stem + '.txt'
            txt_path = yolo_img_dir / txt_filename

            with open(txt_path, 'w', encoding='utf-8') as f:
                if img_id in img_annotations:
                    for ann in img_annotations[img_id]:
                        class_id = self.class_mapping[ann['category_id']]
                        bbox = ann['bbox']
                        yolo_bbox = self.convert_bbox_to_yolo(bbox, width, height)
                        f.write(f"{class_id} {' '.join(map(str, yolo_bbox))}\n")

        print(f"YOLO датасет сохранен в {self.output_dir}")


def main():
    annotations_path = 'restructured_dataset/updated_annotations.json'
    images_base_dir = 'restructured_dataset'
    output_dir = 'yolo_dataset'

    converter = COCOtoYOLO(annotations_path, images_base_dir, output_dir)
    converter.convert()


if __name__ == "__main__":
    main()
