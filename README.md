# ==============================================
#          MANUAL DE INSTALAÇÃO COMPLETO
# ==============================================

# PRÉ-REQUISITOS
# - Python 3.8 ou superior
# - Pip (gerenciador de pacotes Python)
# - Git (opcional para clonar repositório)

# 1. CLONAR REPOSITÓRIO (OPCIONAL)
git clone https://github.com/seu-usuario/calculadora-fake.git
cd calculadora-fake

# 2. CONFIGURAR AMBIENTE VIRTUAL
python -m venv venv

# Ativação do ambiente:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. INSTALAR DEPENDÊNCIAS
pip install -r requirements.txt

# 4. CONFIGURAR VARIÁVEIS DE AMBIENTE
# Crie um arquivo .env na raiz do projeto com:
echo "SECRET_KEY=sua_chave_secreta_aqui" > .env
echo "DATABASE_URL=sqlite:///calculadora_fake.db" >> .env
echo "DEFAULT_EMAIL_PROVIDER=gmail" >> .env
echo "GMAIL_EMAIL=seu_email@gmail.com" >> .env
echo "GMAIL_PASSWORD=sua_senha" >> .env

# 5. INICIAR APLICAÇÃO
python app.py

# ACESSAR NO NAVEGADOR:
# http://localhost:5000

# ==============================================
#          COMANDOS ADICIONAIS ÚTEIS
# ==============================================

# Aplicar migrações de banco de dados:
flask db upgrade

# Executar testes:
pytest tests/

# Modo desenvolvimento com recarregamento:
flask run --debug

# Desativar ambiente virtual:
deactivate

# ==============================================
#          OBSERVAÇÕES IMPORTANTES
# ==============================================
# - Nunca compartilhe seu arquivo .env
# - O banco será criado automaticamente na 1ª execução
# - Para produção, use servidor WSGI (Gunicorn/Waitress)
# - Mantenha suas credenciais em segredo
