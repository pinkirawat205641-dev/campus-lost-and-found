import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_for_bca_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/lost_and_found_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    items = db.relationship('Item', backref='owner', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Electronics, Books, Accessories, Others
    status = db.Column(db.String(50), nullable=False)    # Lost, Found, Claimed
    image_path = db.Column(db.String(255), nullable=True)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(150), nullable=False)
    contact_info = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access your requested page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    status_filter = request.args.get('status', '')

    query = Item.query
    if search_query:
        query = query.filter(Item.title.ilike(f'%{search_query}%') | Item.description.ilike(f'%{search_query}%'))
    if category_filter:
        query = query.filter_by(category=category_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)

    items = query.order_by(Item.date_reported.desc()).all()
    return render_template('index.html', items=items, search_query=search_query, category_filter=category_filter, status_filter=status_filter)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Please check your login details and try again.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        status = request.form.get('status')
        location = request.form.get('location')
        contact_info = request.form.get('contact_info')
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # To prevent filename collisions
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image_path = unique_filename
                
        new_item = Item(
            title=title,
            description=description,
            category=category,
            status=status,
            location=location,
            contact_info=contact_info,
            image_path=image_path,
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item posted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/item/<int:id>')
def item_detail(id):
    item = Item.query.get_or_404(id)
    return render_template('item_detail.html', item=item)

@app.route('/item/<int:id>/update_status', methods=['POST'])
@login_required
def update_status(id):
    item = Item.query.get_or_404(id)
    if item.owner.id != current_user.id:
        flash('You do not have permission to update this item.', 'danger')
        return redirect(url_for('item_detail', id=item.id))
        
    new_status = request.form.get('status')
    if new_status in ['Lost', 'Found', 'Claimed']:
        item.status = new_status
        db.session.commit()
        flash('Status updated successfully.', 'success')
        
    return redirect(url_for('item_detail', id=item.id))

# --- ADMIN ROUTES ---

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_items = Item.query.count()
    total_lost = Item.query.filter_by(status='Lost').count()
    total_found = Item.query.filter_by(status='Found').count()
    total_claimed = Item.query.filter_by(status='Claimed').count()
    return render_template('admin_dashboard.html', 
                            total_users=total_users, 
                            total_items=total_items,
                            total_lost=total_lost,
                            total_found=total_found,
                            total_claimed=total_claimed)

@app.route('/admin/items')
@login_required
@admin_required
def admin_items():
    items = Item.query.order_by(Item.date_reported.desc()).all()
    return render_template('admin_items.html', items=items)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_item/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully by administrator.', 'success')
    return redirect(url_for('admin_items'))

@app.route('/admin/delete_user/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin_users'))
    
    Item.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        # Ensure uploads folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        db.create_all()
        
        # Create default admin if none exists
        admin_user = User.query.filter_by(email='admin@college.edu').first()
        if not admin_user:
            admin_user = User(
                name='Platform Administrator', 
                email='admin@college.edu', 
                password_hash=generate_password_hash('admin', method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin created: admin@college.edu | password: admin")
            
    app.run(debug=True, port=5000)
