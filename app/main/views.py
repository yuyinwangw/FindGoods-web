from flask import render_template, redirect, url_for, session, flash
from flask_login import UserMixin, login_user, current_user, login_required, logout_user
from . import main
from .forms import LoginForm, RegisterForm
from .. import db, login_manager
from ..models import Item, Plform, Userdetail

users = {'JOJO': {'password': 'jojo'}}


class User(UserMixin):
    """
 設置一： 只是假裝一下，所以單純的繼承一下而以 如果我們希望可以做更多判斷，
 如is_administrator也可以從這邊來加入
 """
    pass


@login_manager.user_loader
def user_loader(email):
    """
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id
 :param email:官網此例將email當id使用，賦值給予user.id
 """
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@main.route('/protected')
@login_required
def protected():
    """
 在login_user(user)之後，我們就可以透過current_user.id來取得用戶的相關資訊了
 """
    #  current_user確實的取得了登錄狀態
    if current_user.is_active:
        return 'Logged in as: ' + current_user.id + 'Login is_active:True'


@main.route('/register.html', methods=['GET', 'POST'])
def register():
    # print(session)
    loginform = LoginForm()
    reform = RegisterForm()
    if reform.validate_on_submit():
        user = Userdetail.query.filter_by(username=reform.username.data.lower()).first()
        if user is not None and user.verify_password(reform.password.data):
            login_user(user, reform.remember_me.data)
            return redirect(url_for('.protected'))
        flash('Invalid username or password.')
        return redirect(url_for('.protected'))

    elif loginform.validate_on_submit():
        if loginform.password.data == users['JOJO']['password']:
            user = User()
            user.id = loginform.username.data
            login_user(user, loginform.remember_me.data)
            # return redirect(url_for('.protected'))
            return redirect(url_for('.index'))
        flash('Invalid username or password.')
    # else:
    #     # login status
    #     if 'username' in session.keys():
    #         username = session['username']
    #         return render_template('register.html', loginform=loginform, username=username)
    #     else:
    #         # first time
    #         username = ''
    return render_template('register.html', loginform=loginform, reform=reform)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('You have been logged out, see you next time!!')
    return redirect(url_for('.register'))


@main.route('/', methods=['GET', 'POST'])
@main.route('/index.html', methods=['GET', 'POST'])
def index():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    dataInfo = [[d.ItemNo, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, u.PFName] for d, u in
                db.session.query(Item, Plform).filter(Item.PFNo == Plform.PFNo).filter(Plform.PFName == 'IKEA')]
    for i, data in enumerate(dataInfo):
        dataInfo[i][2] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    return render_template('index.html', dataInfo=dataInfo, username=username)


@main.route('/index2.html', methods=['GET'])
def index2():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    dataInfo = [[d.ItemNo, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, u.PFName] for d, u in db.session.query(Item, Plform).filter(Item.PFNo == Plform.PFNo).filter(Plform.PFName == 'IKEA')]
    for i, data in enumerate(dataInfo):
        dataInfo[i][2] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    return render_template('index2.html', dataInfo=dataInfo, username=username)


@main.route('/products.html', methods=['GET'])
def product():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('products.html', username=username)


@main.route('/search.html', methods=['GET'])
def search():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('search.html', username=username)


@main.route('/trend.html', methods=['GET'])
def trend():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('trend.html', username=username)


@main.route('/about.html', methods=['GET'])
def about():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('about.html', username=username)


@main.route('/myaccount.html', methods=['GET'])
def myaccount():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('myaccount.html', username=username)


@main.route('/cart.html', methods=['GET'])
def cart():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('cart.html', username=username)


@main.route('/checkout.html', methods=['GET'])
def checkout():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('checkout.html', username=username)


@main.route('/contact.html', methods=['GET'])
def contact():
    if 'username' in session.keys():
        username = session['username']
    else:
        username = ''
    return render_template('contact.html', username=username)