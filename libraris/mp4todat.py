import os
import subprocess
from pathlib import Path
import shutil

ROOT = Path(__file__).parent

use_qsv = False

def convert_mp4_to_ivf(ffmpeg, input_directory, temp_directory):
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        return
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.mp4'):
                mp4_path = os.path.join(root, filename)
                ivf_path = os.path.join(temp_directory, f"{os.path.splitext(filename)[0]}.ivf")

                try:
                    subprocess.run([
                        ffmpeg,
                        "-i",
                        mp4_path,
                        "-b:v", "800k",
                        "-codec:v", "vp9",
                        "-threads", "8",
                        "-cpu-used", "4",
                        "-vf", "scale=1080:-1",
                        ivf_path
                    ], check=True)
                    print(f"Successfully converted {filename} to {ivf_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {filename} to IVF: {e}")

def convert_ivf_to_usm(wannacri, temp_directory, output_directory):
    for filename in os.listdir(temp_directory):
        if filename.endswith('.ivf'):
            ivf_path = os.path.join(temp_directory, filename)
            usm_path = os.path.join(temp_directory, f"{os.path.splitext(filename)[0]}.usm")
            dat_path = os.path.join(output_directory / "{filename}", f"{os.path.splitext(filename)[0]}.dat")
            
            try:
                subprocess.run([
                    wannacri,
                    "createusm",
                    ivf_path,
                    "-o",
                    usm_path,
                    "-k",
                    "0x7F4551499DF55E68",
                ], check=True)
                os.rename(usm_path, dat_path)
                print(f"Successfully converted {filename} to {dat_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {filename} to USM: {e}")
            except OSError as e:
                print(f"Error renaming {usm_path} to {dat_path}: {e}")


if __name__ == "__main__":
    input_directory = ROOT.parent / 'input'
    temp_directory = ROOT.parent / 'temp'
    output_directory = ROOT.parent / 'output'
    wannacri = ROOT / 'wannacri.exe'
    encryption_key = '0x7F4551499DF55E68'
    ffmpeg = ROOT / 'ffmpeg.exe'

    convert_mp4_to_ivf(ffmpeg, input_directory, temp_directory)
    convert_ivf_to_usm(wannacri, temp_directory, output_directory)
    
    shutil.rmtree(temp_directory)
