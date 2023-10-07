from app import app
import views
from authentication.auth_blueprint import auth
from settings.settings_blueprint import settings
from user.user_blueprint import user_bp
from projects.projects_bp import projects_bp

app.register_blueprint(auth, url_prefix="/authentication")
app.register_blueprint(settings, url_prefix="/settings")
app.register_blueprint(user_bp, url_prefix="/<username>")
app.register_blueprint(projects_bp, url_prefix = "/projects")


if __name__ == "__main__":
    app.run()
