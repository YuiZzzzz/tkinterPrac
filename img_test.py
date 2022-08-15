from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *


# 创建tk窗口对象
root = Tk()
# 设置窗口标题
root.title('上帝造物管理系统')

img_path = 'data/images/emoji_cake.gif'
img_gif = PhotoImage(file = img_path)
Label(root, image = img_gif).grid(row=0, padx=50, pady=50)


# 开始运行窗口
root.mainloop()