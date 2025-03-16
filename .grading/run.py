import os
import zipfile
from os.path import join, dirname, abspath

import requests


GRADING_SERVER = os.environ["GRADING_SERVER"]
SUBMISSION_URL = f"http://{GRADING_SERVER}/api/submissions"

PROJECT_DIR_PATH = dirname(dirname(abspath(__file__)))
AUTOTESTS_LOG_PATH = join(PROJECT_DIR_PATH, "autotests.log")
LINTERS_LOG_PATH = join(PROJECT_DIR_PATH, "linters.log")

CODE_PATH = join(PROJECT_DIR_PATH, "src", "router.py")
CODE_DIR_PATH = join(PROJECT_DIR_PATH, "src")
ALLOWED_EXTENSIONS = [".py", ".md"]
NEED_CODE_DIRECTORY = True # если нужна забрать целую папку с кодом (для проектных заданий)


def zip_folder(folder_path: str, zip_name: str, allowed_extensions: list[str]) -> None:
    """
    Упаковать папку в ZIP-архив, включая только файлы с разрешенными расширениями.

    :param folder_path: Путь к папке, которую нужно упаковать.
    :param zip_name: Путь к ZIP-архиву, который будет создан.
    :param allowed_extensions: Список разрешенных расширений файлов для упаковки.
    :return: None
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(ext) for ext in allowed_extensions):
                    zip_file.write(file_path, os.path.relpath(file_path, folder_path))


if __name__ == "__main__":
    code_path = CODE_PATH
    if NEED_CODE_DIRECTORY:
        code_path = os.path.join(CODE_DIR_PATH, "code.zip")
        zip_folder(CODE_DIR_PATH, code_path, ALLOWED_EXTENSIONS)

    files = {
        'autotests_log': open(AUTOTESTS_LOG_PATH, 'r'),
        'linters_log': open(LINTERS_LOG_PATH, 'r'),
        'code': open(CODE_PATH, 'r'),
    }

    response = requests.post(SUBMISSION_URL, files=files)

    for file in files.values():
        file.close()

    print(response.text)
