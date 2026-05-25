import subprocess
from pathlib import Path
import sys

MAX_ARGS_LENGTH = 30000

def get_binka_files_from_path(path):
    path = Path(path)

    if path.is_file() and path.suffix.lower() == ".binka":
        return [path]

    if path.is_dir():
        return list(path.rglob("*.binka"))

    return []

def collect_all_binka_files(paths):
    files = []
    for path in paths:
        files.extend(get_binka_files_from_path(path))
    return files

def executeFiles(exe_path, binka_files):
    for file in binka_files:
        command = [str(exe_path), str(file), '-o', str(file.with_suffix(".wav"))]
        print(subprocess.list2cmdline(command))

        try:
            subprocess.run(command, check=True)
            file.unlink()
            print(f"Converted: {file}")
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed: {file}")
            print(e)
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag and drop files or folders onto this executable.")
        input("Press Enter to exit...")
        sys.exit()

    input_paths = sys.argv[1:]

    exe_path = (
        Path(getattr(sys, "_MEIPASS", "."))
        / "vgmstream"
        / "vgmstream-cli.exe")

    binka_files = collect_all_binka_files(input_paths)

    if binka_files:
        print(f"Found {len(binka_files)} .binka files.")
        executeFiles(exe_path, binka_files)

    else:
        print("No .binka files found.")

    input("Done! Press Enter to exit...")
# pyinstaller --onefile --add-data "vgmstream;vgmstream" Binka2WAV.py