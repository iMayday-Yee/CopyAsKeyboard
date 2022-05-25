print("特别说明:")
print("本代码仅用于个人学习使用，其他用途造成任何损失，与作者无关。\n\n")

from pynput.keyboard import Controller, Key, Listener
import win32clipboard as wc
import threading
import time
from threading import Lock
kb = Controller()
#设置打印快捷键
CHCKKEY = "@@@"
#设置复制最长长度
MAXSIZE = 10000
#设置同步锁
lock = Lock()

#创建标志队列用于 存放验证关键字
class FQueue:
    def __init__(self, size):
        self.size = size
        self.list = []

    def append(self, el):
        if len(self.list) == self.size:
            newList = []
            for i in range(1, self.size):
                newList.append(self.list[i])

            newList.append(el)
            self.list = newList
        else:
            self.list.append(el)

    def check(self, str):
        if (len(self.list) < 3):
            return False
        Flag = True
        for i in range(self.size):
            if self.list[i] != str[i]:
                Flag = False;

        return Flag

    def clear(self):
        self.list = []
queue = FQueue(3)
# 监听按压
def on_press(key):
    try:
        # print("正在按压:", format(key.char))
        if format(key.char) != None:
            queue.append(format(key.char))
            if (queue.check(CHCKKEY)):
                process()

    except AttributeError:
     #   print("正在按压:", format(key))
      pass


# 内容处理
def process():
    lock.acquire()
    queue.clear()
    content = getCopyTxet()
    if len(content) > MAXSIZE:
        print("超出处理最大长度。。。不给予处理!!!!")
        return None
    list_text = split_content(content)
    time.sleep(1)
    i=0;
    for line in list_text:
        if CHCKKEY in line:
            print(line + "内容不合法请重新设置")
            return
        else:
            print(line)
            if i==0:
              delete_ckeckkey()
            outLine(line)

        i=i+1;
    lock.release()


#清楚打印CHECK
def delete_ckeckkey():
    time.sleep(0.7)
    for i in range(len(CHCKKEY)):
        kb.press(Key.backspace)
#开始模拟键盘输出打印
def outLine(line):
    list=line.split("\n")
    for el in list:
        kb.type(el)

#内容分割防止内容过大
def split_content(content, width=100):
    list = []
    lenth = len(content);
    # 太小的话直接处理
    if lenth < width:
        list.append(content)
        return list

    if (lenth % width) == 0:
        n = int(lenth / width);
    else:
        n = int(lenth / width) + 1;

    for i in range(n):
        if i == n - 1:

            if lenth % width == 0:
                list.append(content[i * width:(i + 1) * width])
            else:
                list.append(content[i * width:i * width + (lenth % width)])
        else:
            list.append(content[i * width:(i + 1) * width])
    return list


# 监听释放
def on_release(key):
    # print("已经释放:", format(key))

    if key == Key.esc:
        # 停止监听
        return False


# 开始监听
def start_listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 获取粘贴板里的内容
def getCopyTxet():
    wc.OpenClipboard()
    copytxet = wc.GetClipboardData()
    wc.CloseClipboard()
    return str(copytxet)


# **********
# 源码阅读指示
#
# start_listen()--》on_press(key)--》process()--》 outLine(line)
#
# **********
if __name__ == '__main__':
    print("欢迎使用，请将内容复制进粘贴板，按住@@@开始打印复制。。。")
    start_listen()