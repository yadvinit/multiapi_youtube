from flask import Flask
from routes.main_routes import main_bp
from config import Config
from scheduler import init_scheduler
import atexit

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(main_bp)
    
    # intialize schedular
    scheduler = init_scheduler()
    atexit.register(lambda: scheduler.shutdown())
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()