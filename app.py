from flask import *
from flask_migrate import Migrate
from flask_sqlalchemy import *
from sqlalchemy import *
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = Flask
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_NAME = os.getenv('DB_NAME', 'instagram')
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SECRET_KEY'] = "F465656546666"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    gmail = Column(String)
    surname = Column(String)
    name = Column(String)
    parol = Column(String)
    commentary = Column(String)
    img = Column(String)
    save = db.relationship("Save", backref="users", order_by="Save.id")
    reels = db.relationship("Reels", backref="users", order_by="Reels.id")
    like = relationship("Reels", backref="like_by", secondary="like", order_by="Reels.id")
    follow = relationship("Follow", backref='users', order_by="Follow.id")
    comment_reel = db.relationship("Comment", backref='users', order_by="Comment.id")
    comment_like = db.relationship("Comment", backref='comment_like', secondary="like_comment", order_by="Comment.id")


class Follow(db.Model):
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer)
    following_id = Column(Integer, ForeignKey('users.id'))


class Reels(db.Model):
    __tablename__ = 'reels'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    reel = Column(String)
    reel_name = Column(String)
    like_count = Column(Integer)
    length_comment = Column(Integer)
    comment_reel = db.relationship("Comment", backref='reels', order_by="Comment.id")
    save = db.relationship("Save", backref="reels", order_by="Save.id")


def reels_filter():
    get = ''
    if "reel" in session:
        reels = Reels.query.filter(User.id == session["reel"]).first()
        get = reels
    return get


# def checkFile(filename):
#     value = '.' in filename
#     type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
#     return value and type_file


db.Table('like',
         db.Column('reel_id', db.Integer, db.ForeignKey('reels.id')),
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

db.Table('like_comment',
         db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')))


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    reel_id = Column(Integer, ForeignKey('reels.id'))
    text = Column(String)
    comment_li = Column(Integer, default=0)


class Save(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    reel_id = Column(Integer, ForeignKey('reels.id'))


@app.route('/comment_like/<int:comment_id>/<int:user_id>', methods=["POST", "GET"])
def comment_like(comment_id, user_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    user_num = User.query.filter(User.id == user_id).first()
    print(comment)
    like_id = []
    if user_num.comment_like:
        for like in user_num.comment_like:
            like_id.append(like.id)
        if comment.id in like_id:
            user_num.comment_like.remove(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li - 1
            })
            db.session.commit()
        else:
            user_num.comment_like.append(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li + 1
            })
            db.session.commit()

    else:
        user_num.comment_like.append(comment)
        db.session.commit()
        Comment.query.filter(Comment.id == comment_id).update({
            "comment_li": comment.comment_li + 1
        })
        db.session.commit()
    return redirect(url_for("kabinet", user_id=user_id))


@app.route('/comment_like_users/<int:comment_id>/<int:users7_id>', methods=["POST", "GET"])
def comment_like_users(comment_id, users7_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    user_num = User.query.filter(User.id == users7_id).first()
    like_co_users = []
    if user_num.comment_like:
        for like in user_num.comment_like:
            like_co_users.append(like.id)
        if comment.id in like_co_users:
            user_num.comment_like.remove(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li - 1
            })
            db.session.commit()
        else:
            user_num.comment_like.append(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li + 1
            })
            db.session.commit()

    else:
        user_num.comment_like.append(comment)
        db.session.commit()
        Comment.query.filter(Comment.id == comment_id).update({
            "comment_li": comment.comment_li + 1
        })
        db.session.commit()
    return redirect(url_for("users_follow", users7_id=users7_id))


@app.route('/comment_like_ins/<int:comment_id>/<int:user_id>', methods=["POST", "GET"])
def comment_like_ins(comment_id, user_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    user_num = User.query.filter(User.id == user_id).first()
    like_id1 = []
    if user_num.comment_like:
        for like in user_num.comment_like:
            like_id1.append(like.id)
        if comment.id in like_id1:
            user_num.comment_like.remove(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li - 1
            })
            db.session.commit()
        else:
            user_num.comment_like.append(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li + 1
            })
            db.session.commit()

    else:
        user_num.comment_like.append(comment)
        db.session.commit()
        Comment.query.filter(Comment.id == comment_id).update({
            "comment_li": comment.comment_li + 1
        })
        db.session.commit()
    return redirect(url_for("instagram", user_id=user_id))


@app.route('/comment_like_reels/<int:comment_id>/<int:user_id>', methods=["POST", "GET"])
def comment_like_reels(comment_id, user_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    user_num = User.query.filter(User.id == user_id).first()
    like_id1 = []
    if user_num.comment_like:
        for like in user_num.comment_like:
            like_id1.append(like.id)
        if comment.id in like_id1:
            user_num.comment_like.remove(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li - 1
            })
            db.session.commit()
        else:
            user_num.comment_like.append(comment)
            db.session.commit()
            Comment.query.filter(Comment.id == comment_id).update({
                "comment_li": comment.comment_li + 1
            })
            db.session.commit()

    else:
        user_num.comment_like.append(comment)
        db.session.commit()
        Comment.query.filter(Comment.id == comment_id).update({
            "comment_li": comment.comment_li + 1
        })
        db.session.commit()
    return redirect(url_for("reels", user_id=user_id))


@app.route('/save/<int:save_reel_id>/<int:save_id>', methods=["POST", "GET"])
def save(save_reel_id, save_id):
    user_filters = User.query.filter(User.id == save_id).first()
    reel_filter = Reels.query.filter(Reels.id == save_reel_id).first()
    add = Save(user_id=user_filters.id, reel_id=reel_filter.id)
    db.session.add(add)
    db.session.commit()
    return redirect(url_for('kabinet', user_id=user_filters.id))


# @app.route('/unsaved/<int:save_reel_id>/<int:save_id>', methods=["POST", "GET"])
# def unsaved(save_reel_id, save_id):
#     user_filters = Save.query.filter(User.id == save_id).first()
#     reel_filter = Save.query.filter(Save.id == save_reel_id).first()
#     add = Save(user_id=user_filters.id, reel_id=reel_filter.id)
#     db.session.delete(add)
#     db.session.commit()
#     return redirect(url_for('kabinet', user_id=user_filters.id))


@app.route('/add_comment/<int:id_reels_comment>/<int:users7_id>', methods=['POST', 'GET'])
def add_comment(id_reels_comment, users7_id):
    user_num = User.query.filter(User.id == session["id"]).first()
    follower = User.query.filter(User.id == users7_id).first()
    if request.method == "POST":
        comments = request.form.get('comment')
        filters = Reels.query.filter(Reels.id == id_reels_comment).first()
        soni = filters.length_comment
        add = Comment(text=comments, reel_id=id_reels_comment, user_id=user_num.id)
        db.session.add(add)
        db.session.commit()
        Reels.query.filter(Reels.id == id_reels_comment).update({
            'length_comment': soni + 1
        })
        db.session.commit()

    return redirect(url_for('users_follow', users7_id=follower.id))


@app.route('/add_comment_user/<int:id_reels_comment>/<int:users7_id>', methods=['POST', 'GET'])
def add_comment_user(id_reels_comment, users7_id):
    follower = User.query.filter(User.id == users7_id).first()
    if request.method == "POST":
        comments = request.form.get('comment')
        filters = Reels.query.filter(Reels.id == id_reels_comment).first()
        soni = filters.length_comment
        add = Comment(text=comments, reel_id=id_reels_comment, user_id=follower.id)
        db.session.add(add)
        db.session.commit()
        Reels.query.filter(Reels.id == id_reels_comment).update({
            'length_comment': soni + 1
        })
        db.session.commit()

    return redirect(url_for('kabinet', user_id=follower.id))


@app.route('/add_comment_ins/<int:id_reels_comment>/<int:users7_id>', methods=['POST', 'GET'])
def add_comment_ins(id_reels_comment, users7_id):
    follower = User.query.filter(User.id == users7_id).first()
    if request.method == "POST":
        comments = request.form.get('comment')
        filters = Reels.query.filter(Reels.id == id_reels_comment).first()
        soni = filters.length_comment
        add = Comment(text=comments, reel_id=id_reels_comment, user_id=follower.id)
        db.session.add(add)
        db.session.commit()
        Reels.query.filter(Reels.id == id_reels_comment).update({
            'length_comment': soni + 1
        })
        db.session.commit()

    return redirect(url_for('instagram', user_id=follower.id))


@app.route('/add_comment_reels/<int:id_reels_comment>/<int:users7_id>', methods=['POST', 'GET'])
def add_comment_reels(id_reels_comment, users7_id):
    follower = User.query.filter(User.id == users7_id).first()
    if request.method == "POST":
        comments = request.form.get('comment')
        filters = Reels.query.filter(Reels.id == id_reels_comment).first()
        soni = filters.length_comment
        add = Comment(text=comments, reel_id=id_reels_comment, user_id=follower.id)
        db.session.add(add)
        db.session.commit()
        Reels.query.filter(Reels.id == id_reels_comment).update({
            'length_comment': soni + 1
        })
        db.session.commit()

    return redirect(url_for('reels', user_id=follower.id))


@app.route('/follows/<int:username_id>/', methods=["POST", "GET"])
def follows(username_id):
    user = user_filter()
    follower = User.query.filter(User.id == username_id).first()
    follow = Follow.query.filter(Follow.following_id == user.id, Follow.follower_id == follower.id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
    else:
        add = Follow(following_id=user.id, follower_id=follower.id)
        db.session.add(add)
        db.session.commit()
    return redirect(url_for("users_follow", users7_id=follower.id))


@app.route('/add_like/<int:reel_id>/<int:users7_id>', methods=["POST", "GET"])
def add_like(reel_id, users7_id):
    post_name = Reels.query.filter(Reels.id == reel_id).first()
    user_num = User.query.filter(User.id == session["id"]).first()
    post_ids = []
    if user_num.like:
        for post in user_num.like:
            post_ids.append(post.id)
        if post_name.id in post_ids:
            user_num.like.remove(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count - 1
            })
            db.session.commit()
        else:
            user_num.like.append(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count + 1
            })
            db.session.commit()
    else:
        user_num.like.append(post_name)
        db.session.commit()
        Reels.query.filter(Reels.id == reel_id).update({
            "like_count": post_name.like_count + 1
        })
        db.session.commit()
    return redirect(url_for('users_follow', users7_id=users7_id))


@app.route('/add_like_ins/<int:reel_id>/<int:user_id>', methods=["POST", "GET"])
def add_like_ins(reel_id, user_id):
    post_name = Reels.query.filter(Reels.id == reel_id).order_by(Reels.id).first()
    user_num = User.query.filter(User.id == user_id).first()
    post_ids = []
    if user_num.like:
        for post in user_num.like:
            post_ids.append(post.id)
        if post_name.id in post_ids:
            user_num.like.remove(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count - 1
            })
            db.session.commit()
        else:
            user_num.like.append(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count + 1
            })
            db.session.commit()
    else:
        user_num.like.append(post_name)
        db.session.commit()
        Reels.query.filter(Reels.id == reel_id).update({
            "like_count": post_name.like_count + 1
        })
        db.session.commit()
    like_id = []
    for post_like in user_num.like:
        like_id.append(post_like.id)
    return redirect(url_for('instagram', user_id=user_id))


@app.route('/add_like_user/<int:reel_id>/<int:user_id>', methods=["POST", "GET"])
def add_like_user(reel_id, user_id):
    post_name = Reels.query.filter(Reels.id == reel_id).first()
    user_num = User.query.filter(User.id == user_id).first()
    post_ids = []
    if user_num.like:
        for post in user_num.like:
            post_ids.append(post.id)
        if post_name.id in post_ids:
            user_num.like.remove(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count - 1
            })
            db.session.commit()
        else:
            user_num.like.append(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count + 1
            })
            db.session.commit()
    else:
        user_num.like.append(post_name)
        db.session.commit()
        Reels.query.filter(Reels.id == reel_id).update({
            "like_count": post_name.like_count + 1
        })
        db.session.commit()
    like_id = []
    for post_like in user_num.like:
        like_id.append(post_like.id)
    return redirect(url_for('kabinet', user_id=user_id))


@app.route('/add_like_reels/<int:reel_id>/<int:user_id>', methods=["POST", "GET"])
def add_like_reels(reel_id, user_id):
    post_name = Reels.query.filter(Reels.id == reel_id).order_by().first()
    user_num = User.query.filter(User.id == user_id).first()
    post_ids = []
    if user_num.like:
        for post in user_num.like:
            post_ids.append(post.id)
        if post_name.id in post_ids:
            user_num.like.remove(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count - 1
            })
            db.session.commit()
        else:
            user_num.like.append(post_name)
            db.session.commit()
            Reels.query.filter(Reels.id == reel_id).update({
                "like_count": post_name.like_count + 1
            })
            db.session.commit()
    else:
        user_num.like.append(post_name)
        db.session.commit()
        Reels.query.filter(Reels.id == reel_id).update({
            "like_count": post_name.like_count + 1
        })
        db.session.commit()
    like_id = []
    for post_like in user_num.like:
        like_id.append(post_like.id)
    return redirect(url_for('reels', user_id=user_id))


def user_filter():
    get = ''
    if "id" in session:
        users = User.query.filter(User.id == session["id"]).first()
        get = users
    return get


@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.gmail == username).first()
        if user:
            if check_password_hash(user.parol, password):
                session["id"] = user.id
                return redirect(url_for("instagram", user_id=user.id))
            else:
                return redirect(url_for("hello_world"))

    return render_template("login.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        surname = request.form.get("surname")
        name = request.form.get("name")
        parol = request.form.get("parol")
        password = generate_password_hash(parol, 'scrypt')
        add = User(gmail=gmail, surname=surname, name=name, parol=password)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("hello_world"))
    return render_template("register.html")


@app.route('/instagram/<int:user_id>')
def instagram(user_id):
    user = User.query.filter(User.id == user_id).first()
    users7 = User.query.all()
    list = []
    for users in user.follow:
        filter = User.query.filter(User.id == users.follower_id).first()
        list.append({'user': users.id, 'img': filter.img, "gmail": filter.gmail})
    reels = Reels.query.all()
    like_id = []
    for post_like in user.like:
        like_id.append(post_like.id)
    like_id1 = []
    for like in user.comment_like:
        like_id1.append(like.id)
    return render_template("instagram.html", like_id1=like_id1, user=user, users7=users7, follow_img=list, reels=reels,
                           like_id=like_id)


@app.route('/users_follow/<int:users7_id>', methods=["POST", "GET"])
def users_follow(users7_id):
    user = user_filter()
    users_get = User.query.filter(User.id == users7_id).first()
    reels_get = Reels.query.filter(Reels.user == users_get.id).order_by(Reels.id).all()
    followers = len(users_get.follow)
    follow1 = Follow.query.filter(Follow.follower_id == users_get.id).all()
    overall = len(follow1)
    post = len(reels_get)
    like_id = []
    for post_like in user.like:
        like_id.append(post_like.id)
    follow_id = []
    for follows in user.follow:
        follow_id.append(follows.id)
    like_co_users = []
    for like in users_get.comment_like:
        like_co_users.append(like.id)
    return render_template("users_follow.html", users_get=users_get, user=user, reels_get=reels_get, overall=overall,
                           follows=followers, users7_id=users7_id, post=post, like_id=like_id, follow_id=follow_id,
                           like_co_users=like_co_users)


@app.route('/account_edit/<int:user_id>/', methods=["POST", "GET"])
def account_edit(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        gmail = request.form.get("gmail")
        name = request.form.get("name")
        surname = request.form.get("surname")
        commentary = request.form.get("commentary")
        photo = request.files["photo"]
        photo_url = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        User.query.filter(User.id == user_id).update({
            "gmail": gmail,
            "name": name,
            "surname": surname,
            "img": photo_url,
            "commentary": commentary
        })
        db.session.commit()
        return redirect(url_for("kabinet", user_id=user_id))
    return render_template("kabinet_edit.html", user=user)


@app.route('/add_photo/<int:user_id>/', methods=["POST", "GET"])
def add_photo(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        photo = request.files["img"]
        reel_name = request.form.get("reel_name")
        photo_url = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        add = Reels(reel=photo_url, user=user_id, reel_name=reel_name, like_count=0, length_comment=0)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("kabinet", user_id=user_id))
    reels = Reels.query.filter(User.id == user_id).first()
    return render_template("add_photo.html", user=user, reels=reels)


@app.route('/kabinet/<int:user_id>/', methods=["POST", "GET"])
def kabinet(user_id):
    user = User.query.filter(User.id == user_id).first()
    reels = Reels.query.filter(Reels.user == user.id).order_by(Reels.id).all()
    overall = len(user.follow)
    follow = Follow.query.filter(Follow.follower_id == user.id).all()
    followers = len(follow)
    post = len(reels)
    save_reel = user.save
    like_ids = []
    for post_like in user.like:
        like_ids.append(post_like.id)
    for reele in reels:
        for comment in reele.comment_reel:
            print(comment.users)
    like_id = []
    for like in user.comment_like:
        like_id.append(like.id)
    return render_template("kabinet.html", user=user, reels=reels, overall=overall, follows=followers, post=post,
                           save_reel=save_reel, like_ids=like_ids, like_id=like_id)


@app.route('/delete_img/<int:user_id>/<int:reels_id>', methods=["POST", "GET"])
def delete_img(user_id, reels_id):
    user_ids = User.query.filter(User.id == user_id).first()
    reel = Reels.query.filter(Reels.id == reels_id).first()
    db.session.delete(reel)
    db.session.commit()
    return redirect(url_for("kabinet", user_id=user_ids))


@app.route('/reels/<int:user_id>/', methods=["POST", "GET"])
def reels(user_id):
    user = User.query.filter(User.id == user_id).first()
    reel = Reels.query.all()
    like_id1 = []
    for like in user.comment_like:
        like_id1.append(like.id)
    like_ids = []
    for post_like in user.like:
        like_ids.append(post_like.id)
    return render_template("reels.html", user=user, reel=reel, like_id1=like_id1, like_ids=like_ids)


if __name__ == '__main__':
    app.run()
