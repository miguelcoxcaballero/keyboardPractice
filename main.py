import sys
import random
import time
import statistics
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLineEdit
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer

# Configuración de la longitud promedio de una palabra
AVERAGE_WORD_LENGTH = 5

# Lista de caracteres
char_list = [
    # Letras
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z',
    # Letras especiales en español
    'á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ',
    # Puntuación y símbolos
    ',', '.', '-', '_', '\'', '"', '¡', '¿', '!', '?', ';', ':',
    '(', ')', '/', '\\', '@', '#', '$', '%', '&', '=', '*', '+',
    '<', '>', '|', '~', '{', '}', '[', ']', 'º', 'ª', '·', '¬', '€',
    # Números
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    # Caracteres que requieren doble pulsación
    '^', '`', '¨', '´', '~',
]

# Aumentar la frecuencia de caracteres de programación
programming_chars = [
    '\\', '{', '}', '[', ']', '!', ';', ':', '<', '>', '=', '+', '-', '*', '/',
    '%', '&', '|', '~', '$', '_', '.', '?', ':'
]
char_list.extend(programming_chars * 5)  # Aumentar frecuencia

# Eliminar duplicados
char_list = list(set(char_list))

# Mapa de caracteres que requieren doble pulsación
double_press_chars = ['^', '`', '¨', '´', '~']

# Leer palabras desde 'palabras.txt'
try:
    with open('palabras.txt', 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    word_list = []
    print("Archivo 'palabras.txt' no encontrado. Asegúrate de crearlo en el mismo directorio.")

# Leer frases desde 'frases.txt'
try:
    with open('frases.txt', 'r', encoding='utf-8') as f:
        cpp_phrases = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    cpp_phrases = []
    print("Archivo 'frases.txt' no encontrado. Asegúrate de crearlo en el mismo directorio.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Práctica de Mecanografía')
        self.setGeometry(100, 100, 800, 400)

        # Crear un QStackedWidget para alternar entre el menú y la práctica
        self.stacked_widget = QStackedWidget()
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

        # Crear el widget del menú
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_label = QLabel('Selecciona el modo', self)
        self.menu_label.setAlignment(Qt.AlignCenter)
        self.menu_label.setFont(QFont('Fira Code', 24))
        self.menu_layout.addWidget(self.menu_label)

        # Botones de modo
        self.mode1_button = QPushButton('Modo 1: Caracteres Sueltos')
        self.mode2_button = QPushButton('Modo 2: Palabras Aleatorias')
        self.mode3_button = QPushButton('Modo 3: Frases en C++')

        # Conectar botones a funciones
        self.mode1_button.clicked.connect(self.start_mode1)
        self.mode2_button.clicked.connect(self.start_mode2)
        self.mode3_button.clicked.connect(self.start_mode3)

        self.menu_layout.addWidget(self.mode1_button)
        self.menu_layout.addWidget(self.mode2_button)
        self.menu_layout.addWidget(self.mode3_button)

        # Agregar el widget del menú al QStackedWidget
        self.stacked_widget.addWidget(self.menu_widget)

        # Inicializar el widget de práctica
        self.practice_widget = TypingPractice()
        self.stacked_widget.addWidget(self.practice_widget)

        # Configurar la paleta de colores (modo oscuro)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Fondo negro
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Texto blanco
        self.setPalette(palette)
        self.menu_widget.setPalette(palette)
        self.practice_widget.setPalette(palette)

        # Establecer fuentes y estilos para el menú
        buttons = [self.mode1_button, self.mode2_button, self.mode3_button]
        for btn in buttons:
            btn.setFont(QFont('Fira Code', 16))
            btn.setStyleSheet('background-color: #2E3440; color: #D8DEE9; padding: 10px;')

    def start_mode1(self):
        self.practice_widget.set_mode(1)
        self.stacked_widget.setCurrentWidget(self.practice_widget)
        self.practice_widget.start_practice()

    def start_mode2(self):
        self.practice_widget.set_mode(2)
        self.stacked_widget.setCurrentWidget(self.practice_widget)
        self.practice_widget.start_practice()

    def start_mode3(self):
        self.practice_widget.set_mode(3)
        self.stacked_widget.setCurrentWidget(self.practice_widget)
        self.practice_widget.start_practice()

class TypingPractice(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = 1  # Modo por defecto
        self.ppm_list = []  # Lista para almacenar los PPM individuales

        self.current_text = ''
        self.start_time = None  # Indica si el tiempo ha comenzado

        self.initUI()

    def initUI(self):
        # Crear el layout principal
        self.layout = QVBoxLayout(self)

        # Layout para mostrar caracteres
        self.char_layout = QHBoxLayout()
        self.char_layout.setAlignment(Qt.AlignCenter)

        # Etiqueta para los caracteres ya escritos (solo para modos 2 y 3)
        self.typed_label = QLabel('', self)
        self.typed_label.setAlignment(Qt.AlignLeft)
        self.typed_label_font = QFont('Fira Code', 36)
        self.typed_label.setFont(self.typed_label_font)
        self.typed_label.setStyleSheet('color: #A3BE8C')  # Verde para correcto

        # Etiqueta para los caracteres restantes
        self.remaining_label = QLabel('', self)
        self.remaining_label.setAlignment(Qt.AlignLeft)
        self.remaining_label_font = QFont('Fira Code', 36)
        self.remaining_label.setFont(self.remaining_label_font)
        self.remaining_label.setStyleSheet('color: #D8DEE9')  # Blanco/gris claro

        # Etiquetas para modo 1 (caracter actual y siguientes)
        self.label = QLabel('', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_font = QFont('Fira Code', 100)
        self.label.setFont(self.label_font)

        self.next_label1 = QLabel('', self)
        self.next_label1.setAlignment(Qt.AlignCenter)
        self.next_label1_font = QFont('Fira Code', 50)
        self.next_label1.setFont(self.next_label1_font)
        self.next_label1.setStyleSheet('color: gray')

        self.next_label2 = QLabel('', self)
        self.next_label2.setAlignment(Qt.AlignCenter)
        self.next_label2_font = QFont('Fira Code', 30)
        self.next_label2.setFont(self.next_label2_font)
        self.next_label2.setStyleSheet('color: gray')

        # Añadir widgets al layout
        self.char_layout.addWidget(self.label)
        self.char_layout.addWidget(self.next_label1)
        self.char_layout.addWidget(self.next_label2)
        self.layout.addLayout(self.char_layout)

        # Etiqueta de estadísticas
        self.stats_label = QLabel('Tiempo promedio (mediana): N/A', self)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setFont(QFont('Fira Code', 14))
        self.layout.addWidget(self.stats_label)

        # Etiqueta de resultado
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Fira Code', 18))
        self.layout.addWidget(self.result_label)

        # Etiqueta de instrucciones
        self.info_label = QLabel('Escribe el texto mostrado', self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont('Fira Code', 16))
        self.layout.addWidget(self.info_label)

        # Campo de entrada oculto
        self.hidden_input = QLineEdit(self)
        self.hidden_input.setFixedHeight(0)
        self.hidden_input.setFixedWidth(0)
        self.hidden_input.setFocusPolicy(Qt.NoFocus)
        self.hidden_input.setStyleSheet("background: transparent; border: none; color: transparent;")
        self.hidden_input.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.hidden_input)

    def set_mode(self, mode):
        self.mode = mode
        self.ppm_list = []
        self.result_label.setText('')
        self.stats_label.setText('Tiempo promedio (mediana): N/A')
        self.info_label.setText('Escribe el texto mostrado')
        self.current_text = ''
        self.start_time = None
        self.hidden_input.clear()
        self.double_press_buffer = ''
        self.input_buffer = ''

        if mode == 1:
            # Mostrar etiquetas para Modo 1
            self.char_layout.removeWidget(self.typed_label)
            self.char_layout.removeWidget(self.remaining_label)
            self.typed_label.hide()
            self.remaining_label.hide()

            self.char_layout.addWidget(self.label)
            self.char_layout.addWidget(self.next_label1)
            self.char_layout.addWidget(self.next_label2)
            self.label.show()
            self.next_label1.show()
            self.next_label2.show()
        else:
            # Mostrar etiquetas para Modos 2 y 3
            self.char_layout.removeWidget(self.label)
            self.char_layout.removeWidget(self.next_label1)
            self.char_layout.removeWidget(self.next_label2)
            self.label.hide()
            self.next_label1.hide()
            self.next_label2.hide()

            self.char_layout.addWidget(self.typed_label)
            self.char_layout.addWidget(self.remaining_label)
            self.typed_label.show()
            self.remaining_label.show()

    def start_practice(self):
        if self.mode == 1:
            self.next_char(initialize=True)
        elif self.mode == 2:
            self.next_word()
        elif self.mode == 3:
            self.next_phrase()
        # Establecer el foco en el campo de entrada oculto
        self.hidden_input.setFocus()

    def next_char(self, initialize=False):
        if initialize:
            # Inicializar la cola de caracteres
            self.char_queue = [random.choice(char_list) for _ in range(3)]
        else:
            # Avanzar al siguiente caracter
            self.char_queue.pop(0)
            self.char_queue.append(random.choice(char_list))

        self.current_text = self.char_queue[0]
        self.label.setText(self.current_text)
        self.next_label1.setText(self.char_queue[1])
        self.next_label2.setText(self.char_queue[2])
        self.result_label.setText('')
        self.hidden_input.clear()
        self.start_time = time.time()  # Iniciar el tiempo cuando se muestra el carácter
        # Reiniciar buffer de doble pulsación
        self.double_press_buffer = ''

    def next_word(self):
        if not word_list:
            self.current_text = "Lista de palabras vacía. Agrega palabras a 'palabras.txt'."
        else:
            self.current_text = random.choice(word_list)
        self.typed_label.setText('')
        self.remaining_label.setText(self.current_text)
        self.result_label.setText('')
        self.hidden_input.clear()
        self.start_time = None  # Se iniciará al presionar una tecla

    def next_phrase(self):
        if not cpp_phrases:
            self.current_text = "Lista de frases vacía. Agrega frases a 'frases.txt'."
        else:
            self.current_text = random.choice(cpp_phrases)
        self.typed_label.setText('')
        self.remaining_label.setText(self.current_text)
        self.result_label.setText('')
        self.hidden_input.clear()
        self.start_time = None  # Se iniciará al presionar una tecla

    def on_text_changed(self, text):
        if self.mode != 1 and self.start_time is None and text:
            # Iniciar el tiempo cuando el usuario empieza a escribir (Modos 2 y 3)
            self.start_time = time.time()

        if self.mode == 1:
            # Modo de caracteres sueltos
            pressed_char = text[-1] if text else ''
            if not pressed_char:
                return

            pressed_char_lower = pressed_char.lower()
            expected_char = self.current_text.lower()

            if expected_char in double_press_chars:
                # Manejar doble pulsación
                if self.double_press_buffer == '':
                    self.double_press_buffer = pressed_char_lower
                elif self.double_press_buffer == pressed_char_lower:
                    self.process_correct_input()
                    self.double_press_buffer = ''
                else:
                    self.show_incorrect()
                    self.double_press_buffer = ''
            else:
                if pressed_char_lower == expected_char:
                    self.process_correct_input()
                else:
                    self.show_incorrect()
            self.hidden_input.clear()
        else:
            # Modo de palabras o frases
            self.input_buffer = text
            expected_text = self.current_text[:len(self.input_buffer)]
            if self.input_buffer == expected_text:
                # Mostrar texto con los caracteres correctos en verde
                self.typed_label.setText(self.input_buffer)
                self.remaining_label.setText(self.current_text[len(self.input_buffer):])
                if self.input_buffer == self.current_text:
                    self.process_correct_input()
            else:
                self.show_incorrect()

    def process_correct_input(self):
        if self.start_time is None:
            duration = 0
        else:
            end_time = time.time()
            duration = end_time - self.start_time

        if self.mode == 1:
            # Modo 1: Caracteres Sueltos
            # Calcular PPM basado en la longitud promedio de palabra
            ppm = (1 / AVERAGE_WORD_LENGTH) / (duration / 60) if duration > 0 else 0
        elif self.mode == 2:
            # Modo 2: Palabras Aleatorias
            words_typed = 1  # Cada entrada es una palabra
            ppm = words_typed / (duration / 60) if duration > 0 else 0
        elif self.mode == 3:
            # Modo 3: Frases en C++
            words_typed = len(self.current_text.split())
            ppm = words_typed / (duration / 60) if duration > 0 else 0

        self.ppm_list.append(ppm)
        if self.ppm_list:
            median_ppm = statistics.median(self.ppm_list)
            self.stats_label.setText(f'Último PPM: {ppm:.2f}   PPM Mediana: {median_ppm:.2f}')
        else:
            self.stats_label.setText(f'Último PPM: {ppm:.2f}   PPM Mediana: N/A')

        self.result_label.setText('¡Correcto!')
        self.result_label.setStyleSheet('color: #A3BE8C')  # Verde
        QTimer.singleShot(500, self.next_item)  # Esperar 0.5 segundos antes del siguiente

    def show_incorrect(self):
        self.result_label.setText('Incorrecto, intenta de nuevo.')
        self.result_label.setStyleSheet('color: #BF616A')  # Rojo
        # Restablecer el texto mostrado
        if self.mode == 1:
            # En modo 1, no es necesario restablecer etiquetas
            pass
        else:
            # En modo de frases, restablecer hasta el último espacio o guión bajo
            if self.mode == 3:
                last_space_index = max(
                    self.input_buffer.rstrip().rfind(' '),
                    self.input_buffer.rstrip().rfind('_')
                )
                if last_space_index == -1:
                    # Si no hay espacios ni guiones bajos, reiniciar todo
                    self.input_buffer = ''
                else:
                    # Mantener hasta el último espacio o guión bajo
                    self.input_buffer = self.input_buffer[:last_space_index + 1]
                self.hidden_input.setText(self.input_buffer)
                self.typed_label.setText(self.input_buffer)
                self.remaining_label.setText(self.current_text[len(self.input_buffer):])
            else:
                self.input_buffer = ''
                self.hidden_input.clear()
                self.typed_label.setText('')
                self.remaining_label.setText(self.current_text)
        if self.mode != 1:
            self.start_time = None  # Reiniciar el tiempo
        self.double_press_buffer = ''

    def next_item(self):
        if self.mode == 1:
            self.next_char()
        elif self.mode == 2:
            self.next_word()
        elif self.mode == 3:
            self.next_phrase()
        # Restablecer el foco en el campo de entrada oculto
        self.hidden_input.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())