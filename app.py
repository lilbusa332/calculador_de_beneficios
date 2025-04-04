from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, CalculoBeneficio, Token
from datetime import datetime, timedelta
import os
import json
from pdf_generator import generate_pdf_report
from email_service import mail, email_sender
from config import Config
from sqlalchemy import or_
import uuid
from dotenv import load_dotenv

try:
    load_dotenv(encoding='utf-8')
except UnicodeDecodeError:
    try:
        load_dotenv(encoding='utf-8-sig')
    except:
        load_dotenv(encoding='latin-1') 


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas de Autenticação
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'signup' in request.form:
            return handle_signup()
        elif 'login' in request.form:
            return handle_login()
        elif 'forgot_password' in request.form:
            return handle_forgot_password()
    
    return render_template('auth.html')

def handle_signup():
    cpf = request.form.get('cpf').replace('.', '').replace('-', '')
    nome = request.form.get('nome')
    email = request.form.get('email').lower()
    password = request.form.get('password')
    data_nascimento = request.form.get('data_nascimento')
    telefone = request.form.get('telefone')
    cep = request.form.get('cep')
    endereco = request.form.get('endereco')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    
    if User.query.filter(or_(User.email == email, User.cpf == cpf)).first():
        flash('Email ou CPF já cadastrado', 'error')
        return redirect(url_for('auth'))
    
    new_user = User(
        cpf=cpf,
        nome=nome,
        email=email,
        password=generate_password_hash(password),
        data_nascimento=data_nascimento,
        telefone=telefone,
        cep=cep,
        endereco=endereco,
        cidade=cidade,
        estado=estado
    )
    user_data = {
        'nome': new_user.nome,
        'email': new_user.email,
        'cpf': new_user.cpf,
        'data_nascimento': new_user.data_nascimento.isoformat() if new_user.data_nascimento else None,
        'telefone': new_user.telefone,
        'cep': new_user.cep,
        'endereco': new_user.endereco,
        'cidade': new_user.cidade,
        'estado': new_user.estado,
        'data_cadastro': datetime.utcnow().isoformat()
        

    }
    
    db.session.add(new_user)
    db.session.commit()

    salvar_dados_json(user_data, 'usuario')
    
   # email_sender.send_confirmation_email(new_user)
    flash('Cadastro realizado! Verifique seu email para confirmar sua conta.', 'success')
    return redirect(url_for('auth'))

def handle_login():
    email = request.form.get('email').lower()
    password = request.form.get('password')
    remember = 'remember' in request.form
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Credenciais inválidas', 'error')
        return redirect(url_for('auth'))
    
    if not user.email_verified:
        flash('Por favor, verifique seu email antes de fazer login', 'warning')
        return redirect(url_for('auth'))
    
    login_user(user, remember=remember)
    return redirect(url_for('dashboard'))

def handle_forgot_password():
    email = request.form.get('email').lower()
    user = User.query.filter_by(email=email).first()
    
    if user:
        email_sender.send_password_reset_email(user)
    
    flash('Se o email estiver cadastrado, você receberá instruções para redefinir sua senha', 'info')
    return redirect(url_for('auth'))


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}
# Rotas de Confirmação de Email e Redefinição de Senha
@app.route('/confirmar-email/<token>')
def confirm_email(token):
    token_record = Token.query.filter_by(token=token, used=False).first()
    
    if not token_record or token_record.token_type != 'email_verification' or token_record.expires_at < datetime.utcnow():
        flash('Link inválido ou expirado', 'error')
        return redirect(url_for('auth'))
    
    user = User.query.get(token_record.user_id)
    user.email_verified = True
    token_record.used = True
    db.session.commit()
    
    flash('Email confirmado com sucesso! Agora você pode fazer login.', 'success')
    return redirect(url_for('auth'))

@app.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def reset_password(token):
    token_record = Token.query.filter_by(token=token, used=False).first()
    
    if not token_record or token_record.token_type != 'password_reset' or token_record.expires_at < datetime.utcnow():
        flash('Link inválido ou expirado', 'error')
        return redirect(url_for('auth'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('reset_password', token=token))
        
        user = User.query.get(token_record.user_id)
        user.password = generate_password_hash(password)
        token_record.used = True
        db.session.commit()
        
        flash('Senha redefinida com sucesso! Faça login com sua nova senha.', 'success')
        return redirect(url_for('auth'))
    
    return render_template('reset_password.html', token=token)

# Rotas do Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    calculos = CalculoBeneficio.query.filter_by(user_id=current_user.id)\
        .order_by(CalculoBeneficio.data_calculo.desc())\
        .paginate(page=page, per_page=app.config['ITEMS_PER_PAGE'])
    
    return render_template('dashboard.html', user=current_user, calculos=calculos)

@app.route('/calcular-beneficio', methods=['POST'])
@login_required
def calcular_beneficio():
    try:
        data = request.get_json()
        renda = float(data['renda'])
        dependentes = int(data['dependentes'])
        tipo_beneficio = data['tipo_beneficio']
        
        # Algoritmo de cálculo melhorado
        valor_beneficio = calcular_valor_beneficio(renda, dependentes, tipo_beneficio)
        
        # Salvar cálculo
        novo_calculo = save_calculo(renda, dependentes, tipo_beneficio, valor_beneficio)
        
        # Gerar PDF
        pdf_filename = generate_pdf(novo_calculo, renda, dependentes)
        
        return jsonify({
            'success': True,
            'valor_beneficio': valor_beneficio,
            'pdf_url': url_for('download_pdf', filename=pdf_filename),
            'data_calculo': novo_calculo.data_calculo.strftime('%d/%m/%Y %H:%M')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def calcular_valor_beneficio(renda, dependentes, tipo_beneficio):
    # Algoritmo mais complexo e realista
    if tipo_beneficio == 'bolsa_familia':
        if renda <= 89 * dependentes + 178:
            return 600 + (150 * dependentes)
        elif renda <= 178 * dependentes + 356:
            return 400 + (100 * dependentes)
        else:
            return 200 + (50 * dependentes)
    elif tipo_beneficio == 'auxilio_emergencial':
        return min(600 * (1 + dependentes * 0.2), 1200)
    else:  # Benefício genérico
        base = max(1000 - (renda * 0.2), 300)
        return base + (200 * dependentes)

def save_calculo(renda, dependentes, tipo_beneficio, valor_beneficio):
    novo_calculo = CalculoBeneficio(
        user_id=current_user.id,
        valor_beneficio=valor_beneficio,
        parametros=json.dumps({
            'renda': renda,
            'dependentes': dependentes,
            'tipo_beneficio': tipo_beneficio
        }),
        tipo_beneficio=tipo_beneficio
    )
    
    db.session.add(novo_calculo)
    db.session.commit()
    return novo_calculo

def generate_pdf(calculo, renda, dependentes):
    pdf_filename = f"beneficio_{current_user.id}_{calculo.id}.pdf"
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    generate_pdf_report(
        current_user,
        calculo.valor_beneficio,
        pdf_path,
        renda,
        dependentes,
        calculo.tipo_beneficio,
        calculo.data_calculo
    )
    
    calculo.pdf_path = pdf_filename
    db.session.commit()
    return pdf_filename

# Outras rotas
@app.route('/download-pdf/<filename>')
@login_required
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#salvar dados num arquivo json
def salvar_dados_json(dados, nome, arquivo='dados.json'):
    try:
        if hasattr(dados, '__table__'):
            dados = {col.name: getattr(dados, col.name) for col in dados.__table__.columns}
            dados['data_cadastro'] = datetime.utcnow().isoformat()

        registro = {
            'tipo_registro': nome,
            'data_registro': datetime.utcnow().isoformat(),
            'dados': {
                'nome': dados.get('nome'),
                'email': dados.get('email'),
                'data_nascimento': dados.get('data_nascimento'),
                'telefone': dados.get('telefone'),
                'cep': dados.get('cep'),
                'cidade': dados.get('cidade'),
                'estado': dados.get('estado')
            }
        }


        existing_data = []
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        existing_data.append(registro)


        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        print(f'Registro de {nome} salvo em {arquivo}')
    except Exception as e:
        print(f'Erro ao salvar dados: {str(e)}')

        if app.debug:
            import traceback
            traceback.print_exc()