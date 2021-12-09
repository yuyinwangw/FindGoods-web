from flask import Flask, request, jsonify, render_template
import Mysql_pwd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static', static_folder='./static')
# app.register_blueprint(test_controller1, url_prefix='/otherfunctions')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Mysql_pwd.pwd["pwd"]
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'item'

    ItemNo = db.Column(db.String(10), primary_key=True, nullable=False)
    ItemName = db.Column(db.String(60), nullable=False)
    PFNo = db.Column(db.SmallInteger, nullable=False)
    ItemID = db.Column(db.SmallInteger, nullable=False)
    Price = db.Column(db.Float)
    Brand = db.Column(db.String(16))
    Cate = db.Column(db.String(45))
    URL = db.Column(db.Text, nullable=False)
    IMG_Path = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Item %s>" % self.ItemName


@app.route('/index.html')
def index():
    # dataInfo = model_c.getIkeaInfo()
    dataInfo = [[d.ItemNo, d.ItemName, d.URL, str(d.Price), d.Brand, d.Cate] for d in db.session.query(Item)]
    for i, data in enumerate(dataInfo):
        dataInfo[i][1] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    return render_template('index.html', dataInfo=dataInfo)
    # , dataInfo=dataInfo


@app.route('/index2.html', methods=['GET'])
def index2():
    # dataInfo = model_c.getIkeaInfo()
    dataInfo = [[d.ItemNo, d.ItemName, str(d.Price), d.Brand, d.Cate] for d in db.session.query(Item)]
    return render_template('index2.html', dataInfo=dataInfo)
    # , dataInfo=dataInfo


@app.route('/products.html', methods=['GET'])
def product():
    return render_template('products.html')


@app.route('/search.html', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/trend.html', methods=['GET'])
def trend():
    return render_template('trend.html')


@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/cart.html', methods=['GET'])
def cart():
    return render_template('cart.html')


@app.route('/checkout.html', methods=['GET'])
def checkout():
    return render_template('checkout.html')


@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/register.html', methods=['GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
