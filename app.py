from flask import Flask, request, jsonify, render_template
import dao.model_mysql as msql
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/source', static_folder='./static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xxxx@localhost:3306/SHOPDB'
db = SQLAlchemy(app)
# app.register_blueprint(test_controller, url_prefix='/otherfunctions')


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


@app.route('/show_items')
def hello_google():
    item_data = [[d.ItemNo, d.ItemName, str(d.Price), d.Brand, d.Cate] for d in db.session.query(Item)]
    print(item_data)
    column = ['No', 'Name', 'Price', 'Brand', 'Category']
    return render_template('show_item.html', data=item_data, column=column)


@app.route('/')
def index():
    sql = """
    SELECT itemname, price, url FROM item WHERE itemno = 'I0053' OR itemno = 'I0080';
    """
    data = msql.read_project_many(sql)
    path = []
    for i in data:
        path.append("img/" + i[0] + "_1.jpg")
    return render_template('index_blog.html', data=data, path=path)


@app.route('/index_blog.html')
def index2():
    sql = """
    SELECT itemname, price, url FROM item WHERE itemno = 'I0053' OR itemno = 'I0080';
    """
    data = msql.read_project_many(sql)
    path = []
    for i in data:
        path.append("img/" + i[0] + "_1.jpg")
    return render_template('index_blog.html', data=data, path=path)


@app.route('/search.html')
def search():
    return render_template('search.html')


@app.route('/trend.html')
def trend():
    return render_template('trend.html')


@app.route('/information.html')
def information():
    return render_template('information.html')


@app.route('/plateform_post', methods=['GET', 'POST'])
def plateform_post():
    pfname = ''
    data = ''
    column = ''
    requestMethod = request.method
    if requestMethod == 'POST':
        pfname = request.form.get('PL')
        data = msql.read_project("item", pfname)
        column = ['ITEMNO', 'ITEMNAME', 'PFNO', 'ITEMID', 'PRICE', 'BRAND', 'CATE', 'URL', 'IMG_PATH']
    return render_template(
        'ikea_post.html',
        requestMethod=requestMethod,
        pfname=pfname,
        data=data,
        column=column
    )


@app.route('/index.html')
def index3():
    item_data = [[d.ItemName, str(d.Price), d.URL] for d in db.session.query(Item)]
    print(item_data)
    # column = ['Name', 'Price', 'Url', 'Category']
    path = []
    for i in item_data:
        path.append("img/" + i[0] + "_1.jpg")
    pfname = request.form.get('PL')
    return render_template('index.html', data=item_data, path=path)


@app.route('/post.html')
def post():
    return render_template('post.html')


@app.route('/trending.html')
def trending():
    return render_template('trending.html')


@app.route('/author.html')
def author():
    return render_template('author.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)