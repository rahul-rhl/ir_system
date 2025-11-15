import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    pass


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
