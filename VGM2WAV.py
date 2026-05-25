import subprocess
from pathlib import Path
import sys

filetypes = [
    ".binka",
    ".wem",
    ".awb",
    ".fsb"]

def get_binka_files_from_path(path):
    path = Path(path)

    if path.is_file() and path.suffix.lower() in filetypes:
        return [path]

    if path.is_dir():
        lst = []
        for t in filetypes:
            c = list(path.rglob(f"*{t}"))
            print(f"Found {len(c)} {t} files in {path}")
            lst.extend(c)

        return lst

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
        executeFiles(exe_path, binka_files)

    else:
        print("No supported files found.")

    input("Done! Press Enter to exit...")
# pyinstaller --onefile --add-data "vgmstream;vgmstream" VGM2WAV.py