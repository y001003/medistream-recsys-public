
from flask import Flask, render_template, request, url_for

# @app.route('/')
def create_app():
    app = Flask(__name__)

    from demo.routes import index
    from demo.routes import photo_detail

    app.register_blueprint(index.bp)
    app.register_blueprint(photo_detail.bp)
    return app

if __name__ ==  '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)