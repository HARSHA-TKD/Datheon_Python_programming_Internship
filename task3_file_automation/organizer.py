import os
import shutil
from pathlib import Path

# ==========================================
# SMART FILE ORGANIZER
# DATHEON - PYTHON INTERNSHIP TASK 3
# ==========================================

EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code
    ".py": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".java": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code"
}


def get_unique_path(destination):
    """Generate a unique filename if a collision occurs."""

    destination = Path(destination)

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):

    source = Path(folder_path).expanduser()

    if not source.exists() or not source.is_dir():
        print("\nError: Invalid directory!")
        return

    categories = set(EXTENSION_MAP.values())
    categories.add("Others")

    moved = 0
    skipped = 0
    failed = 0

    print("\n" + "=" * 45)
    print("       SMART FILE ORGANIZER")
    print("=" * 45)

    try:
        with os.scandir(source) as entries:
            files = list(entries)

    except PermissionError:
        print("Error: Permission denied while accessing folder.")
        return

    for entry in files:

        try:
            if not entry.is_file(follow_symlinks=False):
                continue

            file_path = Path(entry.path)

            extension = file_path.suffix.lower()

            category = EXTENSION_MAP.get(
                extension, "Others"
            )

            destination_folder = source / category

            destination_folder.mkdir(
                parents=True, exist_ok=True
            )

            destination = get_unique_path(
                destination_folder / file_path.name
            )

            shutil.move(
                str(file_path),
                str(destination)
            )

            print(
                f"[MOVED] {file_path.name} -> {category}"
            )

            moved += 1

        except PermissionError:
            print(f"[DENIED] {entry.name}")
            failed += 1

        except FileExistsError:
            print(f"[EXISTS] {entry.name}")
            skipped += 1

        except OSError as error:
            print(f"[ERROR] {entry.name}: {error}")
            failed += 1

    # Execution Summary
    print("\n" + "=" * 45)
    print("          EXECUTION SUMMARY")
    print("=" * 45)

    print(f"Total files scanned : {len(files)}")
    print(f"Files relocated     : {moved}")
    print(f"Files skipped       : {skipped}")
    print(f"Failed operations   : {failed}")

    print("=" * 45)
    print("       ORGANIZATION COMPLETE!")
    print("=" * 45)


if __name__ == "__main__":

    print("\nSMART FILE ORGANIZER")
    print("-" * 30)

    folder = input(
        "Enter folder path to organize: "
    ).strip().strip('"')

    organize_files(folder)