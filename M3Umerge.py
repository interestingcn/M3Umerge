#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project ：M3Umerge
@Date ：2020.02.27
'''

import time
import os
from multiprocessing import Pool
def welcome():
    msg = '''
============================================================================
.88b  d88. d8888b. db    db      .88b  d88. d88888b d8888b.  d888b  d88888b 
88'YbdP`88 VP  `8D 88    88      88'YbdP`88 88'     88  `8D 88' Y8b 88'     
88  88  88   oooY' 88    88      88  88  88 88ooooo 88oobY' 88      88ooooo 
88  88  88   ~~~b. 88    88      88  88  88 88~~~~~ 88`8b   88  ooo 88~~~~~ 
88  88  88 db   8D 88b  d88      88  88  88 88.     88 `88. 88. ~8~ 88.     
YP  YP  YP Y8888P' ~Y8888P'      YP  YP  YP Y88888P 88   YD  Y888P  Y88888P 
============================================================================
                     .m3u 文件快速合并工具
============================================================================
'''
    return msg

def displayMsg(workname='Default',msg=''):
    now = time.asctime( time.localtime(time.time()) )
    print(f'{now} - {workname}: ' + msg)

def endWith(fileName, *endstring):
    array = map(fileName.endswith, endstring)
    if True in array:
        return True
    else:
        return False

def m3u_filelist(path):
    fileList = os.listdir(path)
    files = []
    for filename in fileList:
        if endWith(filename, '.m3u'):
            files.append(filename)  # 所有m3u文件列表
    return files

def m3u_load(m3uFile):
    channel = {}
    errorNum = 0
    status = 0   # 实时改变步骤状态
    with open(m3uFile, 'r', encoding='utf8') as file:
        displayMsg('Master', f'{m3uFile} 已载入')
        for line in file:
            # 如果当前是描述行：
            if line.startswith('#EXTINF:-1'):
                if status !=0:
                    displayMsg('Master', f'{m3uFile}当前列表缺少行')
                    errorNum+=1
                    exit()
                channelInfo = str(line).replace('\n','')
                status = 1
            # 如果当前是URL行
            if line.startswith('http') or line.startswith('rtsp'): # 当前行为URL
                if status != 1:
                    displayMsg('m3u_load', f'{m3uFile} 解析完成')
                    errorNum += 1
                    exit()
                channel[channelInfo] = str(line).replace('\n','')
                status = 2
            # 上述判断完成
            if status == 2: # 上述步骤处理完毕
                status = 0
        displayMsg('Master', f'{m3uFile} 解析完毕')
        return channel

def work(m3u_data,outputFile,workname='Default'):
    for data in m3u_data:
        info = data + '\n' + m3u_data[data] + '\n'
        with open(outputFile, 'a',encoding='utf8') as file:
            file.write(info)
    displayMsg(workname,'文件写入成功！')

if __name__ == '__main__':
    print(welcome())
    outputFile = 'mergeFile.m3u'
    displayMsg('Master','正在读取文件列表：')
    fileList = m3u_filelist(os.getcwd())
    if outputFile in fileList:
        fileList.remove(outputFile)

    displayMsg('Master', f'正在写入 {outputFile} 文件头')
    with open(outputFile,'w',encoding='utf8') as file:
       file.write('#EXTM3U\n')

    p = Pool(2)
    for file in fileList:
        p.apply_async(work, args=(m3u_load(file),outputFile,file))
    p.close()
    p.join()
    displayMsg('Master','运行完毕!')
