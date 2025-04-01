import os
import zipfile
from os.path import join, dirname, abspath

import requests



GRADING_SERVER = os.environ["GRADING_SERVER"] # http://localhost:8000
GITHUB_PULL_REQUEST_NUMBER = os.environ["PULL_REQUEST_NUMBER"] # 1
GITHUB_REPOSITORY_FROM_GITHUB_ACTION = os.environ["GITHUB_REPOSITORY"] # Daniil-Solo/LLM-Based-Router/
GITHUB_OWNER, GITHUB_REPOSITORY, _ = GITHUB_REPOSITORY_FROM_GITHUB_ACTION.split("/")
SUBMISSION_URL = GRADING_SERVER + "/api/submissions"

PROJECT_DIR_PATH = dirname(dirname(abspath(__file__)))
AUTOTESTS_LOG_PATH = join(PROJECT_DIR_PATH, "autotests.log")
LINTERS_LOG_PATH = join(PROJECT_DIR_PATH, "linters.log")

CODE_PATH = join(PROJECT_DIR_PATH, "src", "router.py")
CODE_DIR_PATH = join(PROJECT_DIR_PATH, "src")
ALLOWED_EXTENSIONS = [".py", ".md"]
NEED_CODE_DIRECTORY = True
# Установите True, если нужно упаковать всю папку по пути, иначе False для одного файла по пути CODE_PATH


def zip_full_folder(folder_path: str, zip_name: str, allowed_extensions: list[str]) -> None:
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


def zip_one_file(file_path: str, zip_name: str) -> None:
    """
    Упаковать один файл в ZIP-архив.

    :param file_path: Путь к файлу, который нужно упаковать.
    :param zip_name: Путь к ZIP-архиву, который будет создан.
    :return: None
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, os.path.basename(file_path))


if __name__ == "__main__":
    code_zip_path = join(PROJECT_DIR_PATH, "code.zip")
    if NEED_CODE_DIRECTORY:
        zip_full_folder(CODE_DIR_PATH, code_zip_path, ALLOWED_EXTENSIONS)
    else:
        zip_one_file(CODE_PATH, code_zip_path)

    files = {
        'autotests_log': open(AUTOTESTS_LOG_PATH, encoding="utf-8", mode='r'),
        'linters_log': open(LINTERS_LOG_PATH, encoding="utf-8", mode='r'),
        'code': open(code_zip_path, mode='rb'),
    }

    headers = {
        "X-GitHub-Owner": GITHUB_OWNER,
        "X-GitHub-Repository": GITHUB_REPOSITORY,
        "X-GitHub-Pull-Request-Number": GITHUB_PULL_REQUEST_NUMBER,
    }

    response = requests.post(SUBMISSION_URL, files=files, headers=headers)

    for file in files.values():
        file.close()

    if response.status_code not in (200, 201):
        raise SystemExit(f"Ошибка {response.status_code}, {response.json()}")
    print(response.json())