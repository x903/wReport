import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from datetime import datetime
from flask import Flask, request, current_app
from flask_admin import Admin
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.json_encoder import JSONEncoder
from app.utils import get_last_week_content, get_week_days



bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = "basic"
login_manager.login_view = 'auth.login'

app = Flask(__name__)

babel = Babel()

admin = Admin(app, name='WeeklyReport', template_mode='bootstrap3')

@babel.localeselector
def get_locale():
    #return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'zh_Hans_CN'


def create_app(config_file):

    app.config.from_pyfile(config_file)

    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .report import report as report_blueprint
    app.register_blueprint(report_blueprint, url_prefix='/report')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # chartkick support
    app.jinja_env.add_extension('chartkick.ext.charts')

    # i18n support
    app.jinja_env.add_extension('jinja2.ext.i18n')

    # jinja env to help check statistics page under this week
    app.jinja_env.globals.update(
        get_this_week_count=lambda: datetime.now().isocalendar()[1])

    # lazy_gettext Json Error Fix
    app.json_encoder = JSONEncoder
    
    app.add_template_filter(get_last_week_content, 'get_last_week_content')
    app.add_template_filter(get_week_days, 'get_week_days')
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='WeeklyReport Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/WeeklyReport.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('WeeklyReport startup')
    return app

from . import models