# app.py 配合修正後的 database.py
from flask import Flask, request, jsonify, redirect, url_for, render_template
from core.database.database import Database 

app = Flask(__name__)
db = Database() 

@app.route('/')
def index():
    # 不用再傳 cursor 了，直接呼叫
    orders = db.get_all_orders()
    return render_template('form.html', orders=orders)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        if 'category' in request.args:
            category = request.args.get('category')
            # 這裡注意：get_product_names_by_category 現在回傳 List of Tuples
            # 但前端 JSON 需要 List of Strings，所以這裡要轉一下
            raw_data = db.get_product_names_by_category(category)
            products = [row[0] for row in raw_data] 
            return jsonify({"product": products})
        
        elif 'product' in request.args:
            product_name = request.args.get('product')
            price = db.get_product_price(product_name)
            return jsonify({"price": price})

    elif request.method == 'POST':
        order_data = {
            "product_date": request.form.get("product_date"),
            "customer_name": request.form.get("customer_name"),
            "product_name": request.form.get("product_name"),
            "product_amount": request.form.get("product_amount"),
            "product_total": request.form.get("product_total"),
            "product_status": request.form.get("product_status"),
            "product_note": request.form.get("product_note")
        }
        db.add_order(order_data)
        return redirect(url_for('index', warning="Order placed successfully"))

    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')
        if order_id:
            db.delete_order(order_id)
            return jsonify({"message": "Order deleted successfully"}), 200
        return jsonify({"message": "Order ID missing"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)