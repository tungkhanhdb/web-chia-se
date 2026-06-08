from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, User, Document 
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
import os
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash("000000")
print(hashed_password)

app = Flask(__name__)
from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import os
UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tạo thư mục nếu nó chưa tồn tại (đề phòng)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bi-mat-cua-Admin' # Mã bảo mật

# Khởi tạo database
db.init_app(app)

with app.app_context():
    db.create_all()

# --- Các đường dẫn (Routes) ---

@app.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        all_docs = Document.query.filter(
            or_(
                Document.original_name.ilike(f'%{search_query}%'),
                Document.file_type.ilike(f'%{search_query}%')
            )
        ).all()
        
    else:
        all_docs = Document.query.all()
    return render_template('index.html', title='HỆ THỐNG CHIA SẺ TÀI LIỆU', documents=all_docs, current_user=current_user)

# --- Hàm login (đăng nhập) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 1. Lấy dữ liệu người dùng nhập
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Debug: Username nhận được là {username}, Password là {password}")
       
        # 2. Kiểm tra xem username có tồn tại hay chưa
        user = User.query.filter_by(username=username).first()

        # 3. Kiểm tra mật khẩu
        if user and check_password_hash(user.password, password):
            login_user(user) # nó sẽ tạo session cho user 

            flash(f"Chào mừng trở lại, {user.username}!")
            return redirect(url_for('index'))
        else:
            flash(f"nhập sai mật khẩu!")
    return render_template('login.html')

# --- Hàm logout (đăng xuất) ---
@app.route('/logout')
def logout():
    logout_user()
    flash("Đã đăng xuất thành công!", "info")
    return redirect(url_for('login'))

# --- Hàm regis (đăng ký) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        
        if not user_name or not pass_word:
            return "Yêu cầu nhập đúng thông tin!"

<<<<<<< HEAD
        # 3. Tạo hồ sơ mới từ cái khuôn User ở models.py
        hashed_password = generate_password_hash(pass_word)

        new_user = User(
            username=user_name,
            password=hashed_password,
            role='user'
)
        # 4. Lưu vào két (Database)
=======
        new_user = User(username=user_name, password=pass_word)
        
>>>>>>> 9527637642c83d9749bbc95f1956391f1e73d3f8
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Đăng ký thành công! Đã lưu vào database!")
            return redirect(url_for('login'))
        except:
            return "Có lỗi! Tên đăng nhập này có người sử dụng!"
            
    return render_template('register.html')

# --- hàm tải lên (upload) ---
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('files')
        if 'files' not in request.files:
            return "Không thấy file nào!"
        if not files or (len(files) == 1 and files[0].filename == ''): # Kiểm tra điều kiện về file
            return "Chưa chọn file nào cả!"
        for file in files:
            if file and file.filename != '':
            
               file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            new_doc = Document(
                filename=file.filename,         
                original_name=file.filename,
                file_type=file.filename.split('.')[-1], 
                user_id=current_user.id        
            )
            db.session.add(new_doc)
        db.session.commit() # lưu vào db
            
        return redirect(url_for('index'))
            
    return render_template('upload.html')

# --- Hàm xóa ---
@app.route('/delete/<int:id>')
@login_required
def delete_file(id):
<<<<<<< HEAD
    doc = Document.query.get_or_404(id) # Tìm file trong DB

    #nếu không phải admin thì chỉ được xóa file của mình
    if current_user.role != 'admin' and doc.user_id != current_user.id:
        flash ("bạn không có quyền xóa")
        return redirect(url_for('index'))



    # Xóa file vật lý trên server (nếu muốn)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Xóa record trong database
=======
    doc = Document.query.get_or_404(id) 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    if doc.user_id != current_user.id:
        flash("Không được quyền xóa tài liệu!")
        return redirect(url_for('index'))
>>>>>>> 9527637642c83d9749bbc95f1956391f1e73d3f8
    db.session.delete(doc)
    db.session.commit()

    flash("Đã xóa tài liệu!")
    return redirect(url_for('index'))

# --- Hàm sửa ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_file(id):
    doc = Document.query.get_or_404(id)

<<<<<<< HEAD
    if current_user.role != 'admin' and doc.user_id != current_user.id:
        flash("Bạn không có quyền sửa tài liệu này!")
=======
    if doc.user_id != current_user.id:
        flash("Không có quyền sửa tài liệu này!")
>>>>>>> 9527637642c83d9749bbc95f1956391f1e73d3f8
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Cập nhật tên mới từ form
        doc.original_name = request.form.get('new_name')
        db.session.commit()
        flash("Đã đổi tên tài liệu thành công!")
        return redirect(url_for('index'))
    return render_template('edit.html', doc=doc)

if __name__ == '__main__':
    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        print("Các bảng trong database:", inspector.get_table_names())
    
    app.run(debug=True)
