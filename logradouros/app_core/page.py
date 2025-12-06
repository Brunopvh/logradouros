import sys
from typing import Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QLineEdit,
    QStackedWidget  # Importante para a navegação
)
from PyQt5.QtCore import Qt


class PageLayout(ABC):

    @abstractmethod
    def set_name(self, name: str):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class PageHLayout(QHBoxLayout):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._name = None

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


class PageVLayout(QVBoxLayout):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._name = None
        self.parent: QWidget = parent

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


class TopBar(QHBoxLayout):

    def __init__(self, top_name: str = "Página Inicial", *, parent: QWidget = None):
        super().__init__(parent)
        self.label_name = QLabel(top_name)
        # Centraliza o texto dentro do QLabel
        # Usamos Qt.AlignCenter para centralizar horizontal e verticalmente
        # (por padrão, já centraliza verticalmente, mas garante)
        self.label_name.setAlignment(Qt.AlignCenter)
        # Define o estilo do QLabel para cor e fonte
        # Este QLabel será esticado para ocupar o espaço disponível no layout.
        self.label_name.setStyleSheet("""
                    background-color: #007bff; 
                    color: white; 
                    font-size: 16pt; /* Aumenta o tamanho da fonte para melhor visualização */
                    font-weight: bold; 
                    padding: 10px;
                """)
        # Adiciona o QLabel ao layout
        self.addWidget(self.label_name)


class HomePage(PageVLayout):

    def __init__(self, parent: QWidget = None, *, name: str = '/home', ):
        super().__init__(parent)
        self.parent: QWidget = parent
        self.set_name(name)

    def set_top_bar(self, top_bar: TopBar):
        self.addLayout(top_bar)


