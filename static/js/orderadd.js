// --- 1. 視窗開關邏輯 (解決 open_input_table is not defined) ---

// 打開彈出視窗
function open_input_table() {
    document.getElementById('addModal').style.display = 'block';
}

// 關閉彈出視窗
function close_input_table() {
    document.getElementById('addModal').style.display = 'none';
}

// 點擊視窗外部也能關閉
window.onclick = function(event) {
    let modal = document.getElementById('addModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// --- 2. 前後端連動與計算邏輯 (保留原本的功能) ---

function selectCategory() {
    let category = document.getElementById("category").value;
    
    fetch(`/product?category=${category}`)
        .then(response => response.json())
        .then(data => {
            let productSelect = document.getElementById("product");
            // 重置選項
            productSelect.innerHTML = "<option value='' disabled selected>請選擇商品</option>";
            
            data.product.forEach(prod => {
                let option = document.createElement("option");
                option.value = prod;
                option.text = prod;
                productSelect.add(option);
            });
            
            // 清空價格與小計
            document.getElementById("price").value = "";
            document.getElementById("total").value = "";
        })
        .catch(error => console.error('Error:', error));
}

function selectProduct() {
    let product = document.getElementById("product").value;

    fetch(`/product?product=${product}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("price").value = data.price;
            countTotal(); // 取得價格後自動計算一次
        })
        .catch(error => console.error('Error:', error));
}

function countTotal() {
    let price = parseFloat(document.getElementById("price").value) || 0;
    let amount = parseInt(document.getElementById("amount").value) || 0;
    
    if (amount <= 0) {
        amount = 1;
        document.getElementById("amount").value = 1;
    }
    
    document.getElementById("total").value = price * amount;
}