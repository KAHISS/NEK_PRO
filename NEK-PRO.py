# libs of python ==========
from tkinter import ttk
from tkcalendar import DateEntry
# my modules ==============
from databaseConnection import Criptography
from functions import *
from interface import Interface
from autobot import SendMessage


class Aplication(
    Interface,
    FunctionsOfSchedule,
    FunctionsOfStudentInformations,
    FunctionsOfPlansInformations,
    FunctionsOfStockInformations,
    FunctionsOfCashManagement,
    FunctionsOfLogin,
    FunctionsOfConfigurations
):

    def __init__(self):
        self.lineTreeviewColor = {}
        self.lastSearch = {}
        self.dataBases = {
            'payments': DataBase('resources/Pagamento.db'),
            'informations': DataBase('resources/Informacoes.db'),
            'cash': DataBase('resources/Caixa.db'),
            'config': DataBase('resources/config.db')
        }
        self.criptography = Criptography()
        self.openColorPicker = True
        self.bot = SendMessage()
        super().__init__()
        self.login_window()

    def login_window(self):
        self.loginWindow = Tk()
        self.loginWindow.title('Login - NEK-PRO')
        width = self.loginWindow.winfo_screenwidth()
        height = self.loginWindow.winfo_screenheight()
        posx = width / 2 - 700 / 2
        posy = height / 2 - 400 / 2
        self.loginWindow.geometry('700x400+%d+%d' % (posx, posy))
        self.loginWindow.config(bg="#ffffff")
        self.loginWindow.iconphoto(False, PhotoImage(file=self.dataBases['config'].searchDatabase('SELECT * FROM Logo')[0][0]))

        # logo image ==============================
        logoImage = self.labels(
            self.loginWindow, '', 0.009, 0.01, width=0.48, height=0.98, position=CENTER, custom='custom',
            photo=self.image('assets/logoct.jpg', (288, 203))[0]
        )

        # frame of inputs =========================
        frameInputs = self.frame(self.loginWindow, 0.5, 0.005, 0.49, 0.985, border=2, radius=10)

        # name login ---------------------------
        labelLogin = self.labels(
            frameInputs, '', 0.256, 0.05, width=0.65, height=0.2, position=CENTER, size=90, color='#3b321a',
            photo=self.image('assets/login.png', (200, 100))[0]
        )

        # user name and password -----------------------------
        userName = self.entry(
            frameInputs, 0.1, 0.3, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Usuário'
        )
        userName.bind('<FocusIn>', lambda e: userName.configure(fg_color=self.colorsOfEntrys[0]))

        password = self.entry(
            frameInputs, 0.1, 0.5, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Senha', show='*'
        )

        # visibility ---------------------------------
        visibilityPasswordBtn = self.button(
            frameInputs, '', 0.76, 0.53, 0.08, 0.05, photo=self.image('assets/icon_eyeClose.png', (26, 26))[0], custom='entry',
            type_btn='buttonPhoto', background='white', hover_cursor='white', function=lambda: self.toggle_visibility(password, visibilityPasswordBtn)
        )
        password.bind('<FocusIn>', lambda e: [password.configure(fg_color=self.colorsOfEntrys[0]), visibilityPasswordBtn.configure(fg_color=self.colorsOfEntrys[0])])
        password.bind('<Return>', lambda e: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}))

        # line separator higher --------------------
        lineHigher = self.line_separator(frameInputs, 0.05, 0.65)

        # button of login and button of register ----------------------
        loginBtn = self.button(
            frameInputs, 'Iniciar sessão', 0.1, 0.72, 0.8, 0.1,
            function=lambda: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}),
        )
        closeBtn = self.button(
            frameInputs, 'Fechar', 0.1, 0.85, 0.8, 0.1,
            function=lambda: self.loginWindow.destroy()
        )
        self.loginWindow.mainloop()

    # ================================== main window configure =======================================
    def main_window(self):
        # screen configure ===================================
        self.root = Toplevel()
        self.root.title('NEK-PRO')
        self.root.state('zoomed')
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')
        self.root.configure(background="#ffffff")
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: [self.loginWindow.destroy(), self.backup_dataBaes_discret()])
        self.root.iconphoto(False, PhotoImage(file=self.dataBases['config'].searchDatabase('SELECT * FROM Logo')[0][0]))
        # event bind ============================================
        self.root.bind_all('<Control-b>', lambda e: self.backup_dataBaes())
        self.root.bind_all('<Control-l>', lambda e: self.loading_database())
        # style notebook
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 13, "bold"), foreground=self.colorsOfLabels[1])

        # style treeviews ==================================================
        self.style_treeview = ttk.Style()
        self.style_treeview.theme_use('vista')
        self.style_treeview.configure('Treeview', rowheight=25, fieldbackground='#261c20', foreground=self.colorsOfTreeviews[2], font='Arial 13')
        self.style_treeview.map('Treeview',
                                background=[('selected', '#000000')],  # Cor de fundo da seleção
                                foreground=[('selected', 'white')]
                                )
        # Cor do texto da seleção
        self.photosAndIcons = {
            'pdf': self.image('assets/icon_pdf.png', (46, 46)),
            'informações': self.image('assets/icon_informacoes.png', (46, 46)),
            'random': self.image('assets/icon_random.png', (36, 36)),
            'image': self.image('assets/icon_imagem.png', (26, 26)),
            'costumer': self.image('assets/icon_no_picture.png', (76, 76)),
            'employee': self.image('assets/icon_no_picture.png', (76, 76)),
            'product': self.image('assets/icon_product.png', (76, 76)),
            'barCode': self.image('assets/icon_barCode.png', (76, 76)),
        }
        self.mainTabview = ttk.Notebook(self.root)
        self.mainTabview.place(relx=0, rely=0.01, relwidth=1, relheight=1)

        # information ============================================================
        self.mainInformationFrame = self.main_frame_notebook(self.mainTabview, ' Cadastro & Informações ')
        self.informationsManagementTabview = self.notebook(self.mainInformationFrame)
        # costumers management ---------------------------------------------------
        self.costumersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Alunos ')
        self.frame_customers()
        # services management ---------------------------------------------------
        self.plansFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Planos ')
        self.frame_plans()
        # stock -----------------------------------------------------------------
        self.stockFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Estoque ')
        self.frame_sale_inventory_control()

        # schedule ============================================================
        self.mainScheduleFrame = self.main_frame_notebook(self.mainTabview, ' Pagamentos ')
        self.scheduleManagementTabview = self.notebook(self.mainScheduleFrame)
        # schedule management ---------------------------------------------------
        self.scheduleFrame = self.main_frame_notebook(self.scheduleManagementTabview, ' Gerenciador de pagamentos ')
        self.frame_schedule()
        # sale management ---------------------------------------------------
        self.saleFrame = self.main_frame_notebook(self.scheduleManagementTabview, ' Gerenciador de vendas ')
        self.frame_sale()

        # user management ---------------------------------------------------
        self.userFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Usuários ')
        self.frame_users()

        # cash register ============================================================
        self.mainCashRegisterFrame = self.main_frame_notebook(self.mainTabview, ' Caixa ')
        self.cashManagementTabview = self.notebook(self.mainCashRegisterFrame)
        # cash management ---------------------------------------------------
        self.cashFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciamento de caixa ')
        self.frame_cash_register_management_day()

        # configuration ============================================================
        self.configurationFrame = self.main_frame_notebook(self.mainTabview, ' Configurações ')
        self.configurationTabview = self.notebook(self.configurationFrame)
        # costumization ---------------------------------------------------
        self.costumizationFrame = self.main_frame_notebook(self.configurationTabview, ' Customização ')
        # costimizators ===============================================
        self.frameForCostumizations = self.frame(self.costumizationFrame, 0, 0.01, 0.999, 0.95)
        self.frame_costumization_buttons()
        self.frame_costumization_frames()
        self.frame_costumization_tabview()
        self.frame_costumization_treeview()
        self.frame_costumization_entrys()
        self.frame_costumization_labels()
        self.save()
        # loadings configs ---------------------------
        self.load_configs()

        # filling in lists -----------------------------------------
        self.refresh_combobox_student()
        self.refresh_combobox_plan()
        self.refresh_combobox_stock()

        # keeping window ===========================================
        self.root.mainloop()

    # =================================  schedule configuration  ======================================
    def frame_schedule(self):
        # frame inputs ==========================================
        self.frameInputsSchedule = self.frame(self.scheduleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom -------------
        labelCustom = self.labels(self.frameInputsSchedule, 'Aluno:', 0.02, 0.22, width=0.08)
        self.customScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.10, 0.22, 0.2, 0.12, type_entry='list',
            function=lambda e: self.completing_payment_informations()
        )

        # plan -------------
        labelPlan = self.labels(self.frameInputsSchedule, 'Plano:', 0.02, 0.36, width=0.15)
        self.planScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.10, 0.36, 0.2, 0.12, type_entry='list',
            function=lambda e: self.completing_payment_informations(type_complet='price')
        )

        # value -------------
        labelValue = self.labels(self.frameInputsSchedule, 'Valor:', 0.02, 0.50, width=0.15)
        self.valueScheduleEntry = self.entry(self.frameInputsSchedule, 0.10, 0.50, 0.2, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsSchedule, 'M/Pagamento:', 0.32, 0.22, width=0.15)
        self.methodPayScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.44, 0.22, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # date -------------
        labelDate = self.labels(self.frameInputsSchedule, 'Data de pagamento:', 0.32, 0.36, width=0.16)
        self.dateScheduleEntry = self.entry(self.frameInputsSchedule, 0.49, 0.36, 0.15, 0.12, type_entry='date')

        # marking ----------
        labelMarking = self.labels(self.frameInputsSchedule, 'Mensalidade:', 0.32, 0.50, width=0.12, custom='optional')
        self.markingScheduleEntry = self.entry(self.frameInputsSchedule, 0.44, 0.50, 0.2, 0.12, type_entry='date')

        # events bind of frame inputs ===========================
        self.customScheduleEntry.bind('<FocusOut>', lambda e: self.completing_payment_informations())
        self.planScheduleEntry.bind('<FocusOut>', lambda e: self.completing_payment_informations(type_complet='price'))
        self.customScheduleEntry.bind('<KeyPress>', lambda e: self.customScheduleEntry.configure(
            values=[name[1] for name in self.search_student(informations=self.searching_list(self.customScheduleEntry.get(), 29, 'nome'), save_seacrh=False, insert=False)]
        ))

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSchedule, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewSchedule = self.frame(self.scheduleFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Aluno', 'Plano', 'Valor', 'Método de Pagamento', 'Data', 'pagamento')
        self.treeviewSchedule = self.treeview(self.frameTreeviewSchedule, informationOfTable)
        self.lineTreeviewColor['payments'] = 0
        # event bind treeview ==========================================
        self.treeviewSchedule.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule))

        # save last search schedule ===================================
        self.lastSearch['payments'] = ''

        # buttons management ===========================================
        functions = {
            'register': lambda: self.register_scheduling(entryPicker()[0], self.treeviewSchedule, entryPicker()[1]),
            'search': lambda: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'order': lambda e: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'update': lambda: self.update_schedule(self.treeviewSchedule, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_schedule(self.treeviewSchedule),
            'pdf': lambda: self.create_pdf_schedule(self.treeviewSchedule),
            'informations': lambda: self.message_informations_schedule(self.treeviewSchedule)
        }
        self.orderBtnSchedule = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSchedule, functions, self.photosAndIcons, informationOfTable, type_btns='complete')

        # pick up entrys ===========================
        def entryPicker():
            entrysGet = []
            entrys = []
            for widget in self.frameInputsSchedule.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            entrysGet.append(self.orderBtnSchedule.get())
            return [entrysGet, entrys, ['', '', '', self.dateScheduleEntry.get(), '', self.orderBtnSchedule.get()]]

        # init search for day ===============================================
        self.search_schedule(self.treeviewSchedule, entryPicker()[0])

    def frame_sale(self):
        # frame inputs ==========================================
        self.frameInputsSale = self.frame(self.saleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom -------------
        labelCustom = self.labels(self.frameInputsSale, 'Cliente:', 0.02, 0.22, width=0.08)
        self.customSaleEntry = self.entry(self.frameInputsSale, 0.10, 0.22, 0.2, 0.12, type_entry='list')

        # product -------------
        labelProduct = self.labels(self.frameInputsSale, 'Produto:', 0.02, 0.36, width=0.15)
        self.productSaleEntry = self.entry(
            self.frameInputsSale, 0.10, 0.36, 0.2, 0.12, type_entry='list',
            function=lambda e: self.completing_sale_informations()
        )

        # value -------------
        labelValue = self.labels(self.frameInputsSale, 'Valor:', 0.02, 0.50, width=0.15)
        self.valueSaleEntry = self.entry(self.frameInputsSale, 0.10, 0.50, 0.2, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsSale, 'M/Pagamento:', 0.32, 0.22, width=0.15)
        self.methodPaySaleEntry = self.entry(
            self.frameInputsSale, 0.44, 0.22, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # date -------------
        labelDate = self.labels(self.frameInputsSale, 'Data de pagamento:', 0.32, 0.36, width=0.16)
        self.dateSaleEntry = self.entry(self.frameInputsSale, 0.49, 0.36, 0.15, 0.12, type_entry='date')

        # events bind of frame inputs ===========================
        self.productSaleEntry.bind('<FocusOut>', lambda e: self.completing_sale_informations())
        self.customSaleEntry.bind('<KeyPress>', lambda e: self.customScheduleEntry.configure(
            values=[name[1] for name in self.search_student(informations=self.searching_list(self.customSaleEntry.get(), 29, 'nome'), save_seacrh=False, insert=False)]
        ))

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSale, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewSale, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewSale = self.frame(self.saleFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Cliente', 'Plano', 'Valor', 'Método de Pagamento', 'Data')
        self.treeviewSale = self.treeview(self.frameTreeviewSale, informationOfTable)
        self.lineTreeviewColor['sale'] = 0
        # event bind treeview ==========================================
        self.treeviewSale.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSale))

        # save last search schedule ===================================
        self.lastSearch['sale'] = ''

        # buttons management ===========================================
        functions = {
            'register': lambda: self.register_sale(entryPicker()[0], self.treeviewSale, entryPicker()[1]),
            'search': lambda: self.search_sale(self.treeviewSale, entryPicker()[0]),
            'order': lambda e: self.search_sale(self.treeviewSale, entryPicker()[0]),
            'update': lambda: self.update_sale(self.treeviewSale, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_sale(self.treeviewSale),
            'pdf': lambda: self.create_pdf_schedule(self.treeviewSale),
            'informations': lambda: self.message_informations_schedule(self.treeviewSale)
        }
        self.orderBtnSale = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSale, functions, self.photosAndIcons, informationOfTable, type_btns='complete')

        # pick up entrys ===========================
        def entryPicker():
            entrysGet = []
            entrys = []
            for widget in self.frameInputsSale.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            entrysGet.append(self.orderBtnSale.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_sale(self.treeviewSale, entryPicker()[0])

    # =================================  informations configuration  ======================================
    def frame_customers(self):
        # frame photo ==========================================
        self.framePhotoClient = self.frame(self.costumersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelClient = self.labels(self.framePhotoClient, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['costumer'][0], position=CENTER)

        # observation --------------------
        self.observationClientEntry = self.text_box(self.costumersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsClient = self.tabview(self.costumersFrame, 0.14, 0, 0.855, 0.44, type_tab='frame')
        self.frameInputsClient.add(' Informações gerais ')
        self.frameInputsClient.add(' Saúde do aluno ')

        # name -------------
        labelName = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Nome:', 0.02, 0.03, width=0.08)
        self.nameClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.11, 0.03, 0.2, 0.13, type_entry='entry')

        # peso -------------
        labelPeso = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Peso:', 0.02, 0.17, width=0.08)
        self.pesoClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.11, 0.17, 0.2, 0.13, type_entry='entry')

        # student cpf -------------
        labelStudentCpf = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'CPF/Aluno:', 0.02, 0.31, width=0.15)
        self.studentCpfEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.13, 0.31, 0.18, 0.13, type_entry='entry')

        # student rg -------------
        labelStudentRg = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'RG/Aluno:', 0.02, 0.45, width=0.15)
        self.studentRgEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.13, 0.45, 0.18, 0.13, type_entry='entry')

        # birthday -------------
        labelBirthday = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'D/Nascimento:', 0.02, 0.59, width=0.15)
        self.birthdayEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.16, 0.59, 0.15, 0.13, type_entry='date')

        # responsible -------------
        labelResponsible = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Responsável:', 0.02, 0.73, width=0.20)
        self.responsibleEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.155, 0.73, 0.155, 0.13, type_entry='entry')

        # responsible rg (no lugar de Tel/Aluno) -------------
        labelResponsibleRg = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'RG/Responsável:', 0.33, 0.03, width=0.155)
        self.responsibleRgEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.49, 0.03, 0.14, 0.13, type_entry='entry')

        # student phone (reintroduzido) -------------
        labelStudentPhone = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Tel/Aluno:', 0.33, 0.17, width=0.15)
        self.studentPhoneEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.49, 0.17, 0.14, 0.13, type_entry='entry')

        # responsible phone -------------
        labelResponsiblePhone = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Tel/Responsável:', 0.33, 0.31, width=0.155)
        self.responsiblePhoneEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.49, 0.31, 0.14, 0.13, type_entry='entry')

        # address -----------------
        labelAddress = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Endereço:', 0.33, 0.45, width=0.16)
        self.addressClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.43, 0.45, 0.2, 0.13, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'CEP:', 0.33, 0.59, width=0.16)
        self.zipCodeClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.43, 0.59, 0.125, 0.13, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Cidade:', 0.33, 0.73, width=0.16)
        self.cityClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.43, 0.73, 0.2, 0.13, type_entry='entry')

        # state (no lugar de E-mail) -----------------
        labelState = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Estado:', 0.66, 0.03, width=0.16)
        self.stateClientEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.74, 0.03, 0.2, 0.13, type_entry='entry')

        # email (reorganizado) -----------------
        labelEmail = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'E-mail:', 0.66, 0.17, width=0.16)
        self.emailEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.74, 0.17, 0.2, 0.13, type_entry='entry')

        # school -----------------
        labelSchool = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Escola:', 0.66, 0.31, width=0.16)
        self.schoolEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.74, 0.31, 0.2, 0.13, type_entry='entry')

        # plan -----------------
        labelPlan = self.labels(self.frameInputsClient.tab(' Informações gerais '), 'Plano:', 0.66, 0.45, width=0.16)
        self.studentPlanEntry = self.entry(self.frameInputsClient.tab(' Informações gerais '), 0.74, 0.45, 0.2, 0.13, type_entry='list')

        # medication use -----------------
        labelMedicationUse = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Usa algum tipo de medicação com prescrição médica?', 0.02, 0.03, width=0.5, size=17)
        self.whichMedication = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.24, 0.14, 0.16, 0.13, type_entry='entry')
        self.medicationUse = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.02, 0.15, self.whichMedication, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.17, 0.15, width=0.07, size=17)

        # medication allergy -----------------
        labelMedicationAllergy = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Tem alergia a algum medicamento?', 0.02, 0.32, width=0.5, size=17)
        self.whichMedicationAllergy = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.24, 0.42, 0.16, 0.13, type_entry='entry')
        self.medicationAllergy = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.02, 0.44, self.whichMedicationAllergy, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.17, 0.44, width=0.07, size=17)

        # heart problem -----------------
        labelHeartProblem = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Tem algum problema cardíaco?', 0.02, 0.60, width=0.5, size=17)
        self.whichHeartProblem = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.24, 0.71, 0.16, 0.13, type_entry='entry')
        self.heartProblem = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.02, 0.72, self.whichHeartProblem, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.17, 0.72, width=0.07, size=17)

        # feel pain -----------------
        labelFeelPain = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Sente algum tipo de dor?', 0.42, 0.03, width=0.5, size=17)
        self.whichFeelPain = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.63, 0.14, 0.16, 0.13, type_entry='entry')
        self.feelPain = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.42, 0.15, self.whichFeelPain, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.56, 0.15, width=0.07, size=17)

        # broke the bone -----------------
        labelBone = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Já quebrou algum osso?', 0.42, 0.32, width=0.5, size=17)
        self.whichBone = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.63, 0.42, 0.16, 0.13, type_entry='entry')
        self.bone = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.42, 0.44, self.whichBone, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.56, 0.44, width=0.07, size=17)

        # other problem -----------------
        labelOtherProblem = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Algum outro problema não mencionado?', 0.42, 0.60, width=0.5, size=17)
        self.whichOtherProblem = self.entry(self.frameInputsClient.tab(' Saúde do aluno '), 0.63, 0.71, 0.16, 0.13, type_entry='entry')
        self.otherProblem = self.ask(self.frameInputsClient.tab(' Saúde do aluno '), 'Sim', 'Não', 0.42, 0.72, self.whichOtherProblem, 0.12, 0.1)
        which = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Qual(is)?', 0.56, 0.72, width=0.07, size=17)

        # blood type -----------------
        labelBloodType = self.labels(self.frameInputsClient.tab(' Saúde do aluno '), 'Tipo sanguíneo:', 0.82, 0.03, width=0.16)
        self.bloodTypeEntry = self.entry(
            self.frameInputsClient.tab(' Saúde do aluno '), 0.82, 0.14, 0.12, 0.13, type_entry='list',
            value=['A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsClient, '', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewStudent, False, type_insert='advanced', table='Clientes', photo='costumer'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsClient, '', 0.05, 0.875, 0.04, 0.10,
            function=lambda: self.active_monthly_payments(self.treeviewStudent),
            photo=self.image('assets/icon_cashFlow.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # message -------------
        sendMessage = self.button(
            self.frameInputsClient, '', 0.10, 0.875, 0.04, 0.10,
            function=lambda: self.send_message_payments(self.treeviewStudent),
            photo=self.image('assets/mandar.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # document -------------
        document = self.button(
            self.frameInputsClient, '', 0.15, 0.875, 0.02, 0.11,
            function=lambda: self.create_record(self.selection_treeview(self.treeviewStudent)),
            photo=self.image('assets/documento-de-texto.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        self.labelClient.bind('<Double-Button-1>', lambda e: self.pick_picture(self.labelClient, 'costumer'))
        self.studentPlanEntry.bind('<KeyPress>', lambda e: self.studentPlanEntry.configure(
            values=[name[1] for name in self.search_plan(informations=self.searching_list(self.studentPlanEntry.get(), 1, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.zipCodeClientEntry.bind(
            '<FocusOut>',
            lambda e: [
                self.request_adrees(self.zipCodeClientEntry.get(), [self.cityClientEntry, self.stateClientEntry]),
                self.treating_numbers(self.zipCodeClientEntry, type_treating=10)
            ]
        )
        self.studentPhoneEntry.bind('<FocusOut>', lambda e: self.treating_numbers(info=self.studentPhoneEntry, type_treating=9))
        self.responsiblePhoneEntry.bind('<FocusOut>', lambda e: self.treating_numbers(info=self.responsiblePhoneEntry, type_treating=9))
        self.studentCpfEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.studentCpfEntry, type_treating=10))
        self.studentRgEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.studentRgEntry, type_treating=11))
        self.responsibleRgEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.responsibleRgEntry, type_treating=11))

        # frame treeview ==================
        self.frameTreeviewStudent = self.frame(self.costumersFrame, 0.005, 0.45, 0.689, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = self.dataBases['informations'].searchDatabaseColumnName('Alunos')
        self.treeviewStudent = self.treeview(self.frameTreeviewStudent, informationOfTable)
        self.lineTreeviewColor['student'] = 0
        # event bind treeview ==========================================
        self.treeviewStudent.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewStudent, type_insert='advanced', table='Alunos', photo='costumer'))

        # save last search schedule ===================================
        self.lastSearch['student'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_student(entryPicker()[0], self.treeviewStudent),
            'search': lambda: self.search_student(self.treeviewStudent, entryPicker()[0]),
            'order': lambda e: self.search_student(self.treeviewStudent, entryPicker()[0]),
            'update': lambda: self.update_student(self.treeviewStudent, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_student(self.treeviewStudent),
            'pdf': lambda: self.create_pdf_student(self.treeviewStudent),
            'informations': lambda: self.message_informations_student(self.treeviewStudent)
        }
        self.orderBtnClient = self.tab_of_buttons(0.7, 0.48, 0.295, 0.4, self.costumersFrame, functions, self.photosAndIcons, informationOfTable[0:16])

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsClient.tab(' Informações gerais ').winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            # entrys of frameInputs =============================
            for widget in self.frameInputsClient.tab(' Saúde do aluno ').winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # string var informations ======================
            entrysGet.insert(16, self.medicationUse[0].get())
            entrys.insert(16, self.medicationUse[0])
            entrysGet.insert(18, self.medicationAllergy[0].get())
            entrys.insert(18, self.medicationAllergy[0])
            entrysGet.insert(20, self.heartProblem[0].get())
            entrys.insert(20, self.heartProblem[0])
            entrysGet.insert(22, self.feelPain[0].get())
            entrys.insert(22, self.feelPain[0])
            entrysGet.insert(24, self.bone[0].get())
            entrys.insert(24, self.bone[0])
            entrysGet.insert(26, self.otherProblem[0].get())
            entrys.insert(26, self.otherProblem[0])

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['costumer'][1].lower())

            # label photo =================================
            entrys.append(self.labelClient)

            # observations informations ====================
            entrysGet.append(self.observationClientEntry.get("1.0", "end-1c"))
            entrys.append(self.observationClientEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnClient.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_student(self.treeviewStudent, entryPicker()[0])

    def frame_plans(self):
        # frame inputs ==========================================
        self.frameInputsPlan = self.frame(self.plansFrame, 0.195, 0.01, 0.6, 0.43)

        # name --------------------
        labelname = self.labels(self.frameInputsPlan, 'Plano:', 0.07, 0.29, width=0.1)
        self.planEntry = self.entry(self.frameInputsPlan, 0.22, 0.29, 0.2, 0.12, type_entry='entry')

        # price -------------------
        labelPrice = self.labels(self.frameInputsPlan, 'Valor:', 0.07, 0.49, width=0.1)
        self.priceEntry = self.entry(self.frameInputsPlan, 0.22, 0.49, 0.2, 0.12, type_entry='entry')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsPlan, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewPlan, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewPlan = self.frame(self.plansFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Plano', 'Valor')
        self.treeviewPlan = self.treeview(self.frameTreeviewPlan, informationOfTable, max_width=369)
        self.lineTreeviewColor['plan'] = 0
        # event bind treeview ==========================================
        self.treeviewPlan.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewPlan))

        # save last search schedule ===================================
        self.lastSearch['plan'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_plan(entryPicker()[0], self.treeviewPlan, deleteInformationsInputs),
            'search': lambda: self.search_plan(self.treeviewPlan, entryPicker()[0]),
            'order': lambda e: self.search_plan(self.treeviewPlan, entryPicker()[0]),
            'update': lambda: self.update_plan(self.treeviewPlan, entryPicker()[0]),
            'delete': lambda: self.delete_plan(self.treeviewPlan),
            'pdf': lambda: self.create_pdf_plan(self.treeviewPlan),
            'informations': lambda: self.message_informations_plan(self.treeviewPlan)
        }
        self.orderBtnPlan = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsPlan, functions, self.photosAndIcons, informationOfTable)

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsPlan.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            # order =============================================
            entrysGet.append(self.orderBtnPlan.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_plan(self.treeviewPlan, entryPicker()[0])

    def frame_sale_inventory_control(self):
        # frame photo ==========================================
        self.framePhotoSaleInventoryControl = self.frame(self.stockFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelSaleProduct = self.labels(self.framePhotoSaleInventoryControl, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['product'][0], position=CENTER)

        # observation --------------------
        self.observationSaleinventoryControlEntry = self.text_box(self.stockFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsSaleInventoryControl = self.frame(self.stockFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsSaleInventoryControl, 'Nome:', 0.02, 0.12, width=0.15)
        self.nameSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.12, 0.18, 0.12, type_entry='entry')

        # brand -------------
        labelBrand = self.labels(self.frameInputsSaleInventoryControl, 'Marca:', 0.02, 0.26, width=0.15)
        self.brandSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.26, 0.18, 0.12, type_entry='entry')

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsSaleInventoryControl, 'Fornecedor:', 0.02, 0.40, width=0.12)
        self.supplierSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.40, 0.18, 0.12, type_entry='entry')

        # content -------------
        labelContent = self.labels(self.frameInputsSaleInventoryControl, 'Conteúdo:', 0.02, 0.54, width=0.15)
        self.contentSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.54, 0.18, 0.12, type_entry='entry')

        # quantity -------------
        labelQuantity = self.labels(self.frameInputsSaleInventoryControl, 'Quantidade:', 0.02, 0.68, width=0.15)
        self.QuantitySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.68, 0.18, 0.12, type_entry='entry')

        # buy -----------------
        labelBuy = self.labels(self.frameInputsSaleInventoryControl, 'V/compra:', 0.34, 0.12, width=0.16)
        self.buySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.12, 0.18, 0.12, type_entry='entry')

        # sale -----------------
        labelsale = self.labels(self.frameInputsSaleInventoryControl, 'V/venda:', 0.34, 0.26, width=0.16)
        self.saleInputsSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.26, 0.18, 0.12, type_entry='entry')

        # validity -----------------
        labelValidity = self.labels(self.frameInputsSaleInventoryControl, 'Validade:', 0.34, 0.40, width=0.16)
        self.validitySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.40, 0.18, 0.12, type_entry='date')
        self.validitySaleInventoryControlEntry.delete(0, END)

        # entry -----------------
        labelEntry = self.labels(self.frameInputsSaleInventoryControl, 'Entrada:', 0.34, 0.54, width=0.16, custom='optional')
        self.entrySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.54, 0.1794, 0.12, type_entry='date')
        self.entrySaleInventoryControlEntry.delete(0, END)

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSaleInventoryControl, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewStockControl, False, type_insert='advanced', table='Produtos', photo='productSale', data_base='informations'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of inputs ====================
        self.labelSaleProduct.bind('<Double-Button-1>', lambda e: self.pick_picture(self.labelSaleProduct, 'product'))

        # frame treeview ==================
        self.frameTreeviewSaleInventoryControl = self.frame(self.stockFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'Marca', 'Fornecedor', 'Conteúdo', 'Quantidade', 'V/compra', 'V/venda', 'Validade', 'Entrada')
        self.treeviewStockControl = self.treeview(self.frameTreeviewSaleInventoryControl, informationOfTable)
        self.lineTreeviewColor['product'] = 0
        # event bind treeview ==========================================
        self.treeviewStockControl.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewStockControl, type_insert='advanced', table='Produtos', photo='product', data_base='informations')
        )
        self.treeviewStockControl.bind(
            "<Control-s>", lambda e: self.select_finished_and_defeated(self.treeviewStockControl, 'usageStock')
        )

        # save last search schedule ===================================
        self.lastSearch['product'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_stock(entryPicker()[0], self.treeviewStockControl),
            'search': lambda: self.search_stock(self.treeviewStockControl, entryPicker()[0]),
            'order': lambda e: self.search_stock(self.treeviewStockControl, entryPicker()[0]),
            'update': lambda: self.update_stock(self.treeviewStockControl, entryPicker()[0]),
            'delete': lambda: self.delete_stock(self.treeviewStockControl),
            'pdf': lambda: self.create_pdf_stock(self.treeviewStockControl),
            'informations': lambda: self.message_informations_stock(self.treeviewStockControl)
        }
        self.orderBtnSaleIventoryControl = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSaleInventoryControl, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsSaleInventoryControl.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['product'][1])

            # label photo =================================
            entrys.append(self.labelSaleProduct)

            # observations informations ====================
            entrysGet.append(self.observationSaleinventoryControlEntry.get("1.0", "end-1c"))
            entrys.append(self.observationSaleinventoryControlEntry)

            # order =============================================
            entrysGet.append(self.orderBtnSaleIventoryControl.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewStockControl, entryPicker()[0])

    def frame_users(self):
        # frame inputs =========================================
        self.frameInputsUsers = self.frame(self.userFrame, 0.195, 0.01, 0.6, 0.43)

        # user --------------------
        labelUser = self.labels(self.frameInputsUsers, 'Usuário:', 0.07, 0.25, width=0.1)
        self.userEntry = self.entry(self.frameInputsUsers, 0.20, 0.25, 0.23, 0.12, type_entry='entry')

        # password -------------------
        labelPassword = self.labels(self.frameInputsUsers, 'Senha:', 0.07, 0.45, width=0.1)
        self.passwordEntry = self.entry(self.frameInputsUsers, 0.20, 0.45, 0.23, 0.12, type_entry='entry')

        # level -------------------
        labelLevel = self.labels(self.frameInputsUsers, 'Nivel:', 0.07, 0.65, width=0.1)
        self.levelEntry = self.entry(
            self.frameInputsUsers, 0.20, 0.65, 0.23, 0.12, type_entry='list',
            value=['ADMINISTRADOR', 'USUÁRIO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUsers, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUsers = self.frame(self.userFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Usuário', 'Senha', 'Nivel')
        self.treeviewUsers = self.treeview(self.frameTreeviewUsers, informationOfTable, max_width=380)
        self.lineTreeviewColor['users'] = 0
        # event bind treeview ==========================================
        self.treeviewUsers.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers))

        # save last search schedule ===================================
        self.lastSearch['users'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'search': lambda: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'order': lambda e: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'update': lambda: self.password_window(self.update_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_users, {'treeview': self.treeviewUsers})
        }
        self.buttons = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsUsers, functions, self.photosAndIcons, informationOfTable, treeview='no')

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUsers.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            return [entrysGet, entrys]

    # ================================== cash register configuration ===============================

    def frame_cash_register_management_day(self):

        # frame inputs ==========================================
        self.frameInputsCashMonth = self.frame(self.cashFrame, 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashMonthEntry = self.text_box(self.cashFrame, 0.005, 0.01, 0.13, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashMonth, 'T/Alunos:', 0.02, 0.08, width=0.12)
        self.customMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.08, 0.18, 0.12, type_entry='entry')

        # sales -------------
        labelSales = self.labels(self.frameInputsCashMonth, 'T/Vendas:', 0.02, 0.22, width=0.12)
        self.salesMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.22, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashMonth, 'T/Cartão:', 0.02, 0.36, width=0.15)
        self.cardMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.36, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashMonth, 'T/Dinheiro:', 0.02, 0.50, width=0.15)
        self.moneyMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.50, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashMonth, 'T/Transferência:', 0.02, 0.64, width=0.15)
        self.transferMonthEntry = self.entry(self.frameInputsCashMonth, 0.17, 0.64, 0.15, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashMonth, 'T/Nota:', 0.02, 0.78, width=0.16)
        self.noteMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.78, 0.18, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashMonth, 'T/Recebido:', 0.34, 0.08, width=0.16)
        self.receivedMonthEntry = self.entry(self.frameInputsCashMonth, 0.45, 0.08, 0.18, 0.12, type_entry='entry')

        # date -----------------
        labelDate = self.labels(self.frameInputsCashMonth, 'Data:', 0.34, 0.22, width=0.16)
        self.dateMonthEntry = self.entry(self.frameInputsCashMonth, 0.44, 0.22, 0.14, 0.12, type_entry='date', validity='yes')
        self.dateMonthEntry.delete(0, 3)

        # status -----------------
        labelStatus = self.labels(self.frameInputsCashMonth, 'Status:', 0.34, 0.36, width=0.16, custom='optional')
        self.statusMonthEntry = self.entry(
            self.frameInputsCashMonth, 0.44, 0.36, 0.2, 0.12, type_entry='list',
            value=['MÊS EM ANDAMENTO', 'MÊS FINALIZADO']
        )

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashMonth, 'Saida:', 0.34, 0.50, width=0.16, custom='optional')
        self.exitMonthEntry = self.entry(self.frameInputsCashMonth, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashMonth, 'M/Saida:', 0.34, 0.64, width=0.16, custom='optional')
        self.MetodyExitMonthEntry = self.entry(
            self.frameInputsCashMonth, 0.44, 0.64, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashMonth, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashMonth, '', 0.05, 0.875, 0.04, 0.10,
            function=lambda: self.password_window(self.pick_informations_for_cash, {'entrys': entryPicker()[1], 'date': self.dateMonthEntry.get()}),
            photo=self.image('assets/icon_cashFlow.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashMonth, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashMonth, self.lineTreeviewColor['cash']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        self.dateMonthEntry.bind('<FocusOut>', lambda e: self.dateMonthEntry.delete(0, 3))
        self.dateMonthEntry.bind("<<DateEntrySelected>>", lambda e: self.dateMonthEntry.delete(0, 3))

        # frame treeview ==================
        self.frameTreeviewCashMonth = self.frame(self.cashFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'T/Alunos', 'T/Vendas', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'T/Recebido', 'mês', 'Status')
        self.treeviewCashMonth = self.treeview(self.frameTreeviewCashMonth, informationOfTable)
        self.lineTreeviewColor['cash'] = 0
        # event bind treeview ==========================================
        self.treeviewCashMonth.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, type_insert='advanced', table='Gerenciamento_do_mês', data_base='cash')
        )
        # save last search schedule ===================================
        self.lastSearch['cash'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashMonth,
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],

                }
            ),
            'update': lambda: self.password_window(
                self.update_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                }
            ),
        }
        self.orderBtnDay = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashMonth, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashMonth.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashMonthEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashMonthEntry)

            # order =============================================
            entrysGet.append(self.orderBtnDay.get())
            return [entrysGet, entrys]

        # init search =============================
        self.search_cashManagement(
            self.treeviewCashMonth,
            self.searching_list('', 11, 'ID'),
            insert=False
        )

    # ================================== cash register configuration ===============================

    def frame_costumization_buttons(self):
        # buttons -------------------------
        self.frameForButtons = self.frame(self.frameForCostumizations, 0.02, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Botões')
        # -> background
        background = self.labels(self.frameForButtons, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForButtons, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForButtons, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForButtons, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForButtons, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForButtons, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForButtons, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForButtons, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForButtons, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> hover color
        hoverColor = self.labels(self.frameForButtons, 'Cor do hover:', 0.03, 0.54, 0.5, 0.1, size=13)
        colorHvEntry = self.entry(self.frameForButtons, 0.4, 0.54, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerHv = self.button(
            self.frameForButtons, '', 0.7, 0.51, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'hover_color', colorHvEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'border_color', colorBdEntry, color_picker='no'))
        colorHvEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'hover_color', colorHvEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForButtons, 0.03, 0.67)

        # demonstrative button ---------------------
        Btn = self.button(self.frameForButtons, 'Texto', 0.18, 0.78, 0.6, 0.2)

    def frame_costumization_frames(self):
        # buttons -------------------------
        self.frameForFrames = self.frame(self.frameForCostumizations, 0.02, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Frames')

        # -> background
        background = self.labels(self.frameForFrames, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForFrames, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForFrames, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForFrames, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForFrames, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForFrames, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForFrames, 0.03, 0.35)

        # demonstrative frame ---------------------
        frame = self.frame(self.frameForFrames, 0.14, 0.475, 0.67, 0.5)

    def frame_costumization_tabview(self):
        # buttons -------------------------
        self.frameForTabview = self.frame(self.frameForCostumizations, 0.38, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Tabview')

        # -> background
        background = self.labels(self.frameForTabview, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForTabview, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTabview, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForTabview, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForTabview, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTabview, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'border_color', colorBdEntry, color_picker='no'))

        # demonstrative tabview ---------------------
        tabview = self.tabview(self.frameForTabview, 0.14, 0.4, 0.67, 0.55)

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForTabview, 0.03, 0.35)

    def frame_costumization_treeview(self):
        # buttons -------------------------
        self.frameForTreeview = self.frame(self.frameForCostumizations, 0.38, 0.35, 0.2, 0.4, border_color='#d2d2d2', type_frame='labelFrame', text='Tabela')

        # -> line1
        line1 = self.labels(self.frameForTreeview, 'Cor da linha 1:', 0.03, 0.03, 0.5, 0.06, size=13)
        colorL1Entry = self.entry(self.frameForTreeview, 0.4, 0.027, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTreeview, '', 0.7, 0.001, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag1', colorL1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> line2
        line2 = self.labels(self.frameForTreeview, 'Cor da linha 2:', 0.03, 0.15, 0.5, 0.06, size=13)
        colorL2Entry = self.entry(self.frameForTreeview, 0.4, 0.15, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTreeview, '', 0.7, 0.12, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag2', colorL2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> text color
        textColor = self.labels(self.frameForTreeview, 'Cor de texto:', 0.03, 0.27, 0.5, 0.06, size=13)
        colorFgEntry = self.entry(self.frameForTreeview, 0.4, 0.27, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForTreeview, '', 0.7, 0.24, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorL1Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag1', colorL1Entry, color_picker='no'))
        colorL2Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag2', colorL2Entry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry, color_picker='no'))

        # demonstrative treeview ---------------------
        frameTreeview = self.frame(self.frameForTreeview, 0.02, 0.4, 0.97, 0.5, border_color='#d2d2d2')
        treeview = self.treeview(frameTreeview, ['informação 1'])
        self.lineTreeviewColor['demonstrative'] = 0
        self.insert_treeview_informations(treeview, ['Linha 1', 'linha2'], 'demonstrative')

    def frame_costumization_entrys(self):
        # buttons -------------------------
        self.frameForEntrys = self.frame(self.frameForCostumizations, 0.77, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Entradas de texto')
        # -> background
        background = self.labels(self.frameForEntrys, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForEntrys, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForEntrys, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForEntrys, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForEntrys, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForEntrys, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForEntrys, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForEntrys, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForEntrys, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForEntrys, 0.03, 0.54)

        # demonstrative button ---------------------
        entry = self.entry(self.frameForEntrys, 0.18, 0.70, 0.6, 0.2, type_entry='entry')
        entry.insert(0, 'Texto')

    def frame_costumization_labels(self):
        # buttons -------------------------
        self.frameForLabels = self.frame(self.frameForCostumizations, 0.77, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Textos')

        # -> text color
        text1 = self.labels(self.frameForLabels, 'Cor de texto 1:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorFg1Entry = self.entry(self.frameForLabels, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg1 = self.button(
            self.frameForLabels, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(text1, 'text_color', colorFg1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        text2 = self.labels(self.frameForLabels, 'Cor de texto 2:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFg2Entry = self.entry(self.frameForLabels, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg2 = self.button(
            self.frameForLabels, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(text2, 'text_color', colorFg2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorFg1Entry.bind('<Return>', lambda e: self.colorPicker(text1, 'text_color', colorFg1Entry, color_picker='no'))
        colorFg2Entry.bind('<Return>', lambda e: self.colorPicker(text2, 'text_color', colorFg2Entry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForLabels, 0.03, 0.35)

        # demonstrative labels ---------------------
        text1 = self.labels(self.frameForLabels, 'Texto 1', 0.33, 0.5, 0.3, 0.2)
        text2 = self.labels(self.frameForLabels, 'Texto 2', 0.33, 0.75, 0.3, 0.2, custom='optional')

    def save(self):
        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForCostumizations, 0.02, 0.8, width=0.95)

        # demonstrative labels ---------------------
        text1 = self.button(self.frameForCostumizations, 'Salvar', 0.75, 0.86, 0.2, 0.1, function=lambda: self.save_configs())


if __name__ == '__main__':
    app = Aplication()
