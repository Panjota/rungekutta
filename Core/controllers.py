import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QWidget, QLabel
from Core.functions import *
from Core import helpers
from Views.calculo import Ui_calculo
from Views.mainwindow import Ui_MainWindow
from Views.sobre import Ui_sobre
from Views.tabela import Ui_tabela


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=None)
        self.setupUi(self)
        # self.setWindowIcon(QIcon('icons/k.png'))
        self.actionCalculo.triggered.connect(self.clickCalculo)
        self.actionTabela.triggered.connect(self.clickTabela)
        self.actionGrafico.triggered.connect(self.clickGrafico)
        self.actionSobre.triggered.connect(self.clickSobre)
        self.clickSobre()

    def clickCalculo(self):
        helpers.clear_layout(self.body.layout())
        form = WidgetCalculo(parent=self)
        self.body.layout().addWidget(form)

    def clickTabela(self):
        helpers.clear_layout(self.body.layout())
        form = WidgetTabela(parent=self)
        self.body.layout().addWidget(form)

    def clickGrafico(self):
        helpers.clear_layout(self.body.layout())
        form = WidgetGrafico(parent=self)
        self.body.layout().addWidget(form)

    def clickSobre(self):
        helpers.clear_layout(self.body.layout())
        form = WidgetSobre(parent=self)
        self.body.layout().addWidget(form)


class WidgetCalculo(QWidget, Ui_calculo):
    def __init__(self, parent=None):
        super(WidgetCalculo, self).__init__(parent=parent)
        self.setupUi(self)
        self.buttonCalcular.clicked.connect(self.calculo)
        self.buttonLimpar.clicked.connect(self.limpar)

    def calculo(self):
        f = lambda x, y: eval(expression)

        expression = self.lineEquacao.text()
        xinicial = float(self.lineX.text())
        yinicial = float(self.lineY.text())
        passo = float(self.linePasso.text())
        repeticao = int(self.lineRepeticao.text())

        x_values, y_values = runge_kutta(f, xinicial, yinicial, passo, repeticao)
        results = [f"x: {x_values[i]:.3}, y: {y_values[i]}\n" for i in range(len(x_values))]

        plt.plot(x_values, y_values, marker='o')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Gráfico da função usando o Método Runge-Kutta')
        plt.grid(True)
        plt.savefig('grafico.jpg')

        # Nome do arquivo de saída
        output_file_name = "resultados.txt"

        # Escrever os resultados no arquivo
        with open(output_file_name, 'w') as output_file:
            output_file.writelines(results)

        self.limpar()

    def limpar(self):
        self.lineEquacao.clear()
        self.lineY.clear()
        self.lineX.clear()
        self.linePasso.clear()
        self.lineRepeticao.clear()


class WidgetTabela(QWidget, Ui_tabela):
    def __init__(self, parent=None):
        super(WidgetTabela, self).__init__(parent=parent)
        self.setupUi(self)
        self.preencherTabela()

    def preencherTabela(self):
        try:
            # Ler os valores de x e y a partir do arquivo "resultados.txt"
            with open("resultados.txt", 'r') as file:
                lines = file.readlines()
                x_values = []
                y_values = []
                for line in lines:
                    parts = line.strip().split(", ")
                    x_values.append(float(parts[0].split(": ")[1]))
                    y_values.append(float(parts[1].split(": ")[1]))

            # Configurar o número de linhas na tabela
            self.tableWidget.setRowCount(len(x_values))

            # Preencher a tabela com os valores de x e y
            for index, x in enumerate(x_values):
                X = QTableWidgetItem()
                X.setText(str(x))
                self.tableWidget.setItem(index, 0, X)
                self.tableWidget.resizeColumnToContents(0)

            for index, y in enumerate(y_values):
                Y = QTableWidgetItem()
                Y.setText(str(y))
                self.tableWidget.setItem(index, 1, Y)
                self.tableWidget.resizeColumnToContents(1)

        except FileNotFoundError:
            print("Arquivo 'resultados.txt' não encontrado.")
            # Você pode optar por exibir uma mensagem na interface gráfica também
        except Exception as e:
            print(f"Erro ao preencher a tabela: {e}")
            # Lidar com outros erros de leitura ou parsing do arquivo


class WidgetGrafico(QWidget, Ui_tabela):
    def __init__(self, parent=None):
        super(WidgetGrafico, self).__init__(parent=parent)
        self.setupUi(self)
        self.mostrarGrafico()

    def mostrarGrafico(self):
        # Criar um QLabel para exibir a imagem
        label = QLabel(self)

        # Carregar a imagem grafico.jpg usando QPixmap
        pixmap = QPixmap("grafico.jpg")

        if not pixmap.isNull():  # Verificar se a imagem foi carregada com sucesso
            label.setPixmap(pixmap)
            label.setScaledContents(True)  # Redimensionar a imagem para o tamanho do QLabel
            label.setGeometry(0, 0, self.width(), self.height())  # Define a geometria do QLabel
            label.show()
        else:
            print("Não foi possível carregar a imagem grafico.jpg")


class WidgetSobre(QWidget, Ui_sobre):
    def __init__(self, parent=None):
        super(WidgetSobre, self).__init__(parent=parent)
        self.setupUi(self)
