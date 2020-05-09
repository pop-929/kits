'''
@Description: 根据图片分辨率的宽高比来将图像进行分类
@Author: pop
@E-mail: pop929@qq.com
@Date: 2020-05-08 21:34:18
@Version: 1.0.1
@LastEditTime: 2020-05-09 14:37:51
'''


import os
#import cv2
from PIL import Image
#import numpy as np
import _thread
import time


file_path="D:\\图片\\临时"  
folderlist=os.listdir(file_path)
i=0
j=0
total=0
file_total=len(folderlist)


def temp():
    File_path="D:\\图片\\临时"  #不能包含中文路径
    folderlist=os.listdir(File_path)
    for folder in folderlist:
        newpath=os.path.join(File_path,folder) #当前文件目录
        if os.path.isfile(newpath):
            continue
        filelist = os.listdir(newpath)
        i=0
        for item in filelist:
            total=len(filelist) #单文件夹文件总数
            if item.endswith(('.jpg','.png','.jpeg')):
                print('item:'+item+' folder:'+folder+'\n')

def progress():
    t=0
    while(file_total!=0):
        print('总进度：%d / %d  ---  当前文件夹进度：%d / %d   --  用时： %.1f s'%(i,file_total,j,total,t*0.5))
        time.sleep(0.5)
        t+=1


if __name__ == '__main__':
    f = open(os.path.join(file_path,'error.txt'),'w')
    if not os.path.exists(os.path.join(file_path,'横')):
        os.mkdir(os.path.join(file_path,'横'))
    if not os.path.exists(os.path.join(file_path,'竖')):
        os.mkdir(os.path.join(file_path,'竖'))
    if not os.path.exists(os.path.join(file_path,'正')):
        os.mkdir(os.path.join(file_path,'正'))
    
    _thread.start_new_thread(progress)
    for folder in folderlist:
        if str(folder) in ('横','竖','正'):
            file_total-=1
            continue
        newpath=os.path.join(file_path,folder) #当前文件目录
        if os.path.isfile(newpath):
            continue
        filelist = os.listdir(newpath)
        i+=1
        j=0
        for item in filelist:
            total=len(filelist) #单文件夹文件总数
            if item.endswith(('.jpg','.png','.jpeg')):
                #计算图片长宽比函数
                try:
                    img=Image.open(os.path.join(newpath,item))
                    #img=cv2.imread(item,-1)#读取图片信息(不能包含中文)
                    #img=cv2.imdecode(np.fromfile(item,dtype=np.uint8),-1)
                except:
                    f.write(str(folder)+'\\'+item+'\n')
                    continue
                #ratio=img.shape[1]/img.shape[0]  #宽高比
                ratio=img.width/img.height
                img.close()
                src = os.path.join(os.path.abspath(newpath), item)    #原图的地址
                if ratio>1.3:   #横的
                    dst = os.path.join(file_path,'横', item)
                elif ratio<0.8: #竖的
                    dst = os.path.join(file_path, '竖',item)
                else:  #正的
                    dst = os.path.join(file_path, '正',item)
                try:
                    os.rename(src,dst)
                    j+=1
                    #print(item+' -to- '+dst+' success!\n')
                except:
                    f.write(str(folder)+'\\'+item+'\n')
                    continue
    f.close()
    file_total=0
    print('----图片移动完成！！！')