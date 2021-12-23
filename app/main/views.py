from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.orm import load_only
from . import main
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import Item, Plform, User

# users = {'JOJO': {'password': 'jojo'}}


# @main.route('/protected')
# @login_required
# def protected():
#     """
#  在login_user(user)之後，我們就可以透過current_user.id來取得用戶的相關資訊了
#  """
#     #  current_user確實的取得了登錄狀態
#     if current_user.is_active:
#         return 'Logged in as: ' + current_user.id + 'Login is_active:True'


@main.route('/register.html', methods=['GET', 'POST'])
def register():
    loginform = LoginForm()
    reform = RegisterForm()
    if reform.validate_on_submit():
        users = [d.username for d in User.query.options(load_only(User.username))]
        # print(len(users))
        if reform.username_r.data not in users:
            if len(users) == 0:
                user = User(id="1".zfill(4),
                            email=reform.email.data.lower(),
                            username=reform.username_r.data,
                            password=reform.password_r.data,
                            sex=reform.sex.data,
                            age=reform.age.data,
                            area=reform.area.data,
                            career=reform.career.data)
            else:
                first_data = User.query.order_by(User.id.desc()).first()
                new_id = str(int(first_data.id)+1).zfill(4)
                user = User(id=new_id,
                            email=reform.email.data.lower(),
                            username=reform.username_r.data,
                            password=reform.password_r.data,
                            sex=reform.sex.data,
                            age=reform.age.data,
                            area=reform.area.data,
                            career=reform.career.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, reform.remember_me_r.data)
            print(session)
            return redirect(url_for('.index'))
        flash('Username has been used!')

    elif loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user, loginform.remember_me.data)
            print(session)
            # return redirect(url_for('.protected'))
            return redirect(url_for('.index'))
        flash('Invalid username or password.')
    return render_template('register.html', loginform=loginform, reform=reform)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    print(session)
    # flash('You have been logged out, see you next time!!')
    return redirect(url_for('.register'))


@main.route('/', methods=['GET', 'POST'])
@main.route('/index.html', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    dataInfo = [[d.ItemNo, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, u.PFName] for d, u in
                db.session.query(Item, Plform).filter(Item.PFNo == Plform.PFNo).filter(Plform.PFName == 'IKEA')]
    for i, data in enumerate(dataInfo):
        dataInfo[i][2] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    return render_template('index.html', dataInfo=dataInfo, username=username)


@main.route('/index2.html', methods=['GET'])
def index2():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    dataInfo = [[d.ItemNo, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, u.PFName] for d, u in db.session.query(Item, Plform).filter(Item.PFNo == Plform.PFNo).filter(Plform.PFName == 'IKEA')]
    for i, data in enumerate(dataInfo):
        dataInfo[i][2] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    return render_template('index2.html', dataInfo=dataInfo, username=username)


@main.route('/myaccount.html', methods=['GET'])
def myaccount():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
        userInfo = []
        for d in User.query.filter(User.id == current_user.id):
            userInfo.append(["Username" ,d.username])
            userInfo.append(["Email", d.email])
            userInfo.append(["Sex", d.sex])
            userInfo.append(["Age", d.age])
            userInfo.append(["Living Place", d.area])
            userInfo.append(["Occupation", d.career])

        # userInfo = [d.username, d.email for d in User.query.filter(User.id == current_user.id)]
        # dict = {}
        # dict["Username"] = userInfo[0][0]
        # dict["Email"] = userInfo[0][1]
        # dict["Sex"] = userInfo[0][2]
        # dict["Age"] = userInfo[0][3]
        # dict["Living Place"] = userInfo[0][4]
        # dict["Occupation"] = userInfo[0][5]
    else:
        username = ''
        userInfo = ''
    return render_template('myaccount.html', userInfo=userInfo, username=username)


@main.route('/products.html', methods=['GET'])
def product():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    return render_template('products.html', username=username)


@main.route('/search.html', methods=['GET'])
def search():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    return render_template('search.html', username=username)


@main.route('/trend.html', methods=['GET'])
def trend():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    return render_template('trend.html', username=username)


@main.route('/about.html', methods=['GET'])
def about():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    return render_template('about.html', username=username)


# @main.route('/cart.html', methods=['GET'])
# def cart():
#     if 'username' in session.keys():
#         username = session['username']
#     else:
#         username = ''
#     return render_template('cart.html', username=username)
#
#
# @main.route('/checkout.html', methods=['GET'])
# def checkout():
#     if 'username' in session.keys():
#         username = session['username']
#     else:
#         username = ''
#     return render_template('checkout.html', username=username)
#
#
# @main.route('/contact.html', methods=['GET'])
# def contact():
#     if 'username' in session.keys():
#         username = session['username']
#     else:
#         username = ''
#     return render_template('contact.html', username=username)