import xml.etree.ElementTree as ETree
import os
from pathlib import Path


class XMLModifier:
    def __init__(self, xml_files):
        self.xml_files = xml_files

    @staticmethod
    def modify_xml(input_file):
        # Ихменение XML файла
        try:
            tree = ETree.parse(input_file)
            root = tree.getroot()

            # Обратный порядок
            images = root.findall('image')
            # images.reverse() # я не уверен нужно ли это так как в XML id и так в обратном порядке стоят

            # Переназначение id у изображений
            for idx, image in enumerate(images):
                image.set('id', str(idx))

                # Изменение имени, удаление пути к файлу, иизменение расширения
                old_name = image.get('name')
                if old_name:
                    filename = Path(old_name).name
                    name_without_ext = Path(filename).stem
                    new_name = f"{name_without_ext}.png"
                    image.set('name', new_name)

            # Сохранение файлов в папку "modified_files"
            output_file = f"./modified_files/{Path(input_file).stem}_modified{Path(input_file).suffix}"
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"Измененный файл сохранен: {output_file}")

        except ETree.ParseError as e:
            print(f"Ошибка парсинга {input_file}: {e}")
        except Exception as e:
            print(f"Ошибка процесса {input_file}: {e}")

    def modify_all(self):
        for xml_file in self.xml_files:
            if os.path.exists(xml_file):
                self.modify_xml(xml_file)
            else:
                print(f"Файл не найден: {xml_file}")


def main():
    output_dir = "modified_files"
    Path(output_dir).mkdir()

    xml_files = ['../task_train/annotations.xml', '../task_train/annotations-2.xml', '../task_train/annotations-3.xml']
    modifier = XMLModifier(xml_files)
    modifier.modify_all()


if __name__ == "__main__":
    main()
