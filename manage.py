import os
# from main import create_app, db
from app.main import create_app, db
app = create_app(os.getenv('ENV') or 'prod')

if __name__ == '__main__':
    app.run()
