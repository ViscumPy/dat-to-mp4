from pathlib import Path
import subprocess
import os

ROOT = Path(__file__).parent

input_path = ROOT/ 'input'
mp4todat = ROOT / 'libraris' / 'mp4todat.py'
dattomp4 = ROOT / 'libraris' / 'dattomp4.py'

while True:
    os.system('cls')
    
    for filename in os.listdir(input_path):
        if filename.endswith('.dat'):
            datfound = ".dat✅"
            break
        else:
            datfound = ".dat❌"
    for filename in os.listdir(input_path):
        if filename.endswith('.mp4'):
            mp4found = "\n.mp4✅"
            break
        else:
            mp4found = "\n.mp4❌"

    found = datfound + mp4found
    
    mode = input(f"{found}" + 
                "\n1.将mp4转成dat" + 
                "\n2.将dat转成mp4" + 
                "\nq.退出" + 
                "\n请选择功能：")
    
    if mode == '1':
        subprocess.run(['python', str(mp4todat)], check=True)

    elif mode == '2':
        subprocess.run(['python', str(dattomp4)], check=True)
        
    elif mode == 'q':
        exit()