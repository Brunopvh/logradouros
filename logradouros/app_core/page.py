from __future__ import annotations

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


class AppPage(object):

    def __init__(self, parent: QWidget = None, *, name: str = None, ):
        super().__init__()
        self.parent: QWidget = parent
        self._main_layout: QVBoxLayout = None
        self.__name: str = name
        self.isLayout: bool = False
        self.isTopBar: bool = False

    def initUI(self):
        if self._main_layout is None:
            self._main_layout: QVBoxLayout = QVBoxLayout()
        if not self.isLayout:
            self.parent.setLayout(self._main_layout)
            self.isLayout = False

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def add_layout(self, layout: QVBoxLayout | QHBoxLayout):
        self._main_layout.addLayout(layout)

    def add_widget(self, widget: QWidget):
        self._main_layout.addWidget(widget)

    def set_top_bar(self, top_bar: TopBar):
        if self.isTopBar:
            return
        if self._main_layout is None:
            self._main_layout: QVBoxLayout = QVBoxLayout()
        self._main_layout.addLayout(top_bar)
        self.isTopBar = True
        if not self.isLayout:
            self.parent.setLayout(self._main_layout)
            self.isLayout = True


