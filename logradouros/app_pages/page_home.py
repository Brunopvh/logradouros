from PyQt5.QtWidgets import QWidget, QVBoxLayout
import sys
from typing import Callable
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QLineEdit,
    QStackedWidget  # Importante para a navegação
)
from soup_files import File, Directory, LibraryDocs, InputFiles

from logradouros.app_core import PageHLayout, PageVLayout, AppPage, TopBar


class WindowHome(AppPage):

    def __init__(self, parent: QWidget = None, *, name: str = None):
        super().__init__(parent, name=name)
        self.selectedFileSheet: File = None
        self.selectedOutputDir: Directory = None

    def initUI(self):
        super().initUI()

        # Botão para Seleção de Planilha
        self.containerSheet = QHBoxLayout()
        self.btn_planilha: QPushButton = QPushButton("📂 Selecionar Planilha (.xlsx, .csv, etc.)")
        self.btn_planilha.clicked.connect(self.selecionar_planilha)
        self.containerSheet.addWidget(self.btn_planilha)
        # Label Planilha
        self.lbl_planilha = QLabel("1. Nenhuma planilha selecionada.")
        self.lbl_planilha.setWordWrap(True)
        self.containerSheet.addWidget(self.lbl_planilha)

        # Botão para Seleção de Pasta (Diretório)
        self.containerDir = QHBoxLayout()
        self.btn_pasta: QPushButton = QPushButton("📁 Selecionar Pasta de Destino")
        self.btn_pasta.clicked.connect(self.selecionar_pasta)
        self.containerDir.addWidget(self.btn_pasta)
        # Label Pasta
        self.lbl_pasta = QLabel("2. Nenhuma pasta selecionada.")
        self.lbl_pasta.setWordWrap(True)
        self.containerDir.addWidget(self.lbl_pasta)

        # Botão de Avançar
        self.containerButtons = QVBoxLayout()
        self.btn_avancar: QPushButton = QPushButton("➡️ Avançar para a Próxima Etapa")
        self.btn_avancar.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px;")
        self.containerButtons.addWidget(self.btn_avancar)
        self.add_layout(self.containerSheet)
        self.add_layout(self.containerDir)
        self.add_layout(self.containerButtons)

    def check_selected_sheet(self) -> bool:
        """Verifica se os caminhos foram selecionados antes de avançar."""
        if (self.selectedFileSheet is None) or (self.selectedOutputDir is None):
            self.lbl_planilha.setText("❌ POR FAVOR, SELECIONE UMA PLANILHA E UMA PASTA ANTES DE AVANÇAR.")
            return False
        return True

    def connect_next_page(self, cmd: Callable):
        self.btn_avancar.clicked.connect(cmd)

    def selecionar_planilha(self):
        filtro = "Arquivos de Planilha (*.xlsx *.csv);;Todos os Arquivos (*)"
        caminho, _ = QFileDialog.getOpenFileName(self.parent, "Selecionar Arquivo de Planilha", "", filtro)
        if caminho:
            self.selectedFileSheet = File(caminho)
            self.lbl_planilha.setText(f"Planilha Selecionada: **{self.selectedFileSheet.basename()}**")

    def selecionar_pasta(self):
        caminho = QFileDialog.getExistingDirectory(self.parent, "Selecionar Pasta", "")
        if caminho:
            self.selectedOutputDir = Directory(caminho)
            self.lbl_pasta.setText(f"Pasta Selecionada: **{self.selectedOutputDir.basename()}**")


class PageProcessSheet(AppPage):

    def __init__(self, parent: QWidget = None, *, name: str = None):
        super().__init__(parent, name=name)

    def initUI(self):
        super().initUI()
        # Título
        self.add_widget(QLabel("## ✍️ Etapa 2: Entrada de Informações Adicionais"))

        # Rótulo e Caixa de Texto
        self.add_widget(QLabel("Digite informações para o processamento:"))
        self.txt_entrada = QLineEdit()
        self.txt_entrada.setPlaceholderText("Ex: Código de operação, nome do relatório...")
        self.add_widget(self.txt_entrada)

        # Botão Voltar e Processar em um layout horizontal
        h_layout = QHBoxLayout()
        self.btn_voltar: QPushButton = QPushButton("⬅️ Voltar")
        #self.btn_voltar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        h_layout.addWidget(self.btn_voltar)

        self.btn_processar_final: QPushButton = QPushButton("✅ PROCESSAR TUDO AGORA")
        self.btn_processar_final.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        h_layout.addWidget(self.btn_processar_final)
        self.add_layout(h_layout)

        # Rótulo de Status
        self.lbl_status = QLabel("")
        self.add_widget(self.lbl_status)

    def connect_process_action(self, cmd: Callable):
        self.btn_processar_final.clicked.connect(cmd)

    def connect_btn_back_page(self, stack: QStackedWidget):
        self.btn_voltar.clicked.connect(lambda: stack.setCurrentIndex(0))

    def get_text_box(self) -> str:
        return self.txt_entrada.text()
