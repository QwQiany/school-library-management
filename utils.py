import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class TableFrame(ttk.Frame):
    """创建一个带有滚动条的表格框架"""
    def __init__(self, parent, columns, headings, **kwargs):
        super().__init__(parent, **kwargs)
        
        # 创建Treeview
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # 设置列标题
        for i, heading in enumerate(headings):
            self.tree.heading(columns[i], text=heading)
            self.tree.column(columns[i], width=100)  # 默认列宽
        
        # 创建滚动条
        self.scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        # 配置Treeview的滚动
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # 配置网格权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def clear(self):
        """清空表格内容"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def add_row(self, values):
        """添加一行数据"""
        self.tree.insert('', 'end', values=values)
    
    def get_selected_item(self):
        """获取选中的行"""
        selected_items = self.tree.selection()
        if selected_items:
            return self.tree.item(selected_items[0])
        return None
    
    def get_all_items(self):
        """获取所有行"""
        items = []
        for item in self.tree.get_children():
            items.append(self.tree.item(item))
        return items

class EntryDialog(tk.Toplevel):
    """创建一个输入对话框"""
    def __init__(self, parent, title, fields, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title(title)
        self.result = None
        self.fields = fields
        self.entries = {}
        
        # 创建输入框
        for i, (field, label) in enumerate(fields.items()):
            ttk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entries[field] = entry
        
        # 创建按钮
        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 设置模态
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_ok(self):
        """确定按钮点击事件"""
        self.result = {field: entry.get() for field, entry in self.entries.items()}
        self.destroy()
    
    def on_cancel(self):
        """取消按钮点击事件"""
        self.destroy()

class ComboBoxDialog(tk.Toplevel):
    """创建一个下拉选择对话框"""
    def __init__(self, parent, title, label, values, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title(title)
        self.result = None
        
        # 创建标签和下拉框
        ttk.Label(self, text=label).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.combo = ttk.Combobox(self, values=values)
        self.combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # 创建按钮
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 设置模态
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_ok(self):
        """确定按钮点击事件"""
        self.result = self.combo.get()
        self.destroy()
    
    def on_cancel(self):
        """取消按钮点击事件"""
        self.destroy()

def show_error(message):
    """显示错误消息"""
    messagebox.showerror("错误", message)

def show_info(message):
    """显示信息消息"""
    messagebox.showinfo("信息", message)

def show_warning(message):
    """显示警告消息"""
    messagebox.showwarning("警告", message)

def format_date(date_str):
    """格式化日期字符串"""
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%Y-%m-%d')
    except:
        return date_str

def format_money(amount):
    """格式化金额"""
    try:
        return f"¥{float(amount):.2f}"
    except:
        return amount 