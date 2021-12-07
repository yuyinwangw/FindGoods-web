from flask import Flask, request, jsonify, render_template
import model_c

app = Flask(__name__, static_url_path='/static', static_folder='./static')
# app.register_blueprint(test_controller1, url_prefix='/otherfunctions')

@app.route('/index.html')
def index():
    dataInfo = model_c.getIkeaInfo()
    return render_template('index.html', dataInfo=dataInfo)

@app.route('/index2.html', methods=['GET'])
def index2():
    dataInfo = model_c.getIkeaInfo()
    return render_template('index2.html', dataInfo=dataInfo)

@app.route('/cart.html', methods=['GET'])
def cart():
    return render_template('cart.html')

@app.route('/checkout.html', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/product.html', methods=['GET'])
def product():
    return render_template('product.html')

@app.route('/register.html', methods=['GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
