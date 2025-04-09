----------------------------数据库安全管理和备份恢复策略----------------------------------------------

-- 创建用户角色
-- 管理员角色：具有所有权限
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON school_library.* TO 'admin'@'localhost';

-- 图书管理员角色：管理图书信息
CREATE USER 'librarian'@'localhost' IDENTIFIED BY 'lib123';
GRANT SELECT, INSERT, UPDATE, DELETE ON school_library.books TO 'librarian'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON school_library.categories TO 'librarian'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON school_library.publishers TO 'librarian'@'localhost';
GRANT SELECT ON school_library.readers TO 'librarian'@'localhost';
GRANT SELECT ON school_library.borrow_records TO 'librarian'@'localhost';

-- 借阅管理员角色：管理借阅操作
CREATE USER 'borrow_manager'@'localhost' IDENTIFIED BY 'borrow123';
GRANT SELECT ON school_library.books TO 'borrow_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE ON school_library.borrow_records TO 'borrow_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE ON school_library.readers TO 'borrow_manager'@'localhost';
GRANT SELECT, INSERT ON school_library.fines TO 'borrow_manager'@'localhost';

-- 只读用户角色：只能查询
CREATE USER 'reader'@'localhost' IDENTIFIED BY 'reader123';
GRANT SELECT ON school_library.books TO 'reader'@'localhost';
GRANT SELECT ON school_library.categories TO 'reader'@'localhost';
GRANT SELECT ON school_library.publishers TO 'reader'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;