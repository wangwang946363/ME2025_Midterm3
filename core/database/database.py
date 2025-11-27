import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self, cur, category):
        """根據分類取得商品名稱列表"""
        sql = "SELECT product FROM commodity WHERE category = ?"
        cur.execute(sql, (category,))
        result = cur.fetchall()
        # 回傳 List of Strings: ['可樂', '綠茶', ...]
        return [row[0] for row in result]

    def get_product_price(self, cur, product):
        """根據商品名稱取得價格"""
        sql = "SELECT price FROM commodity WHERE product = ?"
        cur.execute(sql, (product,))
        result = cur.fetchone()
        return result[0] if result else 0

    def add_order(self, cur, order_data):
        """新增訂單"""
        # 1. 產生不重複的訂單編號
        order_id = self.generate_order_id()
        
        # 2. 準備 SQL (注意：這裡使用資料庫實際欄位名稱)
        sql = """
        INSERT INTO order_list 
        (order_id, date, customer_name, product, amount, total, status, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # 3. 對應傳入的字典資料
        values = (
            order_id,
            order_data['product_date'],
            order_data['customer_name'],
            order_data['product_name'], # 前端傳來的是 product_name，寫入 product 欄位
            order_data['product_amount'],
            order_data['product_total'],
            order_data['product_status'],
            order_data['product_note']
        )
        
        cur.execute(sql, values)
        # 注意：commit 由外部控制

    def get_all_orders(self, cur):
        """
        取得所有訂單資料
        為了配合 index.html 的迴圈寫法 {% for i in range(order|length) %}
        這裡必須回傳 List of Tuples，且欄位順序要跟 HTML 表頭一致。
        """
        sql = """
        SELECT 
            o.order_id,      -- index 0
            o.date,          -- index 1
            o.customer_name, -- index 2
            o.product,       -- index 3
            c.price,         -- index 4 (Join 取得單價)
            o.amount,        -- index 5
            o.total,         -- index 6
            o.status,        -- index 7
            o.note           -- index 8
        FROM order_list o
        LEFT JOIN commodity c ON o.product = c.product
        """
        cur.execute(sql)
        return cur.fetchall()

    def delete_order(self, cur, order_id):
        """刪除訂單"""
        sql = "DELETE FROM order_list WHERE order_id = ?"
        cur.execute(sql, (order_id,))