from typing import Text
from  flask import Flask, render_template,redirect,jsonify, request
from flask_cors import CORS
from werkzeug.wrappers import response
from chat import chatbot_response
from book import book_response
import json
import random
intents = json.loads(open('data/book_data.json',encoding='utf8').read())
app = Flask(__name__)
CORS(app)
diachi = 'diachi'
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

    return True
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/send")
def send():
    text = request.get_json().get("message")
    #TODO: check if text is valid
    response = book_response(text)
    file =open('bill.txt','a', encoding='utf8')
    file.write('giá quyển sách ' + text + ' : ' + response +'\n') 
    message = {"answer": 'Bạn đã thêm sách có mã ' + text + ' vào giỏ hàng của mình giá quyển sách là: ' + response}
    list_sent=[]
    with open('bill.txt', encoding="utf8") as f:
        train_lines = f.readlines()
        for line in train_lines:
            line = line.split(':')
            for i in range(len(line)):
                line[i] = line[i].strip()
            list_sent.append(line)
    get_Price = []
    for i in list_sent:
        get_Price.append(i[1])
    total_price = 0
    for i in get_Price:
        total_price += int(i)
    file.write('tong gia book la: '+str(total_price) + '\n')
    return jsonify(message)
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    if is_number(text):
        response = book_response(text)
        list_of_intents = intents['book']
        for i in list_of_intents:
            if(i['tag']== text):
                result = i['name']
                break
        result1 = ''.join(result)
        file =open('bill.txt','a', encoding='utf8')
        file.write('giá quyển sách ' + text + ' có tên ' + result1 + ' : ' + response +'\n') 
        message = {"answer": 'Bạn đã thêm sách mã ' + text + ' có tên ' + result1 + ' vào giỏ hàng của mình giá quyển sách là: ' + response + ' Nếu xác nhận thanh toán quý khách vui lòng gõ [thanhtoan] xin cảm ơn'}
    elif 'ĐC' in text:
        file =open('bill.txt','a', encoding='utf8')
        file.write(text)
        message = {"answer": 'Bạn đã nhập địa chỉ: ' + text +' Đơn hàng sẽ giao sớm cho bạn, xin cảm ơn!'}
        
    elif 'DoiSanPham' in text:
        file =open('DoiSanPham.txt','a', encoding='utf8')
        file.write(text)
        message = {"answer": 'Nhà sách đã ghi nhận phản hồi của bạn bạn, xin cảm ơn!'}
    elif text == 'thanhtoan':
        list_sent=[]
        with open('bill.txt', encoding="utf8") as f:
            train_lines = f.readlines()
            for line in train_lines:
                line = line.split(':')
                for i in range(len(line)):
                    line[i] = line[i].strip()
                list_sent.append(line)
        get_Price = []
        for i in list_sent:
            get_Price.append(i[1])
        total_price = 0
        for i in get_Price:
            total_price += int(i)
        file =open('bill.txt','a', encoding='utf8')
        file.write('Tổng giá sách của bạn là: '+str(total_price) + '\n')
        file =open('bill.txt', encoding='utf8')
        textfile = file.read()
        message = {"answer": 'Xin cảm ơn quý khách, quý khách vui lòng kiểm tra lại hoán đơn \n'  +str(textfile) + ' Vui lòng nhập địa chỉ của bạn bằng cú pháp [DC + Địa chỉ của bạn]'}
    else:
        response = chatbot_response(text)
        message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run()