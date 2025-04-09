import tkinter as tk
from tkinter import ttk, messagebox
from utils import TableFrame, EntryDialog, ComboBoxDialog, show_error, show_info, show_warning, format_date

class BorrowManagementFrame(ttk.Frame):
    """借阅管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="借阅管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="借阅图书", command=self.borrow_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        headings = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有借阅记录
        borrow_records = self.db.get_all_borrow_records()
        if not borrow_records:
            return
        
        # 添加数据到表格
        for record in borrow_records:
            self.table.add_row((
                record['借阅记录编号'],
                record['读者卡号'],
                record['索书号'],
                format_date(record['借阅日期']),
                format_date(record['应还日期']),
                format_date(record['归还日期']) if record['归还日期'] else '未归还'
            ))
    
    def borrow_book(self):
        """借阅图书"""
        # 获取所有读者
        readers = self.db.get_all_readers()
        if not readers:
            show_error("没有可用的读者")
            return
        
        # 获取所有可借阅的图书
        books = self.db.get_all_books()
        available_books = [book for book in books if book['在库数量'] > 0]
        
        if not available_books:
            show_error("没有可借阅的图书")
            return
        
        # 创建读者选择对话框
        reader_values = [f"{reader['读者卡号']} - {reader['姓名']}" for reader in readers]
        reader_dialog = ComboBoxDialog(self, "选择读者", "请选择读者:", reader_values)
        self.wait_window(reader_dialog)
        
        if not reader_dialog.result:
            return
        
        # 获取读者ID
        reader_id = reader_dialog.result.split(' - ')[0]
        
        # 创建图书选择对话框
        book_values = [f"{book['索书号']} - {book['书名']} (在库: {book['在库数量']})" for book in available_books]
        book_dialog = ComboBoxDialog(self, "选择图书", "请选择图书:", book_values)
        self.wait_window(book_dialog)
        
        if not book_dialog.result:
            return
        
        # 获取图书ID
        book_id = book_dialog.result.split(' - ')[0]
        
        # 调用借书存储过程
        result = self.db.borrow_book(reader_id, book_id)
        
        try:
            if result and len(result) >= 1:
                for res_set in result:
                    if len(res_set) > 0 and isinstance(res_set[0], dict):
                        output_params = res_set[0]
                        success = output_params.get('p_success', False)
                        message = output_params.get('p_message', '')
                        
                        if success:
                            show_info(message)
                            self.refresh()
                        else:
                            show_error(message)
                        return
                        
            show_error("借阅图书失败: 未能获取操作结果")
        except Exception as e:
            show_error(f"借阅图书失败: {str(e)}")

class ReturnManagementFrame(ttk.Frame):
    """归还管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="归还管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="归还图书", command=self.return_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        headings = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有未归还的借阅记录
        borrow_records = self.db.get_all_borrow_records()
        if not borrow_records:
            return
        
        # 过滤出未归还的记录
        unreturned_records = [record for record in borrow_records if record['归还日期'] is None]
        
        # 添加数据到表格
        for record in unreturned_records:
            self.table.add_row((
                record['借阅记录编号'],
                record['读者卡号'],
                record['索书号'],
                format_date(record['借阅日期']),
                format_date(record['应还日期']),
                '未归还'
            ))
    
    def return_book(self):
        """归还图书"""
        # 获取选中的借阅记录
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要归还的图书")
            return
        
        # 获取借阅记录ID
        values = selected_item['values']
        borrow_id = values[0]
        
        # 确认归还
        if messagebox.askyesno("确认归还", f"确定要归还图书 '{values[2]}' 吗？"):
            # 调用还书存储过程
            result = self.db.return_book(borrow_id)
            
            try:
                if result and len(result) >= 1:
                    for res_set in result:
                        if len(res_set) > 0 and isinstance(res_set[0], dict):
                            output_params = res_set[0]
                            success = output_params.get('p_success', False)
                            message = output_params.get('p_message', '')
                            fine = output_params.get('p_fine_amount', 0)
                            
                            if success:
                                if fine > 0:
                                    show_warning(f"{message}\n需缴纳罚款: ¥{fine:.2f}")
                                else:
                                    show_info(message)
                                self.refresh()
                            else:
                                show_error(message)
                            return
                            
                show_error("归还图书失败: 未能获取操作结果")
            except Exception as e:
                show_error(f"归还图书失败: {str(e)}")

class RenewManagementFrame(ttk.Frame):
    """续借管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="续借管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="续借图书", command=self.renew_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        headings = ('借阅记录编号', '读者卡号', '索书号', '借阅日期', '应还日期', '归还日期')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有未归还的借阅记录
        borrow_records = self.db.get_all_borrow_records()
        if not borrow_records:
            return
        
        # 过滤出未归还的记录
        unreturned_records = [record for record in borrow_records if record['归还日期'] is None]
        
        # 添加数据到表格
        for record in unreturned_records:
            self.table.add_row((
                record['借阅记录编号'],
                record['读者卡号'],
                record['索书号'],
                format_date(record['借阅日期']),
                format_date(record['应还日期']),
                '未归还'
            ))
    
    def renew_book(self):
        """续借图书"""
        # 获取选中的借阅记录
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要续借的图书")
            return
        
        # 获取借阅记录ID
        values = selected_item['values']
        borrow_id = values[0]
        
        # 确认续借
        if messagebox.askyesno("确认续借", f"确定要续借图书 '{values[2]}' 吗？"):
            # 调用续借存储过程
            result = self.db.renew_book(borrow_id)
            
            try:
                if result and len(result) >= 1:
                    for res_set in result:
                        if len(res_set) > 0 and isinstance(res_set[0], dict):
                            output_params = res_set[0]
                            success = output_params.get('p_success', False)
                            message = output_params.get('p_message', '')
                            new_due_date = output_params.get('p_new_due_date', '')
                            
                            if success:
                                show_info(message)
                                self.refresh()
                            else:
                                show_error(message)
                            return
                            
                show_error("续借图书失败: 未能获取操作结果")
            except Exception as e:
                show_error(f"续借图书失败: {str(e)}")

class BorrowHistoryWindow(tk.Toplevel):
    """借阅历史窗口"""
    def __init__(self, parent, db, reader_id, reader_name):
        super().__init__(parent)
        self.db = db
        self.reader_id = reader_id
        self.reader_name = reader_name
        
        self.title(f"读者 '{reader_name}' 的借阅历史")
        self.geometry("800x600")
        
        # 创建标题
        title_label = ttk.Label(self, text=f"读者 '{reader_name}' 的借阅历史", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建表格
        columns = ('借阅记录编号', '索书号', '书名', '作者', '出版社', '借阅日期', '应还日期', '归还日期', '状态', '超期天数', '罚款金额')
        headings = ('借阅记录编号', '索书号', '书名', '作者', '出版社', '借阅日期', '应还日期', '归还日期', '状态', '超期天数', '罚款金额')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """加载借阅历史数据"""
        self.table.clear()
        
        # 调用查询读者借阅历史的存储过程
        result = self.db.get_reader_borrow_history(self.reader_id)
        
        if result and len(result) > 0:
            # 添加数据到表格
            for record in result[0]:
                self.table.add_row((
                    record['借阅记录编号'],
                    record['索书号'],
                    record['书名'],
                    record['作者'],
                    record['出版社'],
                    format_date(record['借阅日期']),
                    format_date(record['应还日期']),
                    format_date(record['归还日期']) if record['归还日期'] else '未归还',
                    record['状态'],
                    record['超期天数'],
                    f"¥{record['罚款金额']:.2f}" if record['罚款金额'] else '¥0.00'
                )) 