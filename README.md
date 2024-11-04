# Corvax Warden Helper

> [!NOTE]  
> Данный репозиторий - **некоммерческая** *User-Friendly* сборка приложения для игроков серверов corvax. Вы можете использовать исходные файлы и ресурсы, чтобы самостоятельно изучить и настроить приложение.
---

> [!CAUTION]  
> **Некоторые антивирусные программы** могут ошибочно распознавать приложение как ***вредоносное ПО***. Это нормальное поведение, так как приложение содержит исполняемые файлы. Если вы обеспокоены безопасностью, вы всегда можете просмотреть код и собрать приложение самостоятельно.

## Установка

### Windows
> [!IMPORTANT]  
> Если вы еще не скачали, то скачайте **`Source code (zip)`** c последннего [релиза](https://github.com/weylor654/warden-helper/releases/tag/v2.0.0), разархивируйте его в отдельную папку. После этого найдите папку **`dist`** и откройте приложение. Другие файлы и папки можно удалить, так как они не требуются для запуска.

### Описание файлов и папок

- **`src/`**: Содержит все исходные файлы приложения на Python:
  - **`warden_helper_logic.py`**: Содержит логику расчётов приложения.
  - **`warden_helper_menu.py`**: Основное меню приложения, отвечающее за пользовательский интерфейс.
  - **`warden_helper_ui.py`**: Крупная таблица с полным переносом таблицы КЗ.
  - **`warden_helper_ui_abridged.py`**: Сокращённый вариант приложения для быстрого расчёта.
  - **`my_bar.py`**: Тест и редактура кастомного заголовка интерфейса.
  - **`GUI_Test.py`**: Тестирование графического интерфейса приложения.

- **`data/`**: Папка с изображениями и ресурсами для приложения.

- **`dist/`**: Папка, содержащая собранное приложение, готовое к запуску.

- **`build/`**: Папка с данными о сборке приложения.

- **`__pycache__/`**: Содержит скомпилированные файлы для оптимизации работы Python.

- **`warden_helper.spec`**: Файл спецификации, используемый для сборки приложения с помощью PyInstaller.

## Лицензия

Это приложение лицензировано под [MIT License](LICENSE).
