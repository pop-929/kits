'''
@Description: png图片转jpg
@Author: pop
@E-mail: pop929@qq.com
@Date: 2020-06-03 13:32:24
@Version: 1.0.1
@LastEditTime: 2020-06-03 16:25:28
'''


import os
from PIL import Image
import threading
import time

src="E:\\动漫\\GHS\\大"  #开始目录
dst="E:\\动漫\\GHS\\小"  #目标目录
folderlist=os.listdir(src)
file_total=len(folderlist) #文件总数
i=0 #执行过的文件数(开始目录下的)
unfinished=1#线程执行情况

def progress():
    t=0
    while(unfinished):
        print('进度：%d / %d   --  用时： %.1f s'
                %(i,file_total,t*0.5))
        time.sleep(0.5)
        t+=1
    print('----图片转换完成！！！')

def change(filelist):
    global i
    for item in filelist:
        i+=1
        newpath=src+'\\'+item
        if os.path.isdir(newpath): #如果是目录
            continue
        if item.endswith(('.png','.PNG')):
            try:
                img=Image.open(newpath)
                temp=dst+'\\'+item[:len(item)-3]+'jpg'
                img.convert('RGB').save(temp,quality=95)
            except Exception as e:
                print(item+' PNG转换JPG 错误:',e)
        elif item.endswith(('.jpg','.JPG','.jpeg','JPEG')):
            try:
                img=Image.open(newpath)
                img.convert('RGB').save(dst+'\\'+item,quality=85)
            except Exception as e:
                print(item+' JPG压缩失败:',e)
        img.close()
        os.remove(newpath)
    global unfinished
    unfinished=0

if __name__ == '__main__':
    if not os.path.exists(dst):
        os.mkdir(dst)
    tp=threading.Thread(target=progress)
    tp.start()
    change(folderlist)