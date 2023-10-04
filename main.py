from app import app
import views
from authentication.auth_blueprint import auth
from settings.settings_blueprint import settings
from user.user_blueprint import user_bp

app.register_blueprint(auth, url_prefix="/authentication")
app.register_blueprint(settings, url_prefix="/settings")
app.register_blueprint(user_bp, url_prefix = "/<username>")


if __name__ == "__main__":
    app.run()
