'''
@Description: 根据图片分辨率的宽高比来将图像进行分类
@Author: pop
@E-mail: pop929@qq.com
@Date: 2020-05-08 21:34:18
@Version: 1.2.1
@LastEditTime: 2020-05-13 00:28:12
'''


import os
from PIL import Image
import threading
import time


#file_path="E:\\动漫\\"  #开始目录
file_path="D:\\图片\\临时"  
folderlist=os.listdir(file_path)
file_total=len(folderlist) #文件总数
f_1=threading.Semaphore(1) #error.txt 文件的锁
i=[0,0,0,0] #执行过的文件数(开始目录下的)
j=[0,0,0,0] #执行过的总文件数
total=[0,0,0,0] #执行过的文件夹的文件总数
ok=[0,0,0,0] #线程执行情况 完成后+1

def listsum(items):
    s=0
    for item in items:
        s+=item
    return s

def progress():
    t=0
    while(listsum(ok)!=4):
        print('总进度：%d / %d  ---  文件夹进度：%d / %d   --  用时： %.1f s'
                %(listsum(i),file_total,listsum(j),listsum(total),t*0.5))
        time.sleep(0.5)
        t+=1
    print('----图片移动完成！！！')
    f.close()


def find(filelist,new_path,tn):
    total[tn]+=len(filelist) #文件夹文件总数
    for item in filelist:
        j[tn]+=1
        newpath=os.path.join(new_path,item) #当前文件路径
        if os.path.isdir(newpath): #如果是目录
            if str(item) in ('横','竖','正'): 
                i[tn]+=1
                continue
            file_list = os.listdir(newpath) #Item这个目录下的文件列表
            if new_path==file_path: i[tn]+=1
            find(file_list,newpath,tn)
        
        if item.endswith(('.jpg','.png','.jpeg')):
            #计算图片长宽比函数
            #if new_path==file_path: i[tn]+=1 #想要总进度准确的话就开启这个
            try:
                img=Image.open(newpath)
            except:
                f_1.acquire()
                f.write('------图片损坏：'+newpath+'  --------\n')
                f_1.release()
                continue
            ratio=img.width/img.height
            img.close()
            if ratio>1.3:   #横的
                dst = os.path.join(file_path,'横', item)
            elif ratio<0.8: #竖的
                dst = os.path.join(file_path, '竖',item)
            else:  #正的
                dst = os.path.join(file_path, '正',item)
            try:
                os.rename(newpath,dst)
            except:
                f_1.acquire()
                f.write(newpath+'\n')
                f_1.release()
                continue
    if file_path==new_path: ok[tn]=1


def mT_find():
    print('选择了多线程！\n')
    n=int(file_total/4)
    list1,list2,list3,list4=folderlist[0:n],folderlist[n+1:2*n],folderlist[2*n+1:3*n],folderlist[3*n+1:]
    t1=threading.Thread(target=find,args=(list1,file_path,0,))
    t2=threading.Thread(target=find,args=(list2,file_path,1,))
    t3=threading.Thread(target=find,args=(list3,file_path,2,))
    t4=threading.Thread(target=find,args=(list4,file_path,3,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

if __name__ == '__main__':
    f = open(os.path.join(file_path,'error.txt'),'w')
    if not os.path.exists(os.path.join(file_path,'横')):
        os.mkdir(os.path.join(file_path,'横'))
    if not os.path.exists(os.path.join(file_path,'竖')):
        os.mkdir(os.path.join(file_path,'竖'))
    if not os.path.exists(os.path.join(file_path,'正')):
        os.mkdir(os.path.join(file_path,'正'))
    
    chose=input('按 1 开始，按 2 使用多线程:')
    tp=threading.Thread(target=progress)
    tp.start()
    if chose=='1':
        ok[1]=ok[2]=ok[3]=1
        find(folderlist,file_path,0)
    else:mT_find()
    