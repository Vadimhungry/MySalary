from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy
from dotenv import load_dotenv
import os


# get env variables
load_dotenv()
SECRET = os.getenv("SECRET_KEY")


cookie_transport = CookieTransport(
    cookie_max_age=3600,
    cookie_name='my_salary_cookie'
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
