import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    MARKDOWN_FILE_PATH = os.environ.get("MARKDOWN_FILE_PATH")
    QDRANT_URL = os.environ.get("QDRANT_URL")
    QDRANT_API = os.environ.get("QDRANT_API")


class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(Config):
    DEBUG = True

configs = dict(
    dev=DevelopmentConfig,
    prod=Config,
    test=TestConfig
)

Config_is = configs[os.environ.get('CONFIG', 'dev')]
