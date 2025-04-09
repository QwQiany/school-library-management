import tkinter as tk
from tkinter import ttk, messagebox
from utils import TableFrame, EntryDialog, show_error, show_info, show_warning
from borrow_management import BorrowHistoryWindow

class ReaderManagementFrame(ttk.Frame):
    """读者信息管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="读者信息管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加读者", command=self.add_reader).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑读者", command=self.edit_reader).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除读者", command=self.delete_reader).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="查看借阅历史", command=self.view_borrow_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('读者卡号', '姓名', '证件号')
        headings = ('读者卡号', '姓名', '证件号')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有读者
        readers = self.db.get_all_readers()
        if not readers:
            return
        
        # 添加数据到表格
        for reader in readers:
            self.table.add_row((
                reader['读者卡号'],
                reader['姓名'],
                reader['证件号']
            ))
    
    def add_reader(self):
        """添加读者"""
        # 创建输入对话框
        fields = {
            '读者卡号': '读者卡号:',
            '姓名': '姓名:',
            '证件号': '证件号:'
        }
        
        dialog = EntryDialog(self, "添加读者", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 创建读者数据
                reader_data = {
                    '读者卡号': dialog.result['读者卡号'],
                    '姓名': dialog.result['姓名'],
                    '证件号': dialog.result['证件号']
                }
                
                # 添加读者
                result = self.db.add_reader(reader_data)
                if result:
                    show_info("添加读者成功")
                    self.refresh()
                else:
                    show_error("添加读者失败")
            except Exception as e:
                show_error(f"添加读者时出错: {str(e)}")
    
    def edit_reader(self):
        """编辑读者"""
        # 获取选中的读者
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要编辑的读者")
            return
        
        # 获取读者数据
        values = selected_item['values']
        reader_id = values[0]
        
        # 获取读者详细信息
        reader = self.db.get_reader_by_id(reader_id)
        if not reader:
            show_error("获取读者信息失败")
            return
        
        # 创建输入对话框
        fields = {
            '读者卡号': '读者卡号:',
            '姓名': '姓名:',
            '证件号': '证件号:'
        }
        
        dialog = EntryDialog(self, "编辑读者", fields)
        
        # 设置当前值
        dialog.entries['读者卡号'].insert(0, reader['读者卡号'])
        dialog.entries['姓名'].insert(0, reader['姓名'])
        dialog.entries['证件号'].insert(0, reader['证件号'])
        
        # 禁用读者卡号编辑
        dialog.entries['读者卡号'].config(state='disabled')
        
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 创建读者数据
                reader_data = {
                    '读者卡号': reader['读者卡号'],  # 使用原始读者卡号
                    '姓名': dialog.result['姓名'],
                    '证件号': dialog.result['证件号']
                }
                
                # 更新读者
                result = self.db.update_reader(reader_data)
                if result:
                    show_info("更新读者成功")
                    self.refresh()
                else:
                    show_error("更新读者失败")
            except Exception as e:
                show_error(f"更新读者时出错: {str(e)}")
    
    def delete_reader(self):
        """删除读者"""
        # 获取选中的读者
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要删除的读者")
            return
        
        # 获取读者ID
        values = selected_item['values']
        reader_id = values[0]
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除读者 '{values[1]}' 吗？"):
            # 删除读者
            result = self.db.delete_reader(reader_id)
            if result:
                show_info("删除读者成功")
                self.refresh()
            else:
                show_error("删除读者失败")
    
    def view_borrow_history(self):
        """查看借阅历史"""
        # 获取选中的读者
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要查看借阅历史的读者")
            return
        
        # 获取读者ID
        values = selected_item['values']
        reader_id = values[0]
        
        # 创建借阅历史窗口
        BorrowHistoryWindow(self, self.db, reader_id, values[1]) 