<div style="font-family: Arial, sans-serif; font-size: 13px; line-height: 1.4; color: #24292e; max-width: 800px;">

<h2 style="font-size: 18px; color: #24292e; margin-top: 24px; margin-bottom: 16px; font-weight: 600; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.3em;">
📖 Manual de Instalação
</h2>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
📋 Pré-requisitos
</h3>
<ul>
  <li>Python 3.8+</li>
  <li>Pip</li>
  <li>Git</li>
</ul>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🔧 Configuração
</h3>
<h4>Clonar repositório</h4>
<pre><code>git clone https://github.com/AntDavid/calculador_de_beneficios.git</code></pre>

<h4>Criar ambiente virtual</h4>
<pre><code>python -m venv venv</code></pre>

<h4>Ativar ambiente</h4>
<pre><code>Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate</code></pre>

<h4>Instalar dependências</h4>
<pre><code>pip install -r requirements.txt</code></pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
⚙️ Configuração do Ambiente
</h3>
<h4>Criar arquivo .env</h4>
<pre><code>echo "SECRET_KEY=sua_chave" > .env
echo "DATABASE_URL=sqlite:///calculadora_fake.db" >> .env
echo "DEFAULT_EMAIL_PROVIDER=gmail" >> .env
echo "GMAIL_EMAIL=seu_email@gmail.com" >> .env
echo "GMAIL_PASSWORD=sua_senha" >> .env</code></pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🚀 Execução
</h3>
<pre><code># Iniciar aplicação
python app.py

# Acessar no navegador:
http://localhost:5000</code></pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🔧 Comandos Úteis
</h3>
<ul>
  <li><code>flask db upgrade</code> - Aplica migrações do banco</li>
  <li><code>pytest tests/</code> - Executa testes</li>
  <li><code>flask run --debug</code> - Modo desenvolvimento</li>
  <li><code>deactivate</code> - Sai do ambiente virtual</li>
</ul>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
⚠️ Observações
</h3>
<ul>
  <li>Nunca compartilhe seu arquivo <code>.env</code></li>
  <li>O banco é criado automaticamente na primeira execução</li>
  <li>Para produção, use WSGI (Gunicorn/Waitress)</li>
</ul>

</div>
