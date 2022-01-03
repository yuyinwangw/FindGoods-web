from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.orm import load_only
import app
from . import main
from .forms import LoginForm, RegisterForm, PhotoForm
from .. import db
from ..models import Item, Plform, User
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# def allowed_file(filename):
#     return '.' in filename and filename.lower().rsplit('.', 1)[1] in ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')

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
    tags = ('vasesbowl','frames','lamps','footstool','Cushion','mugs','desk')
    dataInfo = [[d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, d.TAGS] for d in db.session.query(Item)]
    # dataInfo = []
    info = {}
    # for i, data in enumerate(dataInfo):
    #     dataInfo[i][1] = ("img/ikea_photos/" + data[0] + "_1.jpg")
    for i in tags:
        if i not in info.items():
            info[i]=list()
        for data in dataInfo:
            if data[5]==i:
                info[i].append(data)
    # print(info['frames'])


    # print(tags[0])
    # print(dataInfo[0])
    # dataInfo = []
    return render_template('index.html', dataInfo=info, username=username, tags=tags)


@main.route('/index2.html', methods=['GET'])
def index2():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    dataInfo = [[d.ItemNo, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate, u.PFName] for d, u in db.session.query(Item, Plform).filter(Item.PFNo == Plform.PFNo)]
    # for i, data in enumerate(dataInfo):
    #     dataInfo[i][2] = ("img/ikea_photos/" + data[1] + "_1.jpg")
    # dataInfo = []

    return render_template('index2.html', dataInfo=dataInfo, username=username)

#冷啟動，此用者偏好選單
@main.route('/main_select')
def index3():
    dataInfo = []
    return render_template('main_select.html', dataInfo=dataInfo)

#content-base推薦
@main.route('/recommend/<itemid>')
def recommend(itemid):
    data = [[d.ItemID ,d.Cate]  for d in db.session.query(Item)]
    df2 = pd.DataFrame(data, columns=['title','keywords'])
    count = CountVectorizer()
    count_matrix = count.fit_transform(df2['keywords'])

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(df2.index, index=df2['title'])
    # print(indices)
    # user_select = [[d.ItemID, d.Cate] for d in db.session.query(Item).filter(Item.ItemID == itemid)]
    userselect = [[d.ItemNo,d.ItemID, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate]  for d in db.session.query(Item).filter(Item.ItemID == itemid)]
    def get_recommendations(itemid, n = 10, cosine_sim=cosine_sim2):
        ikea = []
        if itemid not in indices.index:
            print("furniture not in database.")
            return
        else:
            idx = indices[itemid]
        # cosine similarity scores of movies in descending order
        scores = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        # top n most similar movies indexes
        # use 1:n because 0 is the same movie entered
        top_n_idx = list(scores.iloc[1:n].index)
        return df2['title'].iloc[top_n_idx]
    recomItem = get_recommendations(int(itemid), n=9, cosine_sim=cosine_sim2).values.tolist()
    # print(tuple(recomItem))
    # recomlist = tuple([i for i in map(lambda x:str(x) ,recomItem)])
    dataInfo = [[d.ItemID, d.ItemName, d.IMG_Path, d.URL, str(d.Price), d.Brand, d.Cate]  for d in db.session.query(Item).filter(Item.ItemID.in_(recomItem))]
    # print(dataInfo)
    # dataInfo = []
    return render_template('contentbase.html',userselect=userselect, dataInfo=dataInfo)


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


@main.route('/search.html', methods=['GET', 'POST'])
def search():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        username = user.username
    else:
        username = ''
    imgform = PhotoForm()
    print(imgform.image.data)
    print(app.config['default'].UPLOAD_FOLDER)
    if imgform.validate_on_submit():
        image = imgform.image.data
        print(image)
        filename = image.filename
        print(filename)
        image.save(os.path.join(app.config['default'].UPLOAD_FOLDER, filename))
        uploadfile_path = 'img/uploads/' + filename
        print(uploadfile_path)
        return render_template('search.html', username=username, uploadfile_path=uploadfile_path, imgform=imgform)
    elif imgform.errors:
        print("error")
        flash(imgform.errors['image'][0])
    return render_template('search.html', username=username, imgform=imgform)


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