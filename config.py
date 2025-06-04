import secrets

SECRET_ADMIN_PATH = secrets.token_urlsafe(12)
print(f"Admin panel yolu: /admin/{SECRET_ADMIN_PATH}")
