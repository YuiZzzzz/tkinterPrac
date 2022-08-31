from tkinter import *
from tkinter import ttk             # ttk 提供更适合显示表格的视窗
from tkinter import filedialog      # filedialog 提供文件选择弹窗
from tkinter.messagebox import *

from PIL import Image               # 读取和保存图片
from csvio import *

import pandas

# 默认管理系统数据文件路径
DATA_PATH = 'data/data_list.csv'
# 默认的用户列表数据路径
IMG_PATH = 'data/images/'


# 管理系统主页
class RootPage(object):

    ##############################################################################
    # 构造函数

    def __init__(self, master=None):

        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小

        # 管理系统所需数据内容
        self.title = ['序号','物种','平均寿命', '食物', '行为', '叫声', '设计图']

        # 创建StringVar对象, 方便从界面中读取用户填入的数据
        self.name = StringVar()
        self.lifespan = StringVar()
        self.food = StringVar()
        self.hobby = StringVar()
        self.language = StringVar()
        self.design = StringVar()

        # 使用createPage方法, 加载界面
        self.createPage()

    ##############################################################################
    # 主界面
    # 创建管理界面, 实现GUI的组件和布局

    def createPage(self):

        # 在原本的root窗口上创建和放置frame_tv (frame treeview)
        self.frame_tv = Frame(self.root)
        self.frame_tv.pack()

        # 创建ttk的TreeView对象, 其中show='headings'参数的目的是为了格式整齐而隐藏首列
        self.tree = ttk.Treeview(self.frame_tv, show='headings', columns=['0', '1', '2', '3', '4', '5', '6'])

        # 监听tree中item被选中的事件
        self.tree.bind("<<TreeviewSelect>>", self.item_select)


        # 对TreeView对象添加Colunm
        title = self.title  # ['序号','物种','平均寿命', '食物', '行为', '叫声', '设计图']
        for i in range(len(title)):
            self.tree.heading(i, text=title[i]) # 设置heading
            self.tree.column(i, anchor='center', width=40 if i == 0 else 85)   # 设置栏目宽度 (序号栏为40px, 其他栏为85px)
                                                                               # 设置文字内容居中

        # 读取数据
        data = csv_read(DATA_PATH)

        # 向TreeView对象添加每一行数据
        for row in data:
            row = tuple(row)                            # 转换数据类型为tuple
            self.tree.insert(parent='', index='end', values=row)     # parent: 表格类型的Treeview, 填空字符串; 树形类型的Treeview，parent为父节点
                                                                     # index: 插入位置, 可以设置数字, 'end'代表末尾
        # 将TreeView对象放置到Frame上
        self.tree.pack()


        # 在原本的root窗口上创建和放置frame_op (frame operation)
        self.frame_op = Frame(self.root)
        self.frame_op.pack()

        # 所需按钮组件
        Button(self.frame_op, text='增加', command=self.add).grid(row=0, column=0, stick=W, pady=10)
        Button(self.frame_op, text='删除', command=self.delete).grid(row=0, column=1, stick=W, pady=10)
        Button(self.frame_op, text='修改', command=self.modify).grid(row=0, column=2, stick=W, pady=10)
        Button(self.frame_op, text='查询', command=self.search).grid(row=0, column=3, stick=W, pady=10)
        Button(self.frame_op, text='刷新', command=self.refresh).grid(row=0, column=4, stick=W, pady=10)


    # 刷新当前界面
    def refresh(self):
        self.frame_tv.destroy()     # 注销frame_tv, frame_op
        self.frame_op.destroy()
        self.createPage()           # 重新调用创建管理界面

    # # 监听并返回TreeView中被选中的项目
    def item_select(self, event):
        for select in self.tree.selection():
            return self.tree.item(select, "values")



    ##############################################################################
    # 管理系统 *添加* 功能

    def add(self):

        mode = 'add'
        self.top = Toplevel(width=500, height=800)      # 生成一个置顶窗口
        self.top.title(mode)                            # 设置窗口标题

        # 所有页面所需组件
        # 使用grid方法布局, 方便对齐
        Label(self.top).grid(row=0, stick=W)
        Label(self.top, text='物种: ').grid(row=1, stick=W, pady=10)
        Entry(self.top, textvariable=self.name).grid(row=1, column=1, stick=E)
        Label(self.top, text='平均寿命: ').grid(row=2, stick=W, pady=10)
        Entry(self.top, textvariable=self.lifespan).grid(row=2, column=1, stick=E)
        Label(self.top, text='食物: ').grid(row=3, stick=W, pady=10)
        Entry(self.top, textvariable=self.food).grid(row=3, column=1, stick=E)
        Label(self.top, text='喜好: ').grid(row=4, stick=W, pady=10)
        Entry(self.top, textvariable=self.hobby).grid(row=4, column=1, stick=E)
        Label(self.top, text='叫声: ').grid(row=5, stick=W, pady=10)
        Entry(self.top, textvariable=self.language).grid(row=5, column=1, stick=E)

        # 需要接收文件, 按钮显示'设计图待上传', 若已上传, 按钮显示文件名
        Label(self.top, text='设计图: ').grid(row=6, stick=W, pady=10)
        self.design.set('设计图待上传')
        # 点击按钮执行upload函数
        Button(self.top, textvariable=self.design, command=self.upload).grid(row=6, column=1, stick=E)

        # 点击按钮执行, 添加数据并刷新
        Button(self.top, text='确认', command=self.add_n_refresh).grid(row=7, stick=E, pady=10)


    # 添加数据并刷新
    def add_n_refresh(self):

        # 新数据项的id, 需要读取当前数据列表的长度
        id = len(csv_read(DATA_PATH))

        # 新数据项的一维列表
        info = [id, self.name.get(), self.lifespan.get(), self.food.get(),
                self.hobby.get(), self.language.get(), self.design.get()]

        # 写入新数据项
        csv_write(info, DATA_PATH)


        self.top.destroy()  # 关闭当前窗口
        self.refresh()      # 刷新root界面


    # 上传图片
    def upload(self):
        try:
            # 允许的图片后缀类型
            filetypes = [("PNG", "*.png"), ("JPG", "*.jpg"), ("GIF", "*.gif"), ("txt files", "*.txt"),
                         ('All files', '*')]

            # 弹出文件选择窗口, 返回该文件的完整路径
            filepath = filedialog.askopenfilename(title='选择图片',filetypes=filetypes)

            img = Image.open(filepath)              # 使用PIL的Image功能打开文件
            filename = filepath.split('/')[-1]      # 获得图片名称

            # 保存文件
            self.design.set(filename)
            img.save(IMG_PATH + filename)

        except Exception as e:
            print(e)


    ##############################################################################
    # delete
    # 管理系统 *删除* 功能窗口

    def delete(self):

        # 声明cur_data参数
        cur_data = None

        # 检查选中的数据行
        for select in self.tree.selection():
            cur_data = list(self.tree.item(select, "values"))

        # 如果未选中任何数据行, 弹出提示
        if not cur_data:
            showinfo(title='提示', message='请选择要删除的物种')
        # 获得选中的数据行的index值
        else:
            self.ind = int(cur_data[0])

            # 删除前弹窗提示, 询问是否删除
            result = askyesno(title='delet', message='是否删除物种'+cur_data[1]+'?')
            # 选择为'是', result变量为True时
            if result:
                csv_delete(self.ind, DATA_PATH)     # 从csv文件中删除数据
                self.refresh()                      # 刷新root界面



    ##############################################################################
    # modify
    # 管理系统 *修改* 功能窗口

    def modify(self):

        # 声明cur_data参数
        cur_data = None

        # 检查选中的数据行
        for select in self.tree.selection():
            cur_data = list(self.tree.item(select, "values"))

        # 如果未选中任何数据行, 弹出提示
        if not cur_data:
            showinfo(title='提示', message='请选择要修改的物种')

        # 获得选中的数据行的index值, 从数据行中读取并赋给当前name值
        else:
            self.ind = int(cur_data[0])
            self.name = StringVar()
            self.name.set(cur_data[1])
            self.lifespan = StringVar()
            self.lifespan.set(cur_data[2])
            self.food = StringVar()
            self.food.set(cur_data[3])
            self.hobby = StringVar()
            self.hobby.set(cur_data[4])
            self.design = StringVar()
            self.design.set(cur_data[5])

            mode = 'modify'
            self.top = Toplevel(width=500, height=800)      # 生成一个置顶窗口
            self.top.title(mode)                            # 设置窗口标题

            # 所有页面所需组件
            # 使用grid方法布局, 方便对齐
            Label(self.top).grid(row=0, stick=W)
            Label(self.top, text='物种: ').grid(row=1, stick=W, pady=10)
            Entry(self.top, textvariable=self.name).grid(row=1, column=1, stick=E)
            Label(self.top, text='平均寿命: ').grid(row=2, stick=W, pady=10)
            Entry(self.top, textvariable=self.lifespan).grid(row=2, column=1, stick=E)
            Label(self.top, text='食物: ').grid(row=3, stick=W, pady=10)
            Entry(self.top, textvariable=self.food).grid(row=3, column=1, stick=E)
            Label(self.top, text='喜好: ').grid(row=4, stick=W, pady=10)
            Entry(self.top, textvariable=self.hobby).grid(row=4, column=1, stick=E)
            Label(self.top, text='叫声: ').grid(row=5, stick=W, pady=10)
            Entry(self.top, textvariable=self.language).grid(row=5, column=1, stick=E)

            # 需要接收文件, 按钮显示'设计图待上传', 若已上传, 按钮显示文件名
            Label(self.top, text='设计图: ').grid(row=6, stick=W, pady=10)
            self.design.set('设计图待上传')
            # 点击按钮执行upload函数
            Button(self.top, textvariable=self.design, command=self.upload).grid(row=6, column=1, stick=E)

            # 点击按钮执行, 修改数据并刷新
            Button(self.top, text='确认', command=self.modify_n_refresh).grid(row=7, stick=E, pady=10)


    # 修改数据并刷新
    def modify_n_refresh(self):

        # 修改后数据项的一维列表
        info = [self.ind, self.name.get(), self.lifespan.get(), self.food.get(),
                self.hobby.get(), self.language.get(), self.design.get()]

        # 修改数据项
        csv_modify(info, self.ind, DATA_PATH)

        self.top.destroy()  # 关闭当前窗口
        self.refresh()  # 刷新root界面


    ##############################################################################
    # search
    # 管理系统 *查询* 功能窗口

    def search(self):

        mode = 'modify'
        self.top = Toplevel(width=500, height=800)  # 生成一个置顶窗口
        self.top.title(mode)  # 设置窗口标题

        # 简单搜索界面
        Label(self.top).grid(row=0, stick=W)
        Label(self.top, text='搜索物种: ').grid(row=1, stick=W, pady=10)
        Entry(self.top, textvariable=self.name).grid(row=1, column=1, stick=E)
        Button(self.top, text='确认', command=self.search_n_display).grid(row=2, column=1, stick=E)


    # 搜索并展示条目
    def search_n_display(self):

        # 从csv文件中找出条目
        result = csv_search(self.name.get(), DATA_PATH)
        # 如果未找到, 弹出提示
        if not result:
            showinfo(title='未找到', message='管理系统中不存在此物种')

        # 如果找到, 弹出新界面, 展示条目信息
        else:
            self.top.destroy()
            self.refresh()  # 刷新root界面
            self.top = Toplevel(width=600, height=1000)  # 生成一个置顶窗口
            self.top.title(result[1])  # 设置窗口标题

            # 所有页面所需组件
            # 使用grid方法布局, 方便对齐
            Label(self.top).grid(row=0, stick=W)
            Label(self.top, text='物种: ').grid(row=1, stick=W, pady=10)
            Label(self.top, text=result[1]).grid(row=1, column=1, stick=E)
            Label(self.top, text='平均寿命: ').grid(row=2, stick=W, pady=10)
            Label(self.top, text=result[2]).grid(row=2, column=1, stick=E)
            Label(self.top, text='食物: ').grid(row=3, stick=W, pady=10)
            Label(self.top, text=result[3]).grid(row=3, column=1, stick=E)
            Label(self.top, text='喜好: ').grid(row=4, stick=W, pady=10)
            Label(self.top, text=result[4]).grid(row=4, column=1, stick=E)
            Label(self.top, text='叫声: ').grid(row=5, stick=W, pady=10)
            Label(self.top, text=result[5]).grid(row=5, column=1, stick=E)

            # 暂未实现显示图片
            Label(self.top, text='设计图: ').grid(row=6, stick=W, pady=10)
            Label(self.top, text='保存地址:'+result[6]).grid(row=6, column=1, stick=E)








