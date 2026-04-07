import os
import subprocess
from pathlib import Path
import sys

def get_binka_files_from_path(path):
    binka_files = []

    if os.path.isfile(path) and path.lower().endswith(".binka"):
        return [path]

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(".binka"):
                    binka_files.append(os.path.join(root, file))

    return binka_files

def collect_all_binka_files(paths):
    all_files = []
    for path in paths:
        all_files.extend(get_binka_files_from_path(path))
    return all_files

def executeFiles(exe_path, binka_files):
    MAX_ARGS_LENGTH = 32000
    chunk = []
    total_length = len(str(exe_path))

    for file in binka_files:
        file_length = len(file) + 1

        if total_length + file_length > MAX_ARGS_LENGTH:
            command = [str(exe_path)] + chunk
            print(f"Running: {' '.join(command)}")
            subprocess.run(command, check=True)

            chunk = [file]
            total_length = len(str(exe_path)) + len(file)
        else:
            chunk.append(file)
            total_length += file_length

    if chunk:
        command = [str(exe_path)] + chunk
        print(f"Running: {' '.join(command)}")
        subprocess.run(command, check=True)

def deleteFiles(binka_files):
    for file in binka_files:
        wav_file = file + ".wav"
        if os.path.exists(wav_file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"Skipping delete (no output): {file}")

def get_converted_wav_files(binka_files):
    wav_files = []
    for file in binka_files:
        wav_file = file + ".wav"
        if os.path.exists(wav_file):
            wav_files.append(wav_file)
    return wav_files

def renameFiles(wav_files):
    for file_path in wav_files:
        if file_path.lower().endswith(".binka.wav"):
            dir_name = os.path.dirname(file_path)
            new_name = os.path.basename(file_path).replace(".binka", "")
            new_path = os.path.join(dir_name, new_name)
            try:
                os.rename(file_path, new_path)
                print(f"Renamed: {file_path} -> {new_path}")
            except Exception as e:
                print(f"Error renaming {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag and drop files or folders onto this executable.")
        input("Press Enter to exit...")
        sys.exit()

    input_paths = sys.argv[1:]
    exe_path = Path(getattr(sys, "_MEIPASS", ".")) / "vgmstream" / "vgmstream-cli.exe"

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