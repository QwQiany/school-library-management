import tkinter as tk
from tkinter import ttk, messagebox
from utils import TableFrame, EntryDialog, ComboBoxDialog, show_error, show_info, show_warning

class BookManagementFrame(ttk.Frame):
    """图书信息管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="图书信息管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加图书", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑图书", command=self.edit_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除图书", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('索书号', '书名', '作者', '出版社', '类别id', '总数', '在库数量')
        headings = ('索书号', '书名', '作者', '出版社', '类别', '总数', '在库数量')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
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
    
    def add_book(self):
        """添加图书"""
        # 获取出版社和类别列表
        publishers = self.db.get_all_publishers()
        categories = self.db.get_all_categories()
        
        # 创建出版社和类别的映射
        publisher_map = {p['名称']: p['出版社号'] for p in publishers}
        category_map = {c['类别名称']: c['类别id'] for c in categories}
        
        # 创建输入对话框
        fields = {
            '索书号': '索书号:',
            '书名': '书名:',
            '作者': '作者:',
            '出版社': '出版社:',
            '类别': '类别:',
            '总数': '总数:',
            '在库数量': '在库数量:'
        }
        
        dialog = EntryDialog(self, "添加图书", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 转换出版社和类别为ID
                publisher_id = publisher_map.get(dialog.result['出版社'])
                category_id = category_map.get(dialog.result['类别'])
                
                if not publisher_id or not category_id:
                    show_error("出版社或类别不存在")
                    return
                
                # 创建图书数据
                book_data = {
                    '索书号': dialog.result['索书号'],
                    '书名': dialog.result['书名'],
                    '作者': dialog.result['作者'],
                    '出版社': publisher_id,
                    '类别id': category_id,
                    '总数': int(dialog.result['总数']),
                    '在库数量': int(dialog.result['在库数量'])
                }
                
                # 添加图书
                result = self.db.add_book(book_data)
                if result:
                    show_info("添加图书成功")
                    self.refresh()
                else:
                    show_error("添加图书失败")
            except ValueError:
                show_error("请输入有效的数字")
            except Exception as e:
                show_error(f"添加图书时出错: {str(e)}")
    
    def edit_book(self):
        """编辑图书"""
        # 获取选中的图书
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要编辑的图书")
            return
        
        # 获取图书数据
        values = selected_item['values']
        book_id = values[0]
        
        # 获取图书详细信息
        book = self.db.get_book_by_id(book_id)
        if not book:
            show_error("获取图书信息失败")
            return
        
        # 获取出版社和类别列表
        publishers = self.db.get_all_publishers()
        categories = self.db.get_all_categories()
        
        # 创建出版社和类别的映射
        publisher_map = {p['名称']: p['出版社号'] for p in publishers}
        category_map = {c['类别名称']: c['类别id'] for c in categories}
        
        # 获取当前出版社和类别名称
        current_publisher = next((p['名称'] for p in publishers if p['出版社号'] == book['出版社']), '')
        current_category = next((c['类别名称'] for c in categories if c['类别id'] == book['类别id']), '')
        
        # 创建输入对话框
        fields = {
            '索书号': '索书号:',
            '书名': '书名:',
            '作者': '作者:',
            '出版社': '出版社:',
            '类别': '类别:',
            '总数': '总数:',
            '在库数量': '在库数量:'
        }
        
        dialog = EntryDialog(self, "编辑图书", fields)
        
        # 设置当前值
        dialog.entries['索书号'].insert(0, book['索书号'])
        dialog.entries['书名'].insert(0, book['书名'])
        dialog.entries['作者'].insert(0, book['作者'])
        dialog.entries['出版社'].insert(0, current_publisher)
        dialog.entries['类别'].insert(0, current_category)
        dialog.entries['总数'].insert(0, book['总数'])
        dialog.entries['在库数量'].insert(0, book['在库数量'])
        
        # 禁用索书号编辑
        dialog.entries['索书号'].config(state='disabled')
        
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 转换出版社和类别为ID
                publisher_id = publisher_map.get(dialog.result['出版社'])
                category_id = category_map.get(dialog.result['类别'])
                
                if not publisher_id or not category_id:
                    show_error("出版社或类别不存在")
                    return
                
                # 创建图书数据
                book_data = {
                    '索书号': book['索书号'],  # 使用原始索书号
                    '书名': dialog.result['书名'],
                    '作者': dialog.result['作者'],
                    '出版社': publisher_id,
                    '类别id': category_id,
                    '总数': int(dialog.result['总数']),
                    '在库数量': int(dialog.result['在库数量'])
                }
                
                # 更新图书
                result = self.db.update_book(book_data)
                if result:
                    show_info("更新图书成功")
                    self.refresh()
                else:
                    show_error("更新图书失败")
            except ValueError:
                show_error("请输入有效的数字")
            except Exception as e:
                show_error(f"更新图书时出错: {str(e)}")
    
    def delete_book(self):
        """删除图书"""
        # 获取选中的图书
        selected_item = self.table.get_selected_item()
        if not selected_item:
            show_warning("请先选择要删除的图书")
            return
        
        # 获取图书ID
        values = selected_item['values']
        book_id = values[0]
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除图书 '{values[1]}' 吗？"):
            # 删除图书
            result = self.db.delete_book(book_id)
            if result:
                show_info("删除图书成功")
                self.refresh()
            else:
                show_error("删除图书失败")

class CategoryManagementFrame(ttk.Frame):
    """图书类别管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="图书类别管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加类别", command=self.add_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('类别id', '类别名称')
        headings = ('类别ID', '类别名称')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有类别
        categories = self.db.get_all_categories()
        if not categories:
            return
        
        # 添加数据到表格
        for category in categories:
            self.table.add_row((
                category['类别id'],
                category['类别名称']
            ))
    
    def add_category(self):
        """添加类别"""
        # 创建输入对话框
        fields = {
            '类别名称': '类别名称:'
        }
        
        dialog = EntryDialog(self, "添加类别", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 添加类别
                result = self.db.add_category(dialog.result['类别名称'])
                if result:
                    show_info("添加类别成功")
                    self.refresh()
                else:
                    show_error("添加类别失败")
            except Exception as e:
                show_error(f"添加类别时出错: {str(e)}")

class PublisherManagementFrame(ttk.Frame):
    """出版社管理界面"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self, text="出版社管理", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="添加出版社", command=self.add_publisher).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh).pack(side=tk.LEFT, padx=5)
        
        # 创建表格
        columns = ('出版社号', '名称', '地址', '联系电话')
        headings = ('出版社号', '名称', '地址', '联系电话')
        self.table = TableFrame(self, columns, headings)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 加载数据
        self.refresh()
    
    def refresh(self):
        """刷新表格数据"""
        self.table.clear()
        
        # 获取所有出版社
        publishers = self.db.get_all_publishers()
        if not publishers:
            return
        
        # 添加数据到表格
        for publisher in publishers:
            self.table.add_row((
                publisher['出版社号'],
                publisher['名称'],
                publisher['地址'],
                publisher['联系电话']
            ))
    
    def add_publisher(self):
        """添加出版社"""
        # 创建输入对话框
        fields = {
            '名称': '名称:',
            '地址': '地址:',
            '联系电话': '联系电话:'
        }
        
        dialog = EntryDialog(self, "添加出版社", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # 创建出版社数据
                publisher_data = {
                    '名称': dialog.result['名称'],
                    '地址': dialog.result['地址'],
                    '联系电话': dialog.result['联系电话']
                }
                
                # 添加出版社
                result = self.db.add_publisher(publisher_data)
                if result:
                    show_info("添加出版社成功")
                    self.refresh()
                else:
                    show_error("添加出版社失败")
            except Exception as e:
                show_error(f"添加出版社时出错: {str(e)}") 