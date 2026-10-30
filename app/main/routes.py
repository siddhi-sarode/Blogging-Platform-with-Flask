from app.main import bp

@bp.route('/')
def index():
    return "Task 1 Complete: Flask App with Blueprints, SQLAlchemy, and Migrate is running!"