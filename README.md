# TestTaskDataEngineering
Здесь представленны решения задач 1 и 2, которые находятся в папках Task 1 и Task 2 соответственно.

Код к каждому подпункту назван соответсвующе: [префикс][номер подпункта]_[название скрипта].py (префикс для первого задания это XML а для второго COCO)


Чтобы не слишком много файлов загружать я убрал результаты кода и оставил только исходные данные и скрипты. 
Везде где требуется создание папок для вывода результатов это делает сам скрипт.

Все входные данные находятся в папке "task_train"

## Задание 1: Задание по разметке: анализ XML-аннотаций

### Входные файлы:
* annotations.xml
* annotations-2.xml
* annotations-3.xml

### Скрипты:
* XML1_total_stats.py
* XML2_class_stats.py
* XML3_type_stats.py
* XML4_modification.py

### Выходные файлы:
* В скриптах 1-3 выводится внутрення статистика в консоль
* В 4 скрипте в папку "modified_files" которая создается в папке "Task 1" сохраняются:
  * annotations_modified.xml
  * annotations-2_modified.xml
  * annotations-3_modified.xml

## Задание 2: Работа с COCO-датасетом

### Входные файлы:
* task_train_coco 1.0.zip

### Скрипты:
* COCO1_restructure_dataset.py
* COCO1_restructure_dataset.py
* COCO3_reformat_to_YOLO.py

### Выходные файлы:(все папки создаются в "Task 2")
* Для COCO1_restructure_dataset.py это:
  * redtructured_dataset
    * |- images
    * |_ updated_annotations.json
* Для COCO1_restructure_dataset.py это:
  * redtructured_dataset
    * |_ dataset_report.json
* Для COCO3_reformat_to_YOLO.py это:
  * yolo_dataset
