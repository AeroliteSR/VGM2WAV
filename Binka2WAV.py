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
        command = [str(exe_path), str(file)]

        print(subprocess.list2cmdline(command))

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed: {file}")
            print(e)

def deleteFiles(binka_files):
    for file in binka_files:
        wav_file = file.with_suffix(file.suffix + ".wav")

        if wav_file.exists():
            try:
                file.unlink()
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"Skipping delete (no output): {file}")

def get_converted_wav_files(binka_files):
    wav_files = []
    for file in binka_files:
        wav_file = file.with_suffix(file.suffix + ".wav")

        if wav_file.exists():
            wav_files.append(wav_file)
    return wav_files

def renameFiles(wav_files):
    for file_path in wav_files:
        if file_path.name.lower().endswith(".binka.wav"):
            new_name = file_path.name.replace(".binka", "")
            new_path = file_path.with_name(new_name)

            if new_path.exists():
                print(f"Skipping rename, exists: {new_path}")
                continue

            try:
                file_path.rename(new_path)
                print(f"Renamed: {file_path} -> {new_path}")
            except Exception as e:
                print(f"Error renaming {file_path}: {e}")

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
        deleteFiles(binka_files)
        renameFiles(get_converted_wav_files(binka_files))

    else:
        print("No .binka files found.")

    input("Done! Press Enter to exit...")
# pyinstaller --onefile --add-data "vgmstream;vgmstream" Binka2WAV.py