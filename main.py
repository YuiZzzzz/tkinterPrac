
from tkinter import *
from login import LoginPage

# 创建tk窗口对象
root = Tk()
# 设置窗口标题
root.title('上帝造物管理系统')

# 创建登录窗口, 具体构造方法见login.py
LoginPage(root)

# 开始运行窗口
root.mainloop()