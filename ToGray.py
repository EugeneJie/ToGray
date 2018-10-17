import cv2
import glob
import os
import numpy as np

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import *    #使用更美观的图形界面


def selectPath():
    path_ = askdirectory()
    path.set(path_)

def getPath():
    global p
    p = text.get()    #获取文本框中的路径
    if not p:
        p = os.getcwd()    #若文本框为空，则设置为当前路径
        print('已自动为您选择当前目录！(%s)\n'%p)
    root.destroy()

def on_closing():
    root.destroy()
    os._exit(0)


p = os.getcwd()
root = Tk()
root.title('选择文件夹')
path = StringVar()
path.set(os.getcwd())
root.protocol("WM_DELETE_WINDOW", on_closing)    #关闭tk窗口时执行on_closing

Label(root,text = "目标路径:").grid(row = 0, column = 0)
text = Entry(root, textvariable = path)
text.grid(row = 0, column = 1)
Button(root, text = "浏览", command = selectPath).grid(row = 0, column = 2)
Button(root, text = "确认", command = getPath).grid(row = 1, column = 1)

root.mainloop()

jpg = glob.glob(p + '/*.jpg') + glob.glob(p + '/*.jpeg')
png = glob.glob(p + '/*.png')
tif = glob.glob(p + '/*.tif') + glob.glob(p + '/*.tiff')
bmp = glob.glob(p + '/*.bmp')
num = len(jpg)+len(png)+len(tif)+len(bmp)

if num==0:
    print('此目录下没有可转换的图片！\n')
    input('请按回车键退出程序...')
    os._exit(0)

count = 0

print('此目录下共有 '+ str(num) + ' 张图片：')
print('jpg：' + str(len(jpg)))
print('png：' + str(len(png)))
print('tif：' + str(len(tif)))
print('bmp：' + str(len(bmp)))
print('\n'+'='*40)

for i in (jpg+png+tif+bmp):
    filename = i.split('\\')[-1]
    
    #im = imread(p + '/' + filename,cv2.IMREAD_GRAYSCALE)  #全英文路径时可用
    im = cv2.imdecode(np.fromfile(p + '/' + filename,dtype=np.uint8),0)  #支持中文路径
                      
    if not os.path.exists(p +'/convert'):
        os.mkdir(p + '/convert')
        
    #cv2.imwrite((p + '/convert/'+filename),im)  #全英文路径时可用
    cv2.imencode('.jpg', im)[1].tofile(p + '/convert/'+filename)  #支持中文路径

    count+=1
    print('\n%s\t转换完成(%d/%d)...'%(filename,count,num))
    
print('\n'+'='*40)
print('\n所有图片转换完成！请到\"%s\convert\"中查看。\n'%p.replace('/','\\'))

input('请按回车键退出程序...')
