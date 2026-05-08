from flask import Flask

from models import User
from extensions import db, login_manager
from config import settings
from blueprints.index import router as main_bp

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.execute(
            db.Select(User)
            .where(User.id == int(user_id))
        ).scalar_one_or_none()
        
    app.register_blueprint(main_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run("0.0.0.0", 5000, debug=True)