import os
from dotenv import load_dotenv

load_dotenv(encoding='UTF-8')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_muito_segura_aqui')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/pdfs'
    ITEMS_PER_PAGE = 5
    TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION', 3600))  # 1 horaz
    
    # Configurações de e-mail dinâmicas
    EMAIL_PROVIDERS = {
        'gmail': {
            'server': 'smtp.gmail.com',
            'port': 587,
            'use_tls': True
        },
        'outlook': {
            'server': 'smtp.office365.com',
            'port': 587,
            'use_tls': True
        },
        'yahoo': {
            'server': 'smtp.mail.yahoo.com',
            'port': 587,
            'use_tls': True
        },
        'bol': {
            'server': 'smtp.bol.com.br',
            'port': 587,
            'use_tls': True
        }
    }
    DEFAULT_EMAIL_PROVIDER = os.getenv('DEFAULT_EMAIL_PROVIDER', 'gmail')