from datetime import date
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .exts import db
import os
from flask import current_app
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__, url_prefix='/auth')



@auth.route('/upload_avatar/', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session:
        flash('请先登录')
        return redirect(url_for('auth.login'))

    file = request.files.get('avatar')
    if not file:
        flash('未选择文件')
        return redirect(url_for('auth.profile', user_id=session['user_id']))

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1]
    avatar_filename = f"user_{session['user_id']}{ext}"
    save_path = os.path.join(current_app.static_folder, 'user_image', avatar_filename)
    file.save(save_path)

    # 更新用户头像路径
    user = User.query.get(session['user_id'])
    user.avatar = f"/static/user_image/{avatar_filename}"
    db.session.commit()

    flash('头像上传成功')
    return redirect(url_for('auth.profile', user_id=user.id))

# 注册页面
@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 校验唯一性
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('邮箱已注册')
            return redirect(url_for('auth.register'))

        hashed_pwd = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()

        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# 登录页面
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('登录成功')
            return redirect(url_for('article.index'))  # 你的首页
        flash('邮箱或密码错误')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


# 退出登录
@auth.route('/logout/')
def logout():
    session.pop('user_id', None)
    flash('您已退出登录')
    return redirect(url_for('article.index'))


# 个人主页
@auth.route('/profile/<int:user_id>/')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@auth.route('/checkin/', methods=['POST'])
def checkin():
    if 'user_id' not in session:
        flash('请先登录')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    today = date.today()
    if user.last_checkin_date == today:
        return render_template('profile.html', user=user, message="今天已签到，请勿重复签到")

    # 随机经验值
    exp = random.randint(5, 10)
    user.exp += exp
    user.last_checkin_date = today

    # 升级逻辑
    level_exp = [0, 100, 250, 450, 700, 1000]  # 每级所需经验
    for lvl in range(user.level, 6):
        if user.exp >= level_exp[lvl]:
            user.level = lvl
        else:
            break

    db.session.commit()
    return render_template('profile.html', user=user, message=f"签到成功，获得 {exp} 点经验！")