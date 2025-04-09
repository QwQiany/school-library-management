import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# 导入自定义模块
from db_operations import DatabaseOperations
from utils import TableFrame, EntryDialog, ComboBoxDialog, show_error, show_info, show_warning, format_date, format_money

# 导入功能模块
from book_management import BookManagementFrame, CategoryManagementFrame, PublisherManagementFrame
from reader_management import ReaderManagementFrame, BorrowHistoryWindow
from borrow_management import BorrowManagementFrame, ReturnManagementFrame, RenewManagementFrame
from fine_management import FineManagementFrame
from query_management import BookQueryFrame, BorrowQueryFrame, ReaderHistoryFrame

class SchoolLibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("学校图书借阅管理系统")
        self.root.geometry("1200x700")
        
        # 初始化数据库操作
        self.db = DatabaseOperations()
        
        # 创建菜单
        self.create_menu()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建欢迎标签
        welcome_label = ttk.Label(
            self.main_frame, 
            text="欢迎使用学校图书借阅管理系统", 
            font=("Arial", 24)
        )
        welcome_label.pack(pady=50)
        
        # 创建功能按钮
        self.create_function_buttons()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 图书管理菜单
        book_menu = tk.Menu(menubar, tearoff=0)
        book_menu.add_command(label="图书信息管理", command=self.show_book_management)
        book_menu.add_command(label="图书类别管理", command=self.show_category_management)
        book_menu.add_command(label="出版社管理", command=self.show_publisher_management)
        menubar.add_cascade(label="图书管理", menu=book_menu)
        
        # 读者管理菜单
        reader_menu = tk.Menu(menubar, tearoff=0)
        reader_menu.add_command(label="读者信息管理", command=self.show_reader_management)
        menubar.add_cascade(label="读者管理", menu=reader_menu)
        
        # 借阅管理菜单
        borrow_menu = tk.Menu(menubar, tearoff=0)
        borrow_menu.add_command(label="借阅管理", command=self.show_borrow_management)
        borrow_menu.add_command(label="归还管理", command=self.show_return_management)
        borrow_menu.add_command(label="续借管理", command=self.show_renew_management)
        menubar.add_cascade(label="借阅管理", menu=borrow_menu)
        
        # 罚款管理菜单
        fine_menu = tk.Menu(menubar, tearoff=0)
        fine_menu.add_command(label="罚款管理", command=self.show_fine_management)
        menubar.add_cascade(label="罚款管理", menu=fine_menu)
        
        # 查询菜单
        query_menu = tk.Menu(menubar, tearoff=0)
        query_menu.add_command(label="图书信息查询", command=self.show_book_query)
        query_menu.add_command(label="借阅信息查询", command=self.show_borrow_query)
        query_menu.add_command(label="读者借阅历史", command=self.show_reader_history)
        menubar.add_cascade(label="查询", menu=query_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_function_buttons(self):
        """创建功能按钮"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        # 创建按钮网格
        buttons = [
            ("图书信息管理", self.show_book_management),
            ("读者信息管理", self.show_reader_management),
            ("借阅管理", self.show_borrow_management),
            ("归还管理", self.show_return_management),
            ("续借管理", self.show_renew_management),
            ("罚款管理", self.show_fine_management),
            ("图书信息查询", self.show_book_query),
            ("借阅信息查询", self.show_borrow_query),
            ("读者借阅历史", self.show_reader_history)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.grid(row=row, column=col, padx=10, pady=10)
    
    def clear_main_frame(self):
        """清空主框架"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    # 图书管理相关方法
    def show_book_management(self):
        """显示图书信息管理界面"""
        self.clear_main_frame()
        BookManagementFrame(self.main_frame, self.db)
    
    def show_category_management(self):
        """显示图书类别管理界面"""
        self.clear_main_frame()
        CategoryManagementFrame(self.main_frame, self.db)
    
    def show_publisher_management(self):
        """显示出版社管理界面"""
        self.clear_main_frame()
        PublisherManagementFrame(self.main_frame, self.db)
    
    # 读者管理相关方法
    def show_reader_management(self):
        """显示读者信息管理界面"""
        self.clear_main_frame()
        ReaderManagementFrame(self.main_frame, self.db)
    
    # 借阅管理相关方法
    def show_borrow_management(self):
        """显示借阅管理界面"""
        self.clear_main_frame()
        BorrowManagementFrame(self.main_frame, self.db)
    
    def show_return_management(self):
        """显示归还管理界面"""
        self.clear_main_frame()
        ReturnManagementFrame(self.main_frame, self.db)
    
    def show_renew_management(self):
        """显示续借管理界面"""
        self.clear_main_frame()
        RenewManagementFrame(self.main_frame, self.db)
    
    # 罚款管理相关方法
    def show_fine_management(self):
        """显示罚款管理界面"""
        self.clear_main_frame()
        FineManagementFrame(self.main_frame, self.db)
    
    # 查询相关方法
    def show_book_query(self):
        """显示图书信息查询界面"""
        self.clear_main_frame()
        BookQueryFrame(self.main_frame, self.db)
    
    def show_borrow_query(self):
        """显示借阅信息查询界面"""
        self.clear_main_frame()
        BorrowQueryFrame(self.main_frame, self.db)
    
    def show_reader_history(self):
        """显示读者借阅历史界面"""
        self.clear_main_frame()
        ReaderHistoryFrame(self.main_frame, self.db)
    
    # 帮助相关方法
    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(
            "关于", 
            "学校图书借阅管理系统\n\n"
            "版本: 1.0\n"
            "作者: 谢毓珩 苏淏飏\n"
            "日期: 2025年4月\n\n"
            "本系统用于管理学校图书馆的图书借阅、归还、续借等业务。"
        )

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolLibrarySystem(root)
    root.mainloop()