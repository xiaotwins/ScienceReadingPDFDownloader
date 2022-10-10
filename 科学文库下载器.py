from alive_progress import alive_bar as ps
from json import loads as ls
from re import compile as ce
from re import findall as fl
from requests import get as gt
from requests import post as pt
from os import listdir as lr
from os import system as sm

for i in lr():
    if '.pdf' in i:
        if input('输入y以删除PDF: ') == 'y': sm('del *.pdf')
        break

with open('科学文库下载列表.txt', 'r', encoding='utf-8') as f:
    Signal = f.read().split("\n")
    for i in range(len(Signal)):
        if (len(Signal[i])) == 0 or 'book.sciencereading.cn' not in Signal[i]: continue
        if 'href' not in Signal[i]: bookID = Signal[i].split('=')[1]
        else: bookID = Signal[i].split('"')[3].split('=')[1]
        if '&' in bookID: bookID = bookID.split('&')[0]
        bookName = fl(ce('<title>.*?</title>'), gt('https://book.sciencereading.cn/shop/book/Booksimple/show.do?id=' + bookID).text)[0].split('<')[1].split('>')[1]
        if bookName + '.pdf' in lr():
            print(bookName + '存在,跳过')
            continue
        with ps(2) as Go:
            print('正在等待目标服务器应答...')
            bookFileID = ls(pt('https://wkobwp.sciencereading.cn/api/file/add?params=%7B%22params%22%3A%7B%22file%22%3A%22http%3A%2F%2F159.226.241.32%3A81%2F' + bookID + '.pdf%22%7D%7D').text)['result']
            if bookFileID == 'OutOfFileSizeLimit': input(bookName + ',无法下载,按回车键以继续...')
            else:
                print('保存中...')
                Go()
                bookName = bookName.replace(":", "：")
                bookName = bookName.replace("|", "-")
                open(bookName + '.pdf', 'wb').write(gt('https://wkobwp.sciencereading.cn/api/file/' + bookFileID + '/getDocumentbuffer.pdf').content)
                Go()
                print('另存为: ' + bookName + '.pdf')
               
open('科学文库下载列表.txt', 'w', encoding='utf-8').truncate(0)