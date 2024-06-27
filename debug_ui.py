from openai_llms import ask_gpt4v


code_snippet = """
from PyQt5.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QLineEdit
)

from iniciar import iniciar_proceso


class VentanaPrincipal(QMainWindow):
    def __init__(self, applicacion):
        super().__init__()

        # cambiar el titulo de la ventana
        self.setWindowTitle('Auto-Hostal Colombia')

        # cambiar el tamaño de la ventana
        self.resize(500, 200)

        # conseguir el tamaño de la pantalla y de la ventana
        pantalla_rect = applicacion.desktop().screen().rect()
        ventana_rect = self.rect()

        widget_principal = QWidget()
        plan = QVBoxLayout()
        plan.setContentsMargins(20, 20, 20, 20)
        plan.setSpacing(15)
        widget_principal.setLayout(plan)
        self.setCentralWidget(widget_principal)

        # self.barraEstado = QStatusBar()
        # self.setStatusBar(self.barraEstado)
        
        # colocar la ventana en el centro del cuadrante superior derecho
        x = pantalla_rect.width() * 0.85
        y = pantalla_rect.height() * 0.25

        x -= ventana_rect.width() / 2
        y -= ventana_rect.height() / 2

        self.move(int(pantalla_rect.width() - ventana_rect.width() - 50), int(y))

        # crear campos con valores por defecto
        ruta_hoja_plan = QVBoxLayout()
        ruta_hoja_plan.setSpacing(5)
        ruta_hoja_plan.addWidget(QLabel('Ruta de la hoja'))
        ruta_hoja = QLineEdit('/home/brandon/Projects/auto-hostal/example_guest_log.xlsx')
        ruta_hoja_plan.addWidget(ruta_hoja)
        plan.addLayout(ruta_hoja_plan)

        nombre_hoja_plan = QVBoxLayout()
        nombre_hoja_plan.setSpacing(5)
        nombre_hoja_plan.addWidget(QLabel('Nombre de la hoja'))
        nombre_hoja = QLineEdit('NuevaHoja')
        nombre_hoja_plan.addWidget(nombre_hoja)
        plan.addLayout(nombre_hoja_plan)

        # elegir las lineas de inicio y fin
        linea_plan = QHBoxLayout()

        # linea de inicio
        linea_inicio_plan = QVBoxLayout()
        linea_inicio_plan.setSpacing(5)
        linea_inicio_plan.addWidget(QLabel('Linea de inicio'))
        linea_inicio = QLineEdit('2')
        linea_inicio_plan.addWidget(linea_inicio)
        linea_plan.addLayout(linea_inicio_plan)

        # linea de fin
        linea_fin_plan = QVBoxLayout()
        linea_fin_plan.setSpacing(5)
        linea_fin_plan.addWidget(QLabel('Linea de fin'))
        linea_fin = QLineEdit()
        linea_fin.setPlaceholderText('Dejar vacío para todos')
        linea_fin_plan.addWidget(linea_fin)
        linea_plan.addLayout(linea_fin_plan)

        plan.addLayout(linea_plan)

        movimiento_y_mincit_grid = QGridLayout()
        movimiento_y_mincit_grid.setSpacing(5)

        movimiento_y_mincit_grid.addWidget(QLabel('Tipo de Movimiento'), 0, 0)
        entrada_botón = QRadioButton('Entrada')
        salida_botón = QRadioButton('Salida')
        movimiento_y_mincit_grid.addWidget(entrada_botón, 1, 0)
        movimiento_y_mincit_grid.addWidget(salida_botón, 1, 1)

        tipo_movimiento = QButtonGroup()
        tipo_movimiento.addButton(entrada_botón)
        tipo_movimiento.addButton(salida_botón)
        entrada_botón.setChecked(True)  # Set 'Entrada' as the default option

        mincit = QCheckBox()
        mincit_label = QLabel('Entregar datos)
        movimiento_y_mincit_grid.addWidget(mincit_label, 0, 2)
        movimiento_y_mincit_grid.addWidget(mincit, 1, 2)

        plan.addLayout(movimiento_y_mincit_grid)

        # TODO: También permitir que el usuario pueda presionar enter para iniciar el proceso

        # agregar un botón para iniciar el proceso
        iniciar_botón = QPushButton('Iniciar proceso')
        iniciar_botón.clicked.connect(lambda:
                iniciar_proceso(
                    ruta_hoja.text(),
                    nombre_hoja.text(),
                    linea_inicio.text(),
                    linea_fin.text(),
                    tipo_movimiento.checkedButton().text()
                )
        )
        plan.addWidget(iniciar_botón)

    # def muestra_mensaje(self, message):
    #     self.barraEstado.showMessage(message)


def create_app():
    app = QApplication([])
    app.setStyle('windows') # Opciones: 'windows', 'windowsvista', 'motif', 'cde', 'plastique', 'fusion'
    with open('style.qss') as f:
        app.setStyleSheet(f.read())

    ventana = VentanaPrincipal(app)

    ventana.show()

    app.exec_()


if __name__ == "__main__":
    create_app()
"""

system_prompt = "You are an expert software developer."
image_path = "/home/brandon/Projects/doc_analysis/data/screenshots/Bildschirmfoto vom 2024-04-02 20-46-40.png"

messages = [
    {'text': """My code is not behaving as expected. I would like an evenly spaced UI, but the "Entregar datos" label and checkbox are not aligned with the other elements. They seem to be shifted slightly to the right. Here is the code I am using:"""},
    {'code': code_snippet},
    {'text': "And here is an image of the output:"},
    {'image': image_path},
    {'text': "What should I do to fix the alignment?"}
]

result = ask_gpt4v(messages, system_prompt)

print(result)