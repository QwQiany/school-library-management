DROP DATABASE IF EXISTS school_library;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS school_library 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci; 

USE school_library;


-- 创建出版社表
CREATE TABLE publishers (
    出版社号 INT PRIMARY KEY AUTO_INCREMENT,
    名称 VARCHAR(100) NOT NULL UNIQUE,
    地址 VARCHAR(255),
    联系电话 VARCHAR(20)
) ENGINE=InnoDB;

-- 创建图书类别表
CREATE TABLE categories (
    类别id INT PRIMARY KEY AUTO_INCREMENT,
    类别名称 VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 创建图书表
CREATE TABLE books (
    索书号 VARCHAR(20) PRIMARY KEY,
    书名 VARCHAR(200) NOT NULL,
    作者 VARCHAR(100) NOT NULL,
    出版社 INT NOT NULL,
    类别id INT NOT NULL,
    总数 INT NOT NULL CHECK (总数 > 0),
    在库数量 INT NOT NULL CHECK (在库数量 >= 0),
    FOREIGN KEY (出版社) REFERENCES publishers(出版社号),
    FOREIGN KEY (类别id) REFERENCES categories(类别id),
    CHECK (在库数量 <= 总数)
) ENGINE=InnoDB;

-- 创建读者表
CREATE TABLE readers (
    读者卡号 VARCHAR(20) PRIMARY KEY,
    姓名 VARCHAR(50) NOT NULL,
    证件号 VARCHAR(18) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 创建借阅记录表
CREATE TABLE borrow_records (
    借阅记录编号 INT PRIMARY KEY AUTO_INCREMENT,
    读者卡号 VARCHAR(20) NOT NULL,
    索书号 VARCHAR(20) NOT NULL,
    借阅日期 DATE NOT NULL,
    应还日期 DATE NOT NULL,
    归还日期 DATE,
    FOREIGN KEY (读者卡号) REFERENCES readers(读者卡号),
    FOREIGN KEY (索书号) REFERENCES books(索书号),
    CHECK (应还日期 > 借阅日期),
    CHECK (归还日期 IS NULL OR 归还日期 >= 借阅日期)
) ENGINE=InnoDB;

-- 创建罚款记录表
CREATE TABLE fines (
    罚款记录号 INT PRIMARY KEY AUTO_INCREMENT,
    借阅记录编号 INT NOT NULL UNIQUE,
    罚款金额 DECIMAL(10,2) NOT NULL CHECK (罚款金额 >= 0),
    FOREIGN KEY (借阅记录编号) REFERENCES borrow_records(借阅记录编号)
) ENGINE=InnoDB;






-- 插入测试数据

-- 插入出版社数据（6条）
INSERT INTO publishers (名称, 地址, 联系电话) VALUES
('人民教育出版社', '北京市海淀区中关村大街1号', '010-12345678'),
('清华大学出版社', '北京市海淀区清华园1号', '010-23456789'),
('机械工业出版社', '北京市西城区百万庄大街22号', '010-34567890'),
('电子工业出版社', '北京市万寿路173信箱', '010-45678901'),
('商务印书馆', '北京市王府井大街36号', '010-56789012'),
('北京大学出版社', '北京市海淀区颐和园路5号', '010-67890123');

-- 插入图书类别（6条）
INSERT INTO categories (类别名称) VALUES
('计算机科学'),
('文学小说'),
('历史传记'),
('教育教材'),
('科学技术'),
('艺术设计');

-- 插入图书数据（6条，初始在库数量=总数）
INSERT INTO books (索书号, 书名, 作者, 出版社, 类别id, 总数, 在库数量) VALUES
('TP311.13/001', '数据库系统概论', '王珊', 1, 1, 10, 10),
('I247.5/002', '三体', '刘慈欣', 2, 2, 5, 5),
('K825.6/003', '毛泽东传', '罗斯·特里尔', 3, 3, 8, 8),
('G434/004', '现代教育技术', '李芒', 4, 4, 15, 15),
('N49/005', '时间简史', '霍金', 5, 5, 7, 7),
('J06/006', '设计心理学', '唐纳德·诺曼', 6, 6, 6, 6);

-- 插入读者数据（6条）
INSERT INTO readers (读者卡号, 姓名, 证件号) VALUES
('R2023001', '张三', '110101199001011234'),
('R2023002', '李四', '110102199002022345'),
('R2023003', '王五', '110105199003033456'),
('R2023004', '赵六', '110106199004044567'),
('R2023005', '陈七', '110107199005055678'),
('R2023006', '周八', '110108199006066789');

-- 插入借阅记录（6条，全部超期）
INSERT INTO borrow_records (读者卡号, 索书号, 借阅日期, 应还日期, 归还日期) VALUES
('R2023001', 'TP311.13/001', '2023-09-01', '2023-10-01', '2023-10-05'),  -- 超期4天
('R2023002', 'I247.5/002', '2023-09-05', '2023-10-05', '2023-10-10'),  -- 超期5天
('R2023003', 'K825.6/003', '2023-09-10', '2023-10-10', '2023-10-15'),  -- 超期5天
('R2023004', 'G434/004', '2023-09-15', '2023-10-15', '2023-10-20'),  -- 超期5天
('R2023005', 'N49/005', '2023-09-20', '2023-10-20', '2023-10-25'),  -- 超期5天
('R2023006', 'J06/006', '2023-09-25', '2023-10-25', '2023-10-30');  -- 超期5天

-- 插入罚款记录（6条，按每天1元计算）
INSERT INTO fines (借阅记录编号, 罚款金额) VALUES
(1, 4.00),
(2, 5.00),
(3, 5.00),
(4, 5.00),
(5, 5.00),
(6, 5.00);


----------------------------创建触发器----------------------------------------------


-- 借书触发器：更新图书在库数量
DELIMITER //
CREATE TRIGGER after_borrow_insert
AFTER INSERT ON borrow_records
FOR EACH ROW
BEGIN
    UPDATE books 
    SET 在库数量 = 在库数量 - 1
    WHERE 索书号 = NEW.索书号;
END //
DELIMITER ;

-- 还书触发器：更新图书在库数量
DELIMITER //
CREATE TRIGGER after_return_update
AFTER UPDATE ON borrow_records
FOR EACH ROW
BEGIN
    IF OLD.归还日期 IS NULL AND NEW.归还日期 IS NOT NULL THEN
        UPDATE books 
        SET 在库数量 = 在库数量 + 1
        WHERE 索书号 = NEW.索书号;
    END IF;
END //
DELIMITER ;

-- 超期罚款触发器：自动插入罚款记录
DELIMITER //
CREATE TRIGGER after_return_fine
AFTER UPDATE ON borrow_records
FOR EACH ROW
BEGIN
    DECLARE days_overdue INT;
    DECLARE fine_amount DECIMAL(10,2);
    
    IF OLD.归还日期 IS NULL AND NEW.归还日期 IS NOT NULL 
       AND NEW.归还日期 > NEW.应还日期 THEN
        -- 计算超期天数
        SET days_overdue = DATEDIFF(NEW.归还日期, NEW.应还日期);
        -- 计算罚款金额（每天1元）
        SET fine_amount = days_overdue * 1.00;
        
        -- 插入罚款记录
        INSERT INTO fines(借阅记录编号, 罚款金额)
        VALUES(NEW.借阅记录编号, fine_amount);
    END IF;
END //
DELIMITER ;

----------------------------创建视图----------------------------------------------

-- 创建图书信息视图
CREATE VIEW book_info_view AS
SELECT b.索书号, b.书名, b.作者, p.名称 AS 出版社名称, c.类别名称, b.总数, b.在库数量
FROM books b
JOIN publishers p ON b.出版社 = p.出版社号
JOIN categories c ON b.类别id = c.类别id;

-- 创建借阅信息视图
CREATE VIEW borrow_info_view AS
SELECT br.借阅记录编号, r.读者卡号, r.姓名 AS 读者姓名, 
       b.索书号, b.书名, br.借阅日期, br.应还日期, br.归还日期,
       CASE 
           WHEN br.归还日期 IS NULL THEN '未归还'
           WHEN br.归还日期 > br.应还日期 THEN '已超期归还'
           ELSE '已按时归还'
       END AS 借阅状态,
       CASE 
           WHEN br.归还日期 IS NULL AND CURDATE() > br.应还日期 
                THEN DATEDIFF(CURDATE(), br.应还日期) * 1.00
           WHEN br.归还日期 > br.应还日期 
                THEN DATEDIFF(br.归还日期, br.应还日期) * 1.00
           ELSE 0
       END AS 预计罚款
FROM borrow_records br
JOIN readers r ON br.读者卡号 = r.读者卡号
JOIN books b ON br.索书号 = b.索书号;

----------------------------存储过程----------------------------------------------

-- 查询指定读者借阅情况的存储过程
DELIMITER //
CREATE PROCEDURE get_reader_borrow_history(IN reader_id VARCHAR(20))
BEGIN
    SELECT br.借阅记录编号, b.索书号, b.书名, b.作者, 
           p.名称 AS 出版社, br.借阅日期, br.应还日期, br.归还日期,
           CASE 
               WHEN br.归还日期 IS NULL AND CURDATE() <= br.应还日期 THEN '借阅中'
               WHEN br.归还日期 IS NULL AND CURDATE() > br.应还日期 THEN '已超期'
               WHEN br.归还日期 <= br.应还日期 THEN '已按时归还'
               ELSE '超期归还'
           END AS 状态,
           CASE 
               WHEN br.归还日期 IS NULL AND CURDATE() > br.应还日期 
                    THEN DATEDIFF(CURDATE(), br.应还日期)
               WHEN br.归还日期 > br.应还日期 
                    THEN DATEDIFF(br.归还日期, br.应还日期)
               ELSE 0
           END AS 超期天数,
           f.罚款金额
    FROM borrow_records br
    JOIN books b ON br.索书号 = b.索书号
    JOIN publishers p ON b.出版社 = p.出版社号
    LEFT JOIN fines f ON br.借阅记录编号 = f.借阅记录编号
    WHERE br.读者卡号 = reader_id
    ORDER BY br.借阅日期 DESC;
END //
DELIMITER ;

-- 借书存储过程
DELIMITER //
CREATE PROCEDURE borrow_book(
    IN p_reader_id VARCHAR(20),
    IN p_book_id VARCHAR(20),
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(100)
)
BEGIN
    DECLARE book_available INT DEFAULT 0;
    DECLARE current_date_var DATE DEFAULT CURDATE();
    DECLARE due_date DATE;
    
    -- 检查图书是否有库存
    SELECT 在库数量 INTO book_available FROM books WHERE 索书号 = p_book_id;
    
    -- 设置默认值
    SET p_success = FALSE;
    SET p_message = '';
    
    -- 设置应还日期（借阅日期后30天）
    SET due_date = DATE_ADD(current_date_var, INTERVAL 30 DAY);
    
    -- 检查是否有足够库存
    IF book_available <= 0 THEN
        SET p_message = '借阅失败：该书已无库存';
    ELSE
        -- 执行借阅操作
        INSERT INTO borrow_records(读者卡号, 索书号, 借阅日期, 应还日期, 归还日期)
        VALUES(p_reader_id, p_book_id, current_date_var, due_date, NULL);
        
        SET p_success = TRUE;
        SET p_message = '借阅成功';
    END IF;
END //
DELIMITER ;

-- 还书存储过程
DELIMITER //
CREATE PROCEDURE return_book(
    IN p_borrow_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(100),
    OUT p_fine DECIMAL(10,2)
)
BEGIN
    DECLARE is_returned BOOLEAN DEFAULT FALSE;
    DECLARE current_date_var DATE DEFAULT CURDATE();
    DECLARE due_date DATE;
    DECLARE days_overdue INT DEFAULT 0;
    
    -- 设置默认值
    SET p_success = FALSE;
    SET p_message = '';
    SET p_fine = 0;
    
    -- 检查借阅记录是否存在且未归还
    SELECT 归还日期 IS NOT NULL, 应还日期 INTO is_returned, due_date 
    FROM borrow_records WHERE 借阅记录编号 = p_borrow_id;
    
    -- 检查是否已经归还
    IF is_returned THEN
        SET p_message = '还书失败：该书已归还';
    ELSE
        -- 执行还书操作
        UPDATE borrow_records 
        SET 归还日期 = current_date_var
        WHERE 借阅记录编号 = p_borrow_id;
        
        -- 计算是否超期
        IF current_date_var > due_date THEN
            SET days_overdue = DATEDIFF(current_date_var, due_date);
            SET p_fine = days_overdue * 1.00;
            SET p_message = CONCAT('还书成功，超期', days_overdue, '天，需缴纳罚款', p_fine, '元');
        ELSE
            SET p_message = '还书成功，未超期';
        END IF;
        
        SET p_success = TRUE;
    END IF;
END //
DELIMITER ;

-- 续借存储过程
DELIMITER //
CREATE PROCEDURE renew_book(
    IN p_borrow_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(100),
    OUT p_new_due_date DATE
)
BEGIN
    DECLARE is_returned BOOLEAN DEFAULT FALSE;
    DECLARE is_overdue BOOLEAN DEFAULT FALSE;
    DECLARE current_due_date DATE;
    
    -- 设置默认值
    SET p_success = FALSE;
    SET p_message = '';
    
    -- 检查借阅记录是否存在且未归还
    SELECT 
        归还日期 IS NOT NULL, 
        应还日期 < CURDATE(),
        应还日期 
    INTO is_returned, is_overdue, current_due_date
    FROM borrow_records 
    WHERE 借阅记录编号 = p_borrow_id;
    
    -- 检查是否已经归还
    IF is_returned THEN
        SET p_message = '续借失败：该书已归还';
    -- 检查是否已经超期
    ELSEIF is_overdue THEN
        SET p_message = '续借失败：该书已超期，请先归还并缴纳罚款';
    ELSE
        -- 执行续借操作（延长30天）
        SET p_new_due_date = DATE_ADD(current_due_date, INTERVAL 30 DAY);
        
        UPDATE borrow_records 
        SET 应还日期 = p_new_due_date
        WHERE 借阅记录编号 = p_borrow_id;
        
        SET p_success = TRUE;
        SET p_message = CONCAT('续借成功，新的应还日期为: ', p_new_due_date);
    END IF;
END //
DELIMITER ;

----------------------------自定义函数----------------------------------------------

-- 计算超期天数函数
DELIMITER //
CREATE FUNCTION calculate_overdue_days(borrow_date DATE, due_date DATE, return_date DATE) 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE overdue_days INT;
    
    IF return_date IS NULL THEN
        -- 如果尚未归还，计算到当前日期的超期天数
        IF CURDATE() > due_date THEN
            SET overdue_days = DATEDIFF(CURDATE(), due_date);
        ELSE
            SET overdue_days = 0;
        END IF;
    ELSE
        -- 如果已归还，计算实际超期天数
        IF return_date > due_date THEN
            SET overdue_days = DATEDIFF(return_date, due_date);
        ELSE
            SET overdue_days = 0;
        END IF;
    END IF;
    
    RETURN overdue_days;
END //
DELIMITER ;

-- 计算罚款金额函数
DELIMITER //
CREATE FUNCTION calculate_fine(overdue_days INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    -- 每超期一天罚款1元
    RETURN overdue_days * 1.00;
END //
DELIMITER ;

----------------------------查询语句----------------------------------------------

-- 1. 简单查询：查询所有可借阅的图书
SELECT 索书号, 书名, 作者, 在库数量
FROM books
WHERE 在库数量 > 0
ORDER BY 索书号;

-- 2. 模糊查询：按书名或作者模糊查询图书
SELECT 索书号, 书名, 作者, 在库数量
FROM books
WHERE 书名 LIKE '%数据库%' OR 作者 LIKE '%王%';

-- 3. 连接查询：查询各类别的图书数量
SELECT c.类别名称, COUNT(b.索书号) AS 图书数量, SUM(b.总数) AS 总册数
FROM categories c
LEFT JOIN books b ON c.类别id = b.类别id
GROUP BY c.类别id, c.类别名称;

-- 4. 嵌套查询：查询借阅量最多的前3本书
WITH top_books AS (
    SELECT br.索书号, COUNT(br.借阅记录编号) AS borrow_count
    FROM borrow_records br
    GROUP BY br.索书号
    ORDER BY borrow_count DESC
    LIMIT 3
)
SELECT b.索书号, b.书名, tb.borrow_count AS 借阅次数
FROM books b
JOIN top_books tb ON b.索书号 = tb.索书号
ORDER BY tb.borrow_count DESC;

-- 5. 复杂查询：统计每位读者的借阅情况和罚款总额
SELECT r.读者卡号, r.姓名, 
       COUNT(br.借阅记录编号) AS 总借阅次数,
       SUM(CASE WHEN br.归还日期 IS NULL THEN 1 ELSE 0 END) AS 未归还数量,
       SUM(CASE WHEN br.归还日期 > br.应还日期 THEN 1 ELSE 0 END) AS 超期归还次数,
       COALESCE(SUM(f.罚款金额), 0) AS 罚款总额
FROM readers r
LEFT JOIN borrow_records br ON r.读者卡号 = br.读者卡号
LEFT JOIN fines f ON br.借阅记录编号 = f.借阅记录编号
GROUP BY r.读者卡号, r.姓名
ORDER BY 罚款总额 DESC;


