from app import app
import views

from authentication.auth_blueprint import auth

app.register_blueprint(auth, url_prefix="/authentication")

if __name__ == "__main__":
    app.run()

