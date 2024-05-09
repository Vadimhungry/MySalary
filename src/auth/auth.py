from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy


cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name='my_salary_cookie')

# todo закинуть секрет в .env
SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)