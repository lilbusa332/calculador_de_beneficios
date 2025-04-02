from flask_mail import Mail, Message
from flask import current_app, render_template, url_for
from threading import Thread
from datetime import datetime, timedelta
from database import db, Token
import uuid
import os

mail = Mail()

class EmailSender:
    def __init__(self):
        self.mail = Mail()
    
    def send_email(self, subject, recipient, template, provider=None, **kwargs):
        app = current_app._get_current_object()
        provider = provider or app.config['DEFAULT_EMAIL_PROVIDER']
        
        if provider not in app.config['EMAIL_PROVIDERS']:
            raise ValueError(f"Provedor {provider} não configurado")
            
        provider_config = app.config['EMAIL_PROVIDERS'][provider]
        
        # Configuração dinâmica
        app.config['MAIL_SERVER'] = provider_config['server']
        app.config['MAIL_PORT'] = provider_config['port']
        app.config['MAIL_USE_TLS'] = provider_config['use_tls']
        app.config['MAIL_USERNAME'] = os.getenv(f'{provider.upper()}_EMAIL')
        app.config['MAIL_PASSWORD'] = os.getenv(f'{provider.upper()}_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv(f'{provider.upper()}_EMAIL')
        
        self.mail.init_app(app)
        
        msg = Message(
            subject,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[recipient]
        )
        msg.html = render_template(template, **kwargs)
        
        Thread(target=self._send_async, args=(app, msg)).start()
    
    def _send_async(self, app, msg):
        with app.app_context():
            try:
                self.mail.send(msg)
                print(f"E-mail enviado com sucesso para {msg.recipients}")
            except Exception as e:
                print(f"Erro ao enviar e-mail: {str(e)}")

    def generate_token(self, user, token_type, expires_in=3600):
        # Revoga tokens antigos do mesmo tipo
        Token.query.filter_by(user_id=user.id, token_type=token_type, used=False).update({'used': True})
        db.session.commit()
        
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        new_token = Token(
            user_id=user.id,
            token=token,
            token_type=token_type,
            expires_at=expires_at
        )
        
        db.session.add(new_token)
        db.session.commit()
        return token

    def send_confirmation_email(self, user, provider=None):
        token = self.generate_token(user, 'email_verification')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        self.send_email(
            subject='Confirme seu email - Sistema Calculadora Fake',
            recipient=user.email,
            template='email/confirmation.html',
            provider=provider,
            user=user,
            confirm_url=confirm_url,
            now=datetime.utcnow()
        )

    def send_password_reset_email(self, user, provider=None):
        token = self.generate_token(user, 'password_reset')
        reset_url = url_for('reset_password', token=token, _external=True)
        self.send_email(
            subject='Redefinição de Senha - Sistema Calculadora Fake',
            recipient=user.email,
            template='email/reset.html',
            provider=provider,
            user=user,
            reset_url=reset_url,
            now=datetime.utcnow()
        )

email_sender = EmailSender()