import os
import sqlite3
from flask import Flask, request, jsonify, redirect, url_for, render_template
from core.database.database import Database

# 初始化 Flask (假設 app.py 在根目錄，且 templates 在 core/templates 或根目錄 templates)
# 視您的資料夾結構而定，如果是預設結構 (同層)，直接用 Flask(__name__) 即可
app = Flask(__name__)

# 初始化資料庫物件
db = Database()

@app.route('/')
def index():
    # 使用 with 語法確保連線會自動關閉
    warning = request.args.get('warning')
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        # 傳入 cursor 取得資料
        orders = db.get_all_orders(cursor)
    
    # 注意：如果您想讓 Modal 表單一開始就存在於頁面上，
    # 且 form.html 是繼承 index.html 的，您應該 render 'form.html'。
    # 因為 form.html extends index.html，所以它會包含 index 的所有內容 + 表單。
    return render_template('form.html', orders=orders, warning = warning)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            if 'category' in request.args:
                category = request.args.get('category')
                # 傳入 cursor
                products = db.get_product_names_by_category(cursor, category)
                return jsonify({"product": products})
            
            elif 'product' in request.args:
                product_name = request.args.get('product')
                # 傳入 cursor
                price = db.get_product_price(cursor, product_name)
                return jsonify({"price": price})

    elif request.method == 'POST':
        # 整理表單資料
        order_data = {
            "product_date": request.form.get("product_date"),
            "customer_name": request.form.get("customer_name"),
            "product_name": request.form.get("product_name"),
            "product_amount": request.form.get("product_amount"),
            "product_total": request.form.get("product_total"),
            "product_status": request.form.get("product_status"),
            "product_note": request.form.get("product_note")
        }
        
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            # 傳入 cursor 新增訂單
            db.add_order(cursor, order_data)
            # 務必執行 commit，否則資料不會寫入
            conn.commit()
            
        return redirect(url_for('index', warning="Order placed successfully"))

    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')
        if order_id:
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                # 傳入 cursor 刪除訂單
                db.delete_order(cursor, order_id)
                conn.commit()
            return jsonify({"message": "Order deleted successfully"}), 200
        return jsonify({"message": "Order ID missing"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)