import os
import subprocess
from pathlib import Path
import shutil

ROOT = Path(__file__).parent

def decrypt_dat_files(wannacri, input_directory, temp_directory, decryption_key):
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        return
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)
    for filename in os.listdir(input_directory):
        if filename.endswith('.dat'):
            dat_path = os.path.join(input_directory, filename)
            output_path = os.path.join(temp_directory, os.path.splitext(filename)[0])
            try:
                subprocess.run([
                    wannacri, 'extractusm', '-p', dat_path, '-o', output_path, '--key', decryption_key
                ], check=True)
                print(f"Successfully decrypted {filename} to {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error decrypting {filename}: {e}")

def convert_ivf_to_mp4(ffmpeg, temp_directory, output_directory):
    if not os.path.isdir(temp_directory):
        print(f"Error: {temp_directory} is not a valid directory.")
        return
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, files in os.walk(temp_directory):
        for filename in files:
            if filename.endswith('.ivf'):
                ivf_path = os.path.join(root, filename)
                mp4_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.mp4")

                try:
                    subprocess.run([
                        ffmpeg, '-i', ivf_path, '-c:v', 'h264_nvenc', mp4_path
                    ], check=True)
                    print(f"Successfully converted {filename} to {mp4_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    input_directory = ROOT.parent / 'input'
    temp_directory = ROOT.parent / 'temp'
    output_directory = ROOT.parent / 'output'
    wannacri = ROOT / 'wannacri.exe'
    decryption_key = '0x7F4551499DF55E68'
    ffmpeg = ROOT / 'ffmpeg.exe'

    decrypt_dat_files(wannacri, input_directory, temp_directory, decryption_key)

    convert_ivf_to_mp4(ffmpeg, temp_directory, output_directory)

    shutil.rmtree(temp_directory)