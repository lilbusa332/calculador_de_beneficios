<div style="font-family: Arial, sans-serif; font-size: 13px; line-height: 1.4; color: #24292e; max-width: 800px;">

<h2 style="font-size: 18px; color: #24292e; margin-top: 24px; margin-bottom: 16px; font-weight: 600; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.3em;">
Manual de Instalação
</h2>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
📋 Pré-requisitos
</h3>
<ul style="margin-left: 20px; margin-bottom: 16px;">
  <li style="margin-bottom: 4px;">Python 3.8+</li>
  <li style="margin-bottom: 4px;">Pip</li>
  <li style="margin-bottom: 4px;">Git</li>
</ul>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🔧 Configuração
</h3>
<pre style="background-color: #f6f8fa; padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.45; overflow-x: auto; margin-bottom: 16px;">
<code> Clonar repositório
git clone https://github.com/AntDavid/calculador_de_beneficios.git

### Criar ambiente virtual
python -m venv venv

### Ativar ambiente:
### Windows: venv\Scripts\activate
### Linux/Mac: source venv/bin/activate

### Instalar dependências
pip install -r requirements.txt</code>
</pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
⚙️ Configuração do Ambiente
</h3>
<pre style="background-color: #f6f8fa; padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.45; overflow-x: auto; margin-bottom: 16px;">
<code># Criar arquivo .env
echo "SECRET_KEY=sua_chave" > .env
echo "DATABASE_URL=sqlite:///calculadora_fake.db" >> .env
echo "DEFAULT_EMAIL_PROVIDER=gmail" >> .env
echo "GMAIL_EMAIL=seu_email@gmail.com" >> .env
echo "GMAIL_PASSWORD=sua_senha" >> .env</code>
</pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🚀 Execução
</h3>
<pre style="background-color: #f6f8fa; padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.45; overflow-x: auto; margin-bottom: 16px;">
<code># Iniciar aplicação
python app.py

### Acessar no navegador:
### http://localhost:5000</code>
</pre>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
🔧 Comandos Úteis
</h3>
<ul style="margin-left: 20px; margin-bottom: 16px;">
  <li style="margin-bottom: 4px;"><code style="background-color: rgba(27,31,35,0.05); padding: 2px 4px; border-radius: 3px;">flask db upgrade</code> - Aplica migrações do banco</li>
  <li style="margin-bottom: 4px;"><code style="background-color: rgba(27,31,35,0.05); padding: 2px 4px; border-radius: 3px;">pytest tests/</code> - Executa testes</li>
  <li style="margin-bottom: 4px;"><code style="background-color: rgba(27,31,35,0.05); padding: 2px 4px; border-radius: 3px;">flask run --debug</code> - Modo desenvolvimento</li>
  <li style="margin-bottom: 4px;"><code style="background-color: rgba(27,31,35,0.05); padding: 2px 4px; border-radius: 3px;">deactivate</code> - Sai do ambiente virtual</li>
</ul>

<h3 style="font-size: 16px; color: #0366d6; margin-top: 16px; margin-bottom: 8px; font-weight: 600;">
⚠️ Observações
</h3>
<ul style="margin-left: 20px; margin-bottom: 16px;">
  <li style="margin-bottom: 4px;">Nunca compartilhe seu arquivo <code style="background-color: rgba(27,31,35,0.05); padding: 2px 4px; border-radius: 3px;">.env</code></li>
  <li style="margin-bottom: 4px;">O banco é criado automaticamente na primeira execução</li>
  <li style="margin-bottom: 4px;">Para produção, use WSGI (Gunicorn/Waitress)</li>
</ul>

</div>
