from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Calculadora de Benefícios - Fingindo que sei o que tô fazendo', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(user, valor_beneficio, output_path, renda, dependentes, tipo_beneficio, data_calculo):
    pdf = PDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Comprovante de Cálculo de Benefício', 0, 1, 'C')
    pdf.ln(10)
    
    # Informações do Cidadão
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Informações do Cidadão', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    info_cidadao = [
        ('Nome:', user.nome),
        ('CPF:', user.cpf),
        ('Data de Nascimento:', user.data_nascimento),
        ('Endereço:', f"{user.endereco}, {user.cidade}/{user.estado}"),
        ('CEP:', user.cep),
        ('Telefone:', user.telefone)
    ]
    
    for label, value in info_cidadao:
        pdf.cell(40, 8, label, 0, 0)
        pdf.cell(0, 8, value, 0, 1)
    
    pdf.ln(10)
    
    # Detalhes do Cálculo
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detalhes do Cálculo', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    tipo_map = {
        'bolsa_familia': 'Bolsa Família',
        'auxilio_emergencial': 'Auxílio Emergencial',
        'outros': 'Outros Benefícios'
    }
    
    calc_info = [
        ('Data do Cálculo:', data_calculo.strftime('%d/%m/%Y %H:%M')),
        ('Tipo de Benefício:', tipo_map.get(tipo_beneficio, tipo_beneficio)),
        ('Renda Mensal:', f"R$ {renda:,.2f}"),
        ('Dependentes:', str(dependentes))
    ]
    
    for label, value in calc_info:
        pdf.cell(60, 8, label, 0, 0)
        pdf.cell(0, 8, value, 0, 1)
    
    pdf.ln(10)
    
    # Resultado
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Resultado do Cálculo', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f"Valor do Benefício: R$ {valor_beneficio:,.2f}", 0, 1, 'C')
    
    # Observações
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 8)
    pdf.multi_cell(0, 5, 'Este documento não substitui a análise oficial do Ministério da Cidadania. '
                         'O valor final pode sofrer ajustes conforme a legislação vigente.')
    
    pdf.output(output_path)