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
                        "-b:v", "800k",  # 设置视频比特率
                        "-codec:v", "vp9",  # 使用 vp9_qsv 编解码器（若可用），否则使用 vp9
                        "-threads", "8",
                        "-cpu-used", "4",  # 提高编码速度
                        "-vf", "scale=1080:-1",  # 将视频缩放到 1080p
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
            dat_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.dat")
            
            try:
                # 创建 .usm 文件
                subprocess.run([
                    wannacri,
                    "createusm",
                    ivf_path,
                    "-o",
                    usm_path,
                    "-k",
                    "0x7F4551499DF55E68",
                ], check=True)
                
                # 将 .usm 文件重命名为 .dat 文件
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

    # Step 1: Convert MP4 to IVF
    convert_mp4_to_ivf(ffmpeg, input_directory, temp_directory)

    # Step 2: Convert IVF to USM
    convert_ivf_to_usm(wannacri, temp_directory, output_directory)
    
    # Clean up temporary files
    shutil.rmtree(temp_directory)
