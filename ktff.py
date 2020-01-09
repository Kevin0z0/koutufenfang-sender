import win32api
import win32con
import win32gui
from json import load
from time import sleep
import win32com.client
from transcoding import *
import win32clipboard as cp


class KTFF:
    def __init__(self, name):
        self.setting = load(open("settings.json","r"))
        self.sleep = self.setting["sleep"]
        self.name = name
        #获取句柄
        while 1:
            self.handle = win32gui.FindWindow(None,self.name)
            if self.handle == 0:
                print("[!] 未发现窗口")
                self.name = input("> 请重新输入窗口的名称: ")
                continue
            self.f = trans(self.setting["file"])
            break

    def __copymsg(self,msg):
        '''复制消息至粘贴板'''
        cp.OpenClipboard()
        cp.EmptyClipboard()
        cp.SetClipboardData(win32con.CF_UNICODETEXT, msg)
        cp.CloseClipboard()

    def __ishide(self):
        '''判断是否为最小化的窗口'''
        a = 0
        for i in win32gui.GetWindowRect(self.handle):
            if i < 0:
                a += 1
        if a == 4:
            return True
        return False

    def __foreground(self):
        '''恢复窗口最小化'''
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SendMessage(self.handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(self.handle)
        except:
            error("[!] 窗口获取失败，请将窗口最小化之后重新尝试")

    def __random_data(self):
        a = [i for i in range(len(self.f))]
        if self.setting["random"]:
            from random import shuffle
            shuffle(a)
        return a

    def send(self):
        win32api.keybd_event(17, 0, 0, 0)
        sleep(0.05)
        win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, 86, 0)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        sleep(0.05)
        win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

    def analyze(self):
        self.__foreground()
        self.sequence = self.__random_data()

    def run(self):
        num = 0
        length = len(self.f)
        while 1:
            self.__copymsg(self.f[self.sequence[num]])
            self.send()
            num += 1
            if num >= length:
                if self.setting["cycle"]:
                    num = 0
                    self.analyze()
                    print("> 已开始重复发送")
                else:
                    error("> 已停止发送")
            sleep(self.sleep)


if __name__ == '__main__':
    print("""
                        ,----,                       
           ,--.       ,/   .`|                       
       ,--/  /|     ,`   .'  :     ,---,.     ,---,. 
    ,---,': / '   ;    ;     /   ,'  .' |   ,'  .' | 
    :   : '/ /  .'___,/    ,'  ,---.'   | ,---.'   | 
    |   '   ,   |    :     |   |   |   .' |   |   .' 
    '   |  /    ;    |.';  ;   :   :  :   :   :  :   
    |   ;  ;    `----'  |  |   :   |  |-, :   |  |-, 
    :   '   \       '   :  ;   |   :  ;/| |   :  ;/| 
    |   |    '      |   |  '   |   |   .' |   |   .' 
    '   : |.  \     '   :  |   '   :  '   '   :  '   
    |   | '_\.'     ;   |.'    |   |  |   |   |  |   
    '   : |         '---'      |   :  \   |   :  \   
    ;   |,'                    |   | ,'   |   | ,'   
    '---'                      `----'     `----'     


    若没有发送消息请点击消息输入框后运行程序
    """)
    k = KTFF(input("> 请输入窗口的名称: "))
    k.analyze()
    k.run()
