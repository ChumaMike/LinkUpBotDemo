from flask import Flask
from src.models.listing_model import db 
from src.models.user_model import User 

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkup.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    # --- REGISTER BLUEPRINTS ---
    
    # 1. Bot Routes 
    from src.api.bot_routes import bot_bp
    app.register_blueprint(bot_bp)
    
    # 2. Web Routes
    from src.api.web_routes import web_bp
    app.register_blueprint(web_bp)
    
    @app.route("/")
    def home():
        return "LinkUp Enterprise is Running!"
        
    return app