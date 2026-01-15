from flask import Flask
from src.models.listing_model import db 

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkup.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key' # Needed for session security later
    
    # Initialize the IMPORTED db instance with this app
    db.init_app(app)
    
    # Create tables context
    with app.app_context():
        # This creates tables if they don't exist yet
        db.create_all()

    # Register Blueprints
    from src.api.bot_routes import bot_bp
    app.register_blueprint(bot_bp)
    
    @app.route("/")
    def home():
        return "LinkUp Bot Enterprise Edition is Running!"
        
    return app