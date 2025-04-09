import tkinter as tk
from tkinter import ttk, messagebox
from utils import TableFrame, EntryDialog, ComboBoxDialog, show_error, show_info, show_warning, format_money

class BookQueryFrame(ttk.Frame):
    """图书信息查询界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="图书信息查询", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建查询框架
        query_frame = ttk.Frame(self)
        query_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(query_frame, text="查询条件:").pack(side=tk.LEFT, padx=5)
        
        self.query_type = tk.StringVar(value="all")
        ttk.Radiobutton(query_frame, text="全部", variable=self.query_type, value="all").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按索书号", variable=self.query_type, value="id").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按书名", variable=self.query_type, value="name").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按作者", variable=self.query_type, value="author").pack(side=tk.LEFT, padx=5)
        
        self.query_entry = ttk.Entry(query_frame, width=30)
        self.query_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(query_frame, text="查询", command=self.search).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('索书号', '书名', '作者', '出版社', '类别', '总数', '在库数量')
        headings = ('索书号', '书名', '作者', '出版社', '类别', '总数', '在库数量')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.load_all_books()
    
    def load_all_books(self):
        """加载所有图书"""
        self.table.clear()
        
        # 获取所有图书
        books = self.db.get_all_books()
        if not books:
            return
        
        # 获取所有出版社和类别
        publishers = {p['出版社号']: p['名称'] for p in self.db.get_all_publishers()}
        categories = {c['类别id']: c['类别名称'] for c in self.db.get_all_categories()}
        
        # 添加数据到表格
        for book in books:
            publisher_name = publishers.get(book['出版社'], str(book['出版社']))
            category_name = categories.get(book['类别id'], str(book['类别id']))
            
            self.table.add_row((
                book['索书号'],
                book['书名'],
                book['作者'],
                publisher_name,
                category_name,
                book['总数'],
                book['在库数量']
            ))
    
    def search(self):
        """搜索图书"""
        query_type = self.query_type.get()
        query_text = self.query_entry.get().strip()
        
        if query_type == "all":
            self.load_all_books()
            return
        
        # 获取所有图书
        books = self.db.get_all_books()
        if not books:
            return
        
        # 获取所有出版社和类别
        publishers = {p['出版社号']: p['名称'] for p in self.db.get_all_publishers()}
        categories = {c['类别id']: c['类别名称'] for c in self.db.get_all_categories()}
        
        # 清空表格
        self.table.clear()
        
        # 根据查询条件过滤图书
        for book in books:
            if query_type == "id" and query_text.lower() in book['索书号'].lower():
                publisher_name = publishers.get(book['出版社'], str(book['出版社']))
                category_name = categories.get(book['类别id'], str(book['类别id']))
                
                self.table.add_row((
                    book['索书号'],
                    book['书名'],
                    book['作者'],
                    publisher_name,
                    category_name,
                    book['总数'],
                    book['在库数量']
                ))
            elif query_type == "name" and query_text.lower() in book['书名'].lower():
                publisher_name = publishers.get(book['出版社'], str(book['出版社']))
                category_name = categories.get(book['类别id'], str(book['类别id']))
                
                self.table.add_row((
                    book['索书号'],
                    book['书名'],
                    book['作者'],
                    publisher_name,
                    category_name,
                    book['总数'],
                    book['在库数量']
                ))
            elif query_type == "author" and query_text.lower() in book['作者'].lower():
                publisher_name = publishers.get(book['出版社'], str(book['出版社']))
                category_name = categories.get(book['类别id'], str(book['类别id']))
                
                self.table.add_row((
                    book['索书号'],
                    book['书名'],
                    book['作者'],
                    publisher_name,
                    category_name,
                    book['总数'],
                    book['在库数量']
                ))

class BorrowQueryFrame(ttk.Frame):
    """借阅信息查询界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="借阅信息查询", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建查询框架
        query_frame = ttk.Frame(self)
        query_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(query_frame, text="查询条件:").pack(side=tk.LEFT, padx=5)
        
        self.query_type = tk.StringVar(value="all")
        ttk.Radiobutton(query_frame, text="全部", variable=self.query_type, value="all").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按读者卡号", variable=self.query_type, value="reader").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按索书号", variable=self.query_type, value="book").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(query_frame, text="按状态", variable=self.query_type, value="status").pack(side=tk.LEFT, padx=5)
        
        self.query_entry = ttk.Entry(query_frame, width=30)
        self.query_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(query_frame, text="查询", command=self.search).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('借阅记录编号', '读者卡号', '读者姓名', '索书号', '书名', '借阅日期', '应还日期', '归还日期', '借阅状态', '预计罚款')
        headings = ('借阅记录编号', '读者卡号', '读者姓名', '索书号', '书名', '借阅日期', '应还日期', '归还日期', '借阅状态', '预计罚款')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.load_all_borrows()
    
    def load_all_borrows(self):
        """加载所有借阅信息"""
        self.table.clear()
        
        # 获取借阅信息视图
        borrow_info = self.db.get_borrow_info_view()
        if not borrow_info:
            return
        
        # 添加数据到表格
        for info in borrow_info:
            self.table.add_row((
                info['借阅记录编号'],
                info['读者卡号'],
                info['读者姓名'],
                info['索书号'],
                info['书名'],
                info['借阅日期'],
                info['应还日期'],
                info['归还日期'] if info['归还日期'] else '未归还',
                info['借阅状态'],
                f"¥{info['预计罚款']:.2f}" if info['预计罚款'] else '¥0.00'
            ))
    
    def search(self):
        """搜索借阅信息"""
        query_type = self.query_type.get()
        query_text = self.query_entry.get().strip()
        
        if query_type == "all":
            self.load_all_borrows()
            return
        
        # 获取借阅信息视图
        borrow_info = self.db.get_borrow_info_view()
        if not borrow_info:
            return
        
        # 清空表格
        self.table.clear()
        
        # 根据查询条件过滤借阅信息
        for info in borrow_info:
            if query_type == "reader" and query_text.lower() in info['读者卡号'].lower():
                self.table.add_row((
                    info['借阅记录编号'],
                    info['读者卡号'],
                    info['读者姓名'],
                    info['索书号'],
                    info['书名'],
                    info['借阅日期'],
                    info['应还日期'],
                    info['归还日期'] if info['归还日期'] else '未归还',
                    info['借阅状态'],
                    f"¥{info['预计罚款']:.2f}" if info['预计罚款'] else '¥0.00'
                ))
            elif query_type == "book" and query_text.lower() in info['索书号'].lower():
                self.table.add_row((
                    info['借阅记录编号'],
                    info['读者卡号'],
                    info['读者姓名'],
                    info['索书号'],
                    info['书名'],
                    info['借阅日期'],
                    info['应还日期'],
                    info['归还日期'] if info['归还日期'] else '未归还',
                    info['借阅状态'],
                    f"¥{info['预计罚款']:.2f}" if info['预计罚款'] else '¥0.00'
                ))
            elif query_type == "status" and query_text.lower() in info['借阅状态'].lower():
                self.table.add_row((
                    info['借阅记录编号'],
                    info['读者卡号'],
                    info['读者姓名'],
                    info['索书号'],
                    info['书名'],
                    info['借阅日期'],
                    info['应还日期'],
                    info['归还日期'] if info['归还日期'] else '未归还',
                    info['借阅状态'],
                    f"¥{info['预计罚款']:.2f}" if info['预计罚款'] else '¥0.00'
                ))

class ReaderHistoryFrame(ttk.Frame):
    """读者借阅历史界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="读者借阅历史查询", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建查询框架
        query_frame = ttk.Frame(self)
        query_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(query_frame, text="读者卡号:").pack(side=tk.LEFT, padx=5)
        
        self.reader_entry = ttk.Entry(query_frame, width=30)
        self.reader_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(query_frame, text="查询", command=self.search).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('借阅记录编号', '索书号', '书名', '作者', '出版社', '借阅日期', '应还日期', '归还日期', '状态', '超期天数', '罚款金额')
        headings = ('借阅记录编号', '索书号', '书名', '作者', '出版社', '借阅日期', '应还日期', '归还日期', '状态', '超期天数', '罚款金额')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def search(self):
        """搜索读者借阅历史"""
        reader_id = self.reader_entry.get().strip()
        
        if not reader_id:
            show_warning("请输入读者卡号")
            return
        
        # 清空表格
        self.table.clear()
        
        # 调用查询读者借阅历史的存储过程
        result = self.db.get_reader_borrow_history(reader_id)
        
        if result and len(result) > 0:
            # 添加数据到表格
            for record in result[0]:
                self.table.add_row((
                    record['借阅记录编号'],
                    record['索书号'],
                    record['书名'],
                    record['作者'],
                    record['出版社'],
                    record['借阅日期'],
                    record['应还日期'],
                    record['归还日期'] if record['归还日期'] else '未归还',
                    record['状态'],
                    record['超期天数'],
                    f"¥{record['罚款金额']:.2f}" if record['罚款金额'] else '¥0.00'
                ))
        else:
            show_info("未找到该读者的借阅历史") 