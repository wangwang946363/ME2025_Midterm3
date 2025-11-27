import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    def get_connection(self):
        """輔助方法：簡化連線開啟"""
        return sqlite3.connect(self.db_path)

    def generate_order_id(self) -> str:
        """產生訂單編號 (注意：這裡不寫 @staticmethod，因為測試會覆寫它)"""
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self, category):
        """
        測試需求：results = self.db.get_product_names_by_category('主食')
        回傳格式：必須是 List of Tuples，因為測試碼寫 products = [r[0] for r in results]
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT product FROM commodity WHERE category = ?"
            cursor.execute(sql, (category,))
            # 直接回傳原始結果 [(product1,), (product2,)...]
            return cursor.fetchall()

    def get_product_price(self, product):
        """
        測試需求：price = self.db.get_product_price('咖哩飯')
        回傳：整數價格，若無則回傳 None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT price FROM commodity WHERE product = ?"
            cursor.execute(sql, (product,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None

    def add_order(self, order_data):
        """
        測試需求：self.db.add_order(order_data) (不傳 cursor)
        邏輯：必須使用 self.generate_order_id() 以支援測試的 Mock
        """
        # 呼叫 self 的方法，這樣測試程式覆寫時才會生效
        order_id = self.generate_order_id()
        
        sql = """
        INSERT INTO order_list 
        (order_id, date, customer_name, product, amount, total, status, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            order_id,
            order_data['product_date'],
            order_data['customer_name'],
            order_data['product_name'],
            order_data['product_amount'],
            order_data['product_total'],
            order_data['product_status'],
            order_data['product_note']
        )
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit() # 記得 commit

    def get_all_orders(self):
        """
        測試需求：orders = self.db.get_all_orders()
        回傳：List of Tuples，且必須包含 JOIN 後的 price 欄位
        """
        sql = """
        SELECT 
            o.order_id,      -- index 0
            o.date,          -- index 1
            o.customer_name, -- index 2
            o.product,       -- index 3
            c.price,         -- index 4 (測試重點驗證這欄)
            o.amount,        -- index 5
            o.total,         -- index 6
            o.status,        -- index 7
            o.note           -- index 8
        FROM order_list o
        LEFT JOIN commodity c ON o.product = c.product
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def delete_order(self, order_id):
        """
        測試需求：success = self.db.delete_order('ORD-001')
        回傳：必須回傳 True
        """
        sql = "DELETE FROM order_list WHERE order_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (order_id,))
            conn.commit()
        return True