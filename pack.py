import os
import shutil

with open('./uicore/v.py', 'r') as f:
    version_data = f.read()

last_num = int((version_data.split('.')[-1]).replace("\"", ""))
with open('./uicore/v.py', 'w') as f:
    f.write("VERSION=\"2.0.%d\"" % (last_num + 1))

print("VERSION=\"2.0.%d\"" % (last_num + 1))


os.system("E:/Development/Environment/anaconda3/envs/webSpider/Scripts/pyinstaller -F -w -i ./resources/icon.ico main.py -n Spider --clean")
os.remove("C:\\Users\\ijink\\OneDrive\\Script\\Spider.exe")
shutil.move("./dist/Spider.exe", "C:\\Users\\ijink\\OneDrive\\Script")
