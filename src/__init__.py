from flask import Flask
from flask_login import LoginManager # <-- Import this
from src.models.listing_model import db 
from src.models.user_model import User 

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkup.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-this-in-prod' # CRITICAL for login
    
    db.init_app(app)
    
    # --- NEW: Setup Login Manager ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Where to send users if they aren't logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -------------------------------

    with app.app_context():
        db.create_all()

    # Register Blueprints
    from src.api.bot_routes import bot_bp
    app.register_blueprint(bot_bp)
    
    from src.api.web_routes import web_bp
    app.register_blueprint(web_bp)

    # We will create this next!
    from src.api.auth_routes import auth_bp 
    app.register_blueprint(auth_bp)
    
    @app.route("/")
    def home():
        return "LinkUp Enterprise is Running!"
        
    return app