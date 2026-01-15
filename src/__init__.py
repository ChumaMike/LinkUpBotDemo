from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register the Blueprints (Routes)
    from src.api.bot_routes import bot_bp
    app.register_blueprint(bot_bp)
    
    @app.route("/")
    def home():
        return "LinkUp Bot Enterprise Edition is Running!"
        
    return app