from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(200), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(15))
    cep = db.Column(db.String(9))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    renda_mensal = db.Column(db.Float)
    dependentes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    calculos = db.relationship('CalculoBeneficio', backref='user', lazy=True)
    tokens = db.relationship('Token', backref='user', lazy=True)

class CalculoBeneficio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    valor_beneficio = db.Column(db.Float, nullable=False)
    parametros = db.Column(db.Text)  # JSON com parâmetros usados
    pdf_path = db.Column(db.String(200))
    tipo_beneficio = db.Column(db.String(50))  # Novo campo

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    token_type = db.Column(db.String(20))  # 'email_verification' ou 'password_reset'
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)