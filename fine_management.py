import tkinter as tk
from tkinter import ttk, messagebox
from utils import TableFrame, EntryDialog, ComboBoxDialog, show_error, show_info, show_warning, format_money

class FineManagementFrame(ttk.Frame):
    """罚款管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="罚款管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加罚款", command=self.add_fine).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('罚款记录号', '借阅记录编号', '罚款金额')
        headings = ('罚款记录号', '借阅记录编号', '罚款金额')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有罚款记录
        fines = self.db.get_all_fines()
        if not fines:
            return
        
        # 添加数据到表格
        for fine in fines:
            self.table.add_row((
                fine['罚款记录号'],
                fine['借阅记录编号'],
                format_money(fine['罚款金额'])
            ))
    
    def add_fine(self):
        """添加罚款"""
        # 获取所有借阅记录
        borrow_records = self.db.get_all_borrow_records()
        if not borrow_records:
            show_error("没有可用的借阅记录")
            return
        
        # 过滤出已归还的记录
        returned_records = [record for record in borrow_records if record['归还日期'] is not None]
        
        if not returned_records:
            show_error("没有已归还的借阅记录")
            return
        
        # 创建借阅记录选择对话框
        record_values = [f"{record['借阅记录编号']} - {record['索书号']} (归还日期: {record['归还日期']})" for record in returned_records]
        record_dialog = ComboBoxDialog(self, "选择借阅记录", "请选择借阅记录:", record_values)
        self.wait_window(record_dialog)
        
        if not record_dialog.result:
            return
        
        # 获取借阅记录ID
        borrow_id = record_dialog.result.split(' - ')[0]
        
        # 检查是否已有罚款记录
        existing_fine = self.db.get_fine_by_borrow_id(borrow_id)
        if existing_fine:
            show_error("该借阅记录已有罚款记录")
            return
        
        # 创建输入对话框
        fields = {
            '罚款金额': '罚款金额:'
        }
        
        dialog = EntryDialog(self, "添加罚款", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 创建罚款数据
                fine_data = {
                    '借阅记录编号': int(borrow_id),
                    '罚款金额': float(dialog.result['罚款金额'])
                }
                
                # 添加罚款
                result = self.db.add_fine(fine_data)
                if result:
                    show_info("添加罚款成功")
                    self.refresh()
                else:
                    show_error("添加罚款失败")
            except ValueError:
                show_error("请输入有效的数字")
            except Exception as e:
                show_error(f"添加罚款时出错: {str(e)}") 