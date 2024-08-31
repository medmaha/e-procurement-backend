import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def delete_pycache_files():
    django_project_path = BASE_DIR

    for root, dirs, files in os.walk(django_project_path):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dir = os.path.join(root, dir_name)
                files_to_delete = [
                    f
                    for f in os.listdir(pycache_dir)
                    if f.endswith(".pyc") and not f == "__init__.py"
                ]
                for file_name in files_to_delete:
                    file_path = os.path.join(pycache_dir, file_name)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

                    # Optionally, delete the corresponding .pyc/.pyo files
                    pyc_file_path = f"{file_path}c"
                    if os.path.exists(pyc_file_path):
                        os.remove(pyc_file_path)
                        print(f"Deleted: {pyc_file_path}")


if __name__ == "__main__":
    delete_pycache_files()
