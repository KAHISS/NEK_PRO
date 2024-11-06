from databaseConnection import DataBase

config = DataBase('resources/config.db')
header = config.searchDatabase('SELECT * FROM Botões')[0]

# sql comands general==========================================
searchAll = 'SELECT * FROM {}'
deleteInformation = 'DELETE FROM {} WHERE ID = {}'

# style of tables general ===============================================
styleTableInformationsTreeview = [
    ('BACKGROUND', (0, 1), (-1, 1), f'{header[0]}'),
    ('BACKGROUND', (0, 2), (-1, -1), f'#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, 1), f'{header[1]}'),
    ('TEXTCOLOR', (0, 2), (-1, -1), f'#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#000000'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#000000')
]
styleTableInformationsComplementary = [
    ('BACKGROUND', (0, 1), (-1, 1), f'{header[2]}'),
    ('BACKGROUND', (0, 2), (-1, -1), f'#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, 1), f'{header[1]}'),
    ('TEXTCOLOR', (0, 2), (-1, -1), f'#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#000000'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#000000')]

# sql comands for scheduling ===================================
registerScheduling = (
    'INSERT INTO Pagamentos (aluno,  plano, valor, método_de_pagamento, data, pagamento)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'
)
searchSchedule = '''SELECT * 
                  FROM Pagamentos
                  WHERE {} LIKE "%{}%"
                  and valor LIKE "%{}%"
                  and plano LIKE "%{}%"
                  and método_de_pagamento LIKE "%{}%"
                  and data LIKE "%{}%"
                  and pagamento LIKE "%{}%" ORDER BY {} ASC'''

updateSchedule = '''UPDATE Pagamentos
                      SET aluno = "{}",
                          plano = "{}",
                          valor = "{}",
                          método_de_pagamento = "{}",         
                          data = "{}",
                          pagamento = "{}"
                      WHERE ID = {}'''

# tables for schedule informations =================================
tableWithInformationsScheduleTreeview = [['', '', '', '', '', ''], ['    ID    ', '    Aluno    ', '    valor    ', ' Plano ', '    M/Pagamento   ', '    data    ', '    pagamento    ']]
tableWithInformationsComplementarySchedule = [['', '', '', '', '', '', ''], ['Total de Alunos', 'T/Cartão', 'T/Dinheiro', 'T/Tranferência', 'T/Nota', 'T/Não pago', 'T/Recebido']]

# sql comands for clients informations ==============================
registerStudent = (
    'INSERT INTO Alunos ('
    'nome,'
    'cpf_aluno,'
    'rg_aluno,'
    'data_de_nascimento,'
    'responsável,'
    'rg_responsável,'
    'tel_aluno,'
    'tel_responsável,'
    'endereço,'
    'cep,'
    'cidade,'
    'estado,'
    'email,'
    'escola,'
    'plano,'
    'uso_de_medicação,'
    'qual_medicação,'
    'alergia_a_medicamento,'
    'qual_alergia,'
    'problema_cardíaco,'
    'qual_problema,'
    'dores,'
    'qual_dor,'
    'quebrou_osso,'
    'qual_osso,'
    'outro_problema,'
    'qual_outro,'
    'tipo_sanguíneo,'
    'foto,'
    'observação'
    ')'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchStudent = '''SELECT * 
                  FROM Alunos
                  WHERE {} LIKE "%{}%"
                  and cpf_aluno LIKE "%{}%"
                  and rg_aluno LIKE "%{}%"
                  and data_de_nascimento LIKE "%{}%"
                  and responsável LIKE "%{}%"
                  and rg_responsável LIKE "%{}%"
                  and tel_aluno LIKE "%{}%"
                  and tel_responsável LIKE "%{}%"
                  and endereço LIKE "%{}%"
                  and cep LIKE "%{}%"
                  and cidade LIKE "%{}%"
                  and estado LIKE "%{}%"
                  and email LIKE "%{}%"
                  and escola LIKE "%{}%"
                  and plano LIKE "%{}%"
                  and uso_de_medicação LIKE "%{}%"
                  and qual_medicação LIKE "%{}%"
                  and alergia_a_medicamento LIKE "%{}%"
                  and qual_alergia LIKE "%{}%"
                  and problema_cardíaco LIKE "%{}%" 
                  and qual_problema LIKE "%{}%" 
                  and dores LIKE "%{}%" 
                  and qual_dor LIKE "%{}%"
                  and quebrou_osso LIKE "%{}%" 
                  and qual_osso LIKE "%{}%" 
                  and outro_problema LIKE "%{}%" 
                  and qual_outro LIKE "%{}%" 
                  and tipo_sanguíneo LIKE "%{}%" ORDER BY {} ASC'''

updateStudent = '''UPDATE Alunos
                      SET nome = "{}",
                          cpf_aluno = "{}",
                          rg_aluno = "{}",
                          data_de_nascimento = "{}",
                          responsável = "{}",
                          rg_responsável = "{}",
                          tel_aluno = "{}",
                          tel_responsável = "{}",
                          endereço = "{}",
                          cep = "{}",
                          cidade = "{}",
                          estado = "{}",
                          email = "{}",
                          escola = "{}",
                          plano = "{}",
                          uso_de_medicação = "{}",
                          qual_medicação = "{}",
                          alergia_a_medicamento = "{}",
                          qual_alergia = "{}",
                          problema_cardíaco = "{}",
                          qual_problema = "{}",
                          dores = "{}",
                          qual_dor = "{}",
                          quebrou_osso = "{}",
                          qual_osso = "{}",
                          outro_problema = "{}",
                          qual_outro = "{}",
                          tipo_sanguíneo = "{}",
                          foto = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsStudentTreeview = [['', '', '', '', '', ''], ['    ID    ', ' Nome ', ' CEP ', '  Cidade  ', ' Estado ', ' Plano ']]
tableWithInformationsComplementaryStudent = [['', '', '', '', ''], ['Total de Alunos', 'Maiores de idade', 'Menores de idade', 'Mais velho', 'Mais novo']]

# sql comands for plans informations ==============================
registerPlans = (
    'INSERT INTO Planos (plano, valor)'
    'VALUES ("{}", "{}")'
)
searchPlans = '''SELECT * 
                  FROM Planos
                  WHERE {} LIKE "%{}%"
                  and valor LIKE "%{}%" ORDER BY {} ASC'''

updatePlan = '''UPDATE Planos
                      SET plano = "{}",
                          valor = "{}"
                      WHERE ID = {}'''

# tables for plam informations =================================
tableWithInformationsPlanTreeview = [['', '', ''], ['    ID    ', '    Nome    ', 'Valor']]
tableWithInformationsComplementaryPlan = [[''], ['Total de planos']]

# sql comands for cash ==============================
registerCashManagement = (
    'INSERT INTO Gerenciamento_do_mês (t_alunos, t_vendas, t_cartão, t_dinheiro, t_transferência, t_nota, s_cartão, s_dinheiro, s_transferência, s_nota, t_recebido, mês, status, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchCashManagement = '''SELECT *
                  FROM Gerenciamento_do_mês
                  WHERE t_alunos LIKE "%{}%"
                  and t_vendas LIKE "%{}%"
                  and t_cartão LIKE "%{}%"
                  and t_dinheiro LIKE "%{}%"
                  and t_transferência LIKE "%{}%"
                  and t_nota LIKE "%{}%"
                  and {} LIKE "%{}%"
                  and t_recebido LIKE "%{}%"
                  and mês LIKE "%{}%"
                  and status LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateCashManagement = '''UPDATE Gerenciamento_do_mês
                      SET t_alunos = "{}",
                          t_vendas = "{}",
                          t_cartão = "{}",
                          t_dinheiro = "{}",
                          t_transferência = "{}",
                          t_nota = "{}",
                          {} = "{}",
                          t_recebido = "{}",
                          mês = "{}",
                          status = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsCashManagementTreeview1 = [['', '', '', '', '', '', ''], ['ID', 'T/Alunos', 'T/Vendas', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/Nota']]
tableWithInformationsCashManagementTreeview2 = [['', '', '', '', '', '', ''], ['S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'T/Recebido', 'mês', 'Status']]
tableWithInformationsComplementaryCashManagement = [['', '', '', ''], ['T/Clientes', 'T/Vendas', 'T/Recebido', 'T/Saída']]
# message informations cash day ===============================
messageCashManagement = ('Total de Alunos = {}\n'
                         'Total de Vendas = {}\n'
                         'Total recebido = {}\n'
                         'Total de Saida = {}')

# sql comands for sale stock ==============================
registerStock = (
    'INSERT INTO Produtos (nome, marca, fornecedor, conteúdo, quantidade_em_estoque, valor_de_compra, valor_de_venda, validade, entrada, foto, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchStock = '''SELECT *
                  FROM Produtos
                  WHERE nome LIKE "%{}%"
                  and marca LIKE "%{}%"
                  and fornecedor LIKE "%{}%"
                  and conteúdo LIKE "%{}%"
                  and quantidade_em_estoque LIKE "%{}%"
                  and valor_de_compra LIKE "%{}%"
                  and valor_de_venda LIKE "%{}%"
                  and validade LIKE "%{}%"
                  and entrada LIKE "%{}%" ORDER BY {} ASC'''

updateStock = '''UPDATE Produtos
                      SET nome = "{}",
                          marca = "{}",
                          fornecedor = "{}",
                          conteúdo = "{}",
                          quantidade_em_estoque = "{}",
                          valor_de_compra = "{}",
                          valor_de_venda = "{}",
                          validade = "{}",
                          entrada = "{}",        
                          foto = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsStockTreeview1 = [['', '', '', '', '', ''], ['ID', 'Nome', 'Marca', 'Fornecedor', 'Conteudo', 'Quantidade']]
tableWithInformationsStockTreeview2 = [['', '', '', ''], ['V/compra', 'V/Venda', 'Validade', 'Entrada']]
tableWithInformationsComplementaryStock = [['', '', ''], ['Produtos', 'Vt/Compra', 'Vt/Venda', 'Vencidos']]
messageStock = ('Total de produtos = {}\n'
                'Valor total de compra = {}\n'
                'Valor total de venda  = {}\n'
                'Vencidos = {}')
# sql comands for sale stock ==============================
registerSale = (
    'INSERT INTO Vendas (cliente, produto, valor, método_de_pagamento, data)'
    'VALUES ("{}", "{}", "{}", "{}", "{}")'
)
searchSale = '''SELECT *
                  FROM Vendas
                  WHERE {} LIKE "%{}%"
                  and produto LIKE "%{}%"
                  and valor LIKE "%{}%"
                  and método_de_pagamento LIKE "%{}%"
                  and data LIKE "%{}%" ORDER BY {} ASC'''

updateSale = '''UPDATE Vendas
                      SET cliente = "{}",
                          produto = "{}",
                          valor = "{}",
                          método_de_pagamento = "{}",
                          data = "{}"
                      WHERE ID = {}'''

# tables for schedule informations =================================
tableWithInformationsSaleTreeview = [['', '', '', '', ''], ['    ID    ', '    Cliente    ', '    valor    ', ' Plano ', '    M/Pagamento   ', '    data    ']]
tableWithInformationsComplementarySale = [['', '', '', '', '', '', ''], ['Total de Alunos', 'T/Cartão', 'T/Dinheiro', 'T/Tranferência', 'T/Nota', 'T/Não pago', 'T/Recebido']]
messageSale = ('Total de produtos = {}\n'
               'Valor total de compra = {}\n'
               'Valor total de venda  = {}\n'
               'Vencidos = {}')
# sql comands for users ==============================
registerUsers = (
    'INSERT INTO Usuários (nome, senha, nivel)'
    'VALUES ("{}", "{}", "{}")'
)
searchUsers = '''SELECT *
                  FROM Usuários
                  WHERE nome LIKE "%{}%"
                  and nivel LIKE "%{}%"'''
updateUsers = '''UPDATE Usuários
                      SET nome = "{}",
                          senha = "{}",
                          nivel = "{}"
                      WHERE ID = {}'''

date_pattern = r'\b\d{2}[/-]\d{4}\b'

# set references for replacement
references = {
    'nnn': '',  # Nome
    'ccc': '',  # cpf
    'rgrgrg': '',  # rg
    'ddd': '',  # data de nascimento
    'rerere': '',  # responsável
    'rrr': '',  # rg responsável
    'tatata': '',  # tel aluno
    'trtrtr': '',  # tel responsável
    'eee': '',  # endereço
    'cecece': '',  # cep
    'cicici': '',  # cidade
    'eseses': '',  # estado
    'ememem': '',  # email
    'escesc': '',  # escola
    'ppp': '',  # plano
    'pmpmpm': '',
    'q1': '',
    'amamam': '',
    'q2': '',
    'pcpcpc': '',
    'q3': '',
    'sdsdsd': '',
    'q4': '',
    'jojojo': '',
    'q5': '',
    'lclclc': '',
    'q6': '',
    'sss': ''
}

messageForCharge = ('{} {}, tudo bem? vi aqui que sua mensalidade ainda está pendente. Por gentileza poderia efetuar o pagamento para mim? Você pode fazer o pagamento lá na academia ou efetuar no pix abaixo:\n\n'
                    '📛 Nome: Diego Lima de Melo\n'
                    '🔑 Chave pix: 77998610490\n\n'
                    '📅 Mensalidade: {}\n'
                    '🥊 Seu plano: {}\n'
                    '💰 Valor: {}\n\n'
                    'Desde já agradeço 👊👊👊')
