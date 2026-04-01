import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # secret key flask
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    # database postgresql
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/klasifikasi_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # upload folder jika nanti ada upload dataset
    UPLOAD_FOLDER = "uploads"

    # max upload file
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024