from pathlib import Path
import subprocess

ROOT = Path(__file__).parent

mp4todat = ROOT / 'libraris' / 'mp4todat.py'
dattomp4 = ROOT / 'libraris' / 'dattomp4.py'

mode = input(   "1.将mp4转成dat" + 
                "2.将dat转成mp4" + 
                "\n请选择功能：")

if mode == '1':
    subprocess.run(['python', str(mp4todat)], check=True)

elif mode == '2':
    subprocess.run(['python', str(dattomp4)], check=True)