from tkinter import *
from tkinter.messagebox import *
from root import RootPage
from csvio import *

# 默认的用户列表数据路径
USER_PATH = 'data/user_list.csv'

# 登录页
class LoginPage(object):

    # 构造函数
    def __init__(self, master=None):

        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小

        # 创建StringVar对象, 方便从界面中读取用户填入的数据
        self.username = StringVar()
        self.password = StringVar()

        # 使用createPage方法, 加载界面
        self.createPage()


    # 创建登陆界面, 实现GUI的组件和布局
    def createPage(self):

        # 在原本的root窗口上创建和放置frame
        # (可以理解为, 相当于HTML在body标签下创建的div标签)
        self.page = Frame(self.root)
        self.page.pack()

        # 所有页面所需组件
        # 使用grid方法布局, 方便对齐
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E) # textvariable=self.username 接收用户输入的用户名

        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E) # textvariable=self.username 接收用户输入的密码, show='*'字符显示为星号

        Button(self.page, text='登录', command=self.loginCheck).grid(row=3, stick=W, pady=10) # command参数绑定点击后执行的函数
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=1, stick=E) # command参数绑定self.page.quit 退出界面


    # 登录函数, 点击登录按钮时执行
    def loginCheck(self):

        # 获取输入框中用户的输入
        username = self.username.get()  # get功能针对StringVar对象获取数据
        pwd = self.password.get()

        # 读取用户数据csv, 转换为字典方便搜索
        user_list = csv_read(USER_PATH)
        user_dict = {k: v for [k, v] in user_list}

        # 登录检验
        if username in user_dict.keys():

            # 登录成功
            if pwd == user_dict[username]:
                # 注销当前页面
                self.page.destroy()
                # 创建主窗口, 具体构造方法见root.py
                RootPage(self.root)

            # 登录失败, 弹窗提示密码错误
            else:
                showinfo(title='错误', message='密码错误！')

        # 如果未找到此用户名, 直接提示用户注册
        else:
            # 弹窗提示是否注册账号, 弹窗中有是否选项
            # 选'是'返回值为True, 选'否'返回值为False并且不执行任何操作
            result = askyesno(title='注册', message='不存在此用户名, 是否为您注册账号?')

            # 如果用户选择注册
            if result:

                # csv写入
                csv_write([username, pwd], USER_PATH) # csv读写函数逻辑另见csvio.py

                # 注销当前页面
                self.page.destroy()
                # 创建主窗口, 具体构造方法见root.py
                RootPage(self.root)






