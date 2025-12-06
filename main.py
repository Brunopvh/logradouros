import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QLineEdit,
    QStackedWidget  # Importante para a navegação
)

import os

_script = os.path.abspath(os.path.realpath(__file__))
dir_root = os.path.dirname(_script)
sys.path.insert(0, dir_root)
from logradouros.app_core.page import PageVLayout, TopBar
from logradouros.app_pages.page_home import WindowHome, PageProcessSheet


class PlanilhaProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processador de Planilhas")
        self.setGeometry(100, 100, 700, 300)

        # Variáveis para armazenar os caminhos e o texto de entrada
        self.info_digitada = ""

        # Inicializa o QStackedWidget para gerenciar as páginas
        self.stacked_widget = QStackedWidget(self)
        self.init_ui()

    def init_ui(self):
        main_layout: PageVLayout = PageVLayout(self)
        main_layout.addWidget(self.stacked_widget)

        # 1. Cria e adiciona a Página de Seleção (Índice 0)
        self.widgetPage1 = QWidget()
        self.page_home = WindowHome(self.widgetPage1, name='/home')
        self.setup_page1()

        # Cria e adiciona a Página de Entrada de Dados (Índice 1)
        self.page2 = QWidget()
        self.page_process_sheet = PageProcessSheet(self.page2, name='/process_sheet')
        self.setup_page2()
        self.setLayout(main_layout)

    ## --- Configuração da Página 1: Seleção de Arquivos ---
    def setup_page1(self):
        self.page_home.set_top_bar(TopBar())
        self.page_home.initUI()
        self.page_home.connect_next_page(self.go_to_page2)
        self.stacked_widget.addWidget(self.widgetPage1)

    def setup_page2(self):
        self.page_process_sheet.set_top_bar(TopBar("Processamento"))
        self.page_process_sheet.initUI()
        self.page_process_sheet.connect_btn_back_page(self.stacked_widget)
        self.page_process_sheet.connect_process_action(self.processar_operacao_final)
        self.stacked_widget.addWidget(self.page2)

    def go_to_page2(self):
        """Verifica se os caminhos foram selecionados antes de avançar."""
        if not self.page_home.check_selected_sheet():
            return
        # Muda para o índice 1 (a segunda página)
        self.stacked_widget.setCurrentIndex(1)
        print("--- Avançou para a Página 2 (Entrada de Dados) ---")

    def processar_operacao_final(self):
        """Função chamada ao clicar no botão Processar na Etapa 2."""
        self.info_digitada = self.page_process_sheet.get_text_box()

        # Verifica se o campo de texto foi preenchido (opcional, dependendo da sua regra)
        if not self.info_digitada.strip():
            self.page_process_sheet.lbl_status.setText("❌ Por favor, digite alguma informação no campo de texto.")
            return

        self.caminho_planilha = self.page_home.selectedFileSheet.absolute()
        self.caminho_pasta = self.page_home.selectedOutputDir.absolute()
        # --- Lógica de Processamento Final Aqui ---
        print("\n--- INICIANDO PROCESSAMENTO FINAL ---")
        print(f"Planilha: {self.caminho_planilha}")
        print(f"Pasta: {self.caminho_pasta}")
        print(f"Info Adicional: {self.info_digitada}")

        self.page_process_sheet.lbl_status.setText("⚙️ Processamento em andamento...")
        self.page_process_sheet.lbl_status.setText("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlanilhaProcessorApp()
    ex.show()
    sys.exit(app.exec_())