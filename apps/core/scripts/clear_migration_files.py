import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def delete_migration_files(delete_db=False):
    if delete_db:
        if os.path.exists(os.path.join(BASE_DIR / "db" / "db.sqlite3")):
            os.remove(os.path.join(BASE_DIR / "db" / "db.sqlite3"))

    for root, dirs, files in os.walk(os.path.join(BASE_DIR / "apps")):
        for dir_name in dirs:
            if dir_name == "migrations":
                migrations_dir = os.path.join(root, dir_name)
                files_to_delete = [
                    f
                    for f in os.listdir(migrations_dir)
                    if f.endswith(".py") and not f == "__init__.py"
                ]
                for file_name in files_to_delete:
                    file_path = os.path.join(migrations_dir, file_name)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

                    pyc_file_path = f"{file_path}c"
                    if os.path.exists(pyc_file_path):
                        os.remove(pyc_file_path)
                        print(f"Deleted: {pyc_file_path}")


if __name__ == "__main__":
    delete_migration_files()
