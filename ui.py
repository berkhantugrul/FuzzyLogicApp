import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from fuzzy_logic import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

themeUpdater = [1] # 0-dark theme / 1-light theme - EXPERIMENTAL


# MAIN WINDOW DEFINITION
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuzzy Logic Interface")
        self.setGeometry(100, 100, 1750, 1000)

        self.Components()

    # UI Component's function
    def Components(self):
        
        # Main Interface Header Font
        header_font = QFont("Calibri", 14)

        # Main Interface Sub-Text Font
        text_font = QFont("Calibri", 13)

        # Main Interface Button Font,
        button_font = QFont("Calibri", 11)

        """ LEFT-PART OF INTERFACE: LABEL - SPINBOX - BUTTON - DARKMODE SWITCH """

        # Part's Frame
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(40, 40, 310, 900)  # Çerçeve çizgi kalınlığı
        self.left_frame.setStyleSheet("""
            QFrame {
                border: 0.5px solid rgba(0, 0, 0, 0.5);
            }
        """)

        # 'Input Values' header
        self.input_values = QLabel(self)
        self.input_values.setText("Input Values")
        self.input_values.setFont(header_font)
        self.input_values.setGeometry(QRect(130, 50, 110, 31))
        self.input_values.setStyleSheet("background: transparent; border: none;") 

        # 'MarketValue' sub-text
        self.market_value_txt = QLabel(self)
        self.market_value_txt.setText("MarketValue")
        self.market_value_txt.setFont(text_font)
        self.market_value_txt.setGeometry(QRect(60, 100, 171, 31))
        self.market_value_txt.setStyleSheet("background: transparent; border: none;") 

        # 'MarketValue's Spinbox
        self.market_value_spinbox = QSpinBox(self)
        self.market_value_spinbox.setGeometry(QRect(240, 100, 91, 31))
        self.market_value_spinbox.setMinimum(-1)
        self.market_value_spinbox.setValue(-1)
        self.market_value_spinbox.setMaximum(1000)
        self.market_value_spinbox.setStyleSheet("QSpinBox { font-size: 15px; }")

        # 'Location' sub-text
        self.location_txt = QLabel(self)
        self.location_txt.setText("Location")
        self.location_txt.setFont(text_font)
        self.location_txt.setGeometry(QRect(60, 140, 171, 31))
        self.location_txt.setStyleSheet("background: transparent; border: none;") 

        # 'Location's Spinbox
        self.location_spinbox = QDoubleSpinBox(self)
        self.location_spinbox.setGeometry(QRect(240, 140, 91, 31))
        self.location_spinbox.setMinimum(-1)
        self.location_spinbox.setValue(-1)
        self.location_spinbox.setMaximum(1000)
        self.location_spinbox.setSingleStep(0.1)
        self.location_spinbox.setDecimals(1)
        self.location_spinbox.setStyleSheet("QDoubleSpinBox { font-size: 15px; }")

        # 'Asset' sub-text
        self.asset_txt = QLabel(self)
        self.asset_txt.setText("Asset")
        self.asset_txt.setFont(text_font)
        self.asset_txt.setGeometry(QRect(60, 180, 171, 31))
        self.asset_txt.setStyleSheet("background: transparent; border: none;") 

        # 'Asset's Spinbox
        self.asset_spinbox = QSpinBox(self)
        self.asset_spinbox.setGeometry(QRect(240, 180, 91, 31))
        self.asset_spinbox.setMinimum(-1)
        self.asset_spinbox.setValue(-1)
        self.asset_spinbox.setMaximum(1000)
        self.asset_spinbox.setStyleSheet("QSpinBox { font-size: 15px; }")

        # 'Income' sub-text
        self.income_txt = QLabel(self)
        self.income_txt.setText("Income")
        self.income_txt.setFont(text_font)
        self.income_txt.setGeometry(QRect(60, 220, 171, 31))
        self.income_txt.setStyleSheet("background: transparent; border: none;") 

        # 'Income' Spinbox
        self.income_spinbox = QSpinBox(self)
        self.income_spinbox.setGeometry(QRect(240, 220, 91, 31))
        self.income_spinbox.setMinimum(-1)
        self.income_spinbox.setValue(-1)
        self.income_spinbox.setMaximum(1000)
        self.income_spinbox.setStyleSheet("QSpinBox { font-size: 15px; }")

        # 'Interest' sub-text
        self.interest_txt = QLabel(self)
        self.interest_txt.setText("Interest")
        self.interest_txt.setFont(text_font)
        self.interest_txt.setGeometry(QRect(60, 260, 171, 31))
        self.interest_txt.setStyleSheet("background: transparent; border: none;") 

        # 'Interest's Spinbox
        self.interest_spinbox = QDoubleSpinBox(self)
        self.interest_spinbox.setGeometry(QRect(240, 260, 91, 31))
        self.interest_spinbox.setMinimum(-1)
        self.interest_spinbox.setValue(-1)
        self.interest_spinbox.setMaximum(1000)
        self.interest_spinbox.setDecimals(1)
        self.interest_spinbox.setSingleStep(0.1)
        self.interest_spinbox.setStyleSheet("QDoubleSpinBox { font-size: 15px; }")

        # 'Reset Inputs' Button
        self.reset_inputs_button = QPushButton("Reset All", self)
        self.reset_inputs_button.resize(270, 40)
        self.reset_inputs_button.setFont(button_font)
        self.reset_inputs_button.move(60, 330)
        self.reset_inputs_button.clicked.connect(self.ResetInputs)

        # 'Show I/O Graphs' Button
        # self.show_graphs_button = QPushButton("Show I/O Graphs", self)
        # self.show_graphs_button.resize(270, 40)
        # self.show_graphs_button.setFont(button_font)
        # self.show_graphs_button.move(60, 780)

        # 'System Evaluation Info Text'
        self.system_info = QLabel(self)
        self.system_info.setText("Tips:\n\nFor fuzzy system's evaluation, all of \ninput values have to be entered. \nOtherwise, the system will return an \nerror message.")
        self.system_info.setFont(QFont("Calibri", 12, QFont.Bold))
        self.system_info.setGeometry(QRect(60, 440, 270, 120))
        self.system_info.setStyleSheet("background: transparent; border: none;") 

        # Show Graph Info Text
        self.graph_info = QLabel(self)
        self.graph_info.setText("To show a fuzzy variable's graph,\na variable must be selected. \nOtherwise, the system will return an \nerror message.")
        self.graph_info.setFont(QFont("Calibri", 12, QFont.Bold))
        self.graph_info.setGeometry(QRect(60, 570, 270, 120))
        self.graph_info.setStyleSheet("background: transparent; border: none;") 

        # Dark-Light Mode Switch Button
        self.mode_switch = QPushButton("Dark/Light Mode", self)
        self.mode_switch.resize(270, 40)
        self.mode_switch.setFont(button_font)
        self.mode_switch.move(60, 390)
        self.mode_switch.clicked.connect(self.ChangeMode)

        # 'TERMINATE FUZZY SYSTEM' Button
        self.terminate = QPushButton("TERMINATE FUZZY SYSTEM", self)
        self.terminate.resize(270, 100)
        self.terminate.setFont(button_font)
        self.terminate.move(60, 720)
        self.terminate.clicked.connect(self.TerminateSystem)

        """ MIDDLE PART OF INTERFACE: SHOWING THE INPUT RESULTS """

        # Part's Frame
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(370, 40, 660, 900)  # Çerçeve çizgi kalınlığı
        self.left_frame.setStyleSheet("""
            QFrame {
                border: 0.5px solid rgba(0, 0, 0, 0.5);
            }
        """)

         # 'INPUT GRAPHS' Header Text
        self.input_graphs_header = QLabel(self)
        self.input_graphs_header.setText("Input Classes & Graphs")
        self.input_graphs_header.setFont(header_font)
        self.input_graphs_header.setGeometry(QRect(610, 50, 200, 31)) 
        self.input_graphs_header.setStyleSheet("background: transparent; border: none;") 

        # 'Input' sub-header of table
        self.input_results = QLabel(self)
        self.input_results.setText("Input")
        self.input_results.setStyleSheet("background: transparent; border: none;") 
        self.input_results.setFont(text_font)
        self.input_results.setGeometry(450, 110, 60, 30)
        self.input_results.setStyleSheet("background: transparent; border: none;") 
        self.input_results.setAlignment(Qt.AlignCenter)
        
        # Input Value Results
        # 'Value' sub-header of table
        self.input_value_results = QLabel(self)
        self.input_value_results.setText("Value")
        self.input_value_results.setFont(text_font)
        self.input_value_results.setGeometry(620, 110, 47, 30)
        self.input_value_results.setStyleSheet("background: transparent; border: none;") 

        # 'Degree' sub-header of table
        self.input_value_results = QLabel(self)
        self.input_value_results.setText("Degree")
        self.input_value_results.setFont(text_font)
        self.input_value_results.setGeometry(760, 110, 47, 30)
        self.input_value_results.setStyleSheet("background: transparent; border: none;") 

        # 'Input-Class' sub-header of table
        self.input_results_class = QLabel(self)
        self.input_results_class.setText("Class")
        self.input_results_class.setStyleSheet("background: transparent; border: none;") 
        self.input_results_class.setFont(text_font)
        self.input_results_class.setGeometry(900, 110, 60, 30)
        self.input_results_class.setAlignment(Qt.AlignCenter)
        self.input_results_class.setStyleSheet("background: transparent; border: none;") 

        # 'MarketValue' sub-header of table
        self.market_value_lowheader = QLabel(self)
        self.market_value_lowheader.setText("MarketValue")
        self.market_value_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.market_value_lowheader.setFont(text_font)
        self.market_value_lowheader.setGeometry(420, 170, 120, 30)
        self.market_value_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.market_value_lowheader.setAlignment(Qt.AlignCenter)

        # MarketValue - Value
        self.market_value_degree = QLabel(self)
        self.market_value_degree.setText("-")
        self.market_value_degree.setFont(button_font)
        self.market_value_degree.move(730, 170)
        self.market_value_degree.setAlignment(Qt.AlignCenter)
        self.market_value_degree.setStyleSheet("background: transparent; border: none;") 
        
        # MarketValue - Degree
        self.market_value_value = QLabel(self)
        self.market_value_value.setText("-")
        self.market_value_value.setFont(button_font)
        self.market_value_value.move(590, 170)
        self.market_value_value.setAlignment(Qt.AlignCenter)
        self.market_value_value.setStyleSheet("background: transparent; border: none;")

        # MarketValue Input - Class text
        self.market_value_class = QLabel(self)
        self.market_value_class.setText("-")
        self.market_value_class.setFont(button_font)
        self.market_value_class.move(880, 170)
        self.market_value_class.setAlignment(Qt.AlignCenter)
        self.market_value_class.setStyleSheet("background: transparent; border: none;") 


        # 'Location' sub-header of table
        self.location_lowheader = QLabel(self)
        self.location_lowheader.setText("Location")
        self.location_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.location_lowheader.setFont(text_font)
        self.location_lowheader.setGeometry(420, 210, 120, 30)
        self.location_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.location_lowheader.setAlignment(Qt.AlignCenter)

        # Location - Value
        self.location_degree = QLabel(self)
        self.location_degree.setText("-")
        self.location_degree.setFont(button_font)
        self.location_degree.move(730, 210)
        self.location_degree.setAlignment(Qt.AlignCenter)
        self.location_degree.setStyleSheet("background: transparent; border: none;") 

        # Location - Degree
        self.location_value = QLabel(self)
        self.location_value.setText("-")
        self.location_value.setFont(button_font)
        self.location_value.move(590, 210)
        self.location_value.setAlignment(Qt.AlignCenter)
        self.location_value.setStyleSheet("background: transparent; border: none;")

        # Location Input - Class text
        self.location_class = QLabel(self)
        self.location_class.setText("-")
        self.location_class.setFont(button_font)
        self.location_class.move(880, 210)
        self.location_class.setAlignment(Qt.AlignCenter)
        self.location_class.setStyleSheet("background: transparent; border: none;") 

        # 'Asset' sub-header of table
        self.asset_lowheader = QLabel(self)
        self.asset_lowheader.setText("Asset")
        self.asset_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.asset_lowheader.setFont(text_font)
        self.asset_lowheader.setGeometry(420, 250, 120, 30)
        self.asset_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.asset_lowheader.setAlignment(Qt.AlignCenter)

        # Asset - Value
        self.asset_degree = QLabel(self)
        self.asset_degree.setText("-")
        self.asset_degree.setFont(button_font)
        self.asset_degree.move(730, 250)
        self.asset_degree.setAlignment(Qt.AlignCenter)
        self.asset_degree.setStyleSheet("background: transparent; border: none;") 

        # Asset - Degree
        self.asset_value = QLabel(self)
        self.asset_value.setText("-")
        self.asset_value.setFont(button_font)
        self.asset_value.move(590, 250)
        self.asset_value.setAlignment(Qt.AlignCenter)
        self.asset_value.setStyleSheet("background: transparent; border: none;")

        # Asset Input - Class text
        self.asset_class = QLabel(self)
        self.asset_class.setText("-")
        self.asset_class.setFont(button_font)
        self.asset_class.move(880, 250)
        self.asset_class.setAlignment(Qt.AlignCenter)
        self.asset_class.setStyleSheet("background: transparent; border: none;")         

        # 'Income' sub-header of table
        self.income_lowheader = QLabel(self)
        self.income_lowheader.setText("Income")
        self.income_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.income_lowheader.setFont(text_font)
        self.income_lowheader.setGeometry(420, 290, 120, 30)
        self.income_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.income_lowheader.setAlignment(Qt.AlignCenter)
        
        # Income - Value
        self.income_degree = QLabel(self)
        self.income_degree.setText("-")
        self.income_degree.setFont(button_font)
        self.income_degree.move(730, 290)
        self.income_degree.setAlignment(Qt.AlignCenter)
        self.income_degree.setStyleSheet("background: transparent; border: none;") 

        # Income - Degree
        self.income_value = QLabel(self)
        self.income_value.setText("-")
        self.income_value.setFont(button_font)
        self.income_value.move(590, 290)
        self.income_value.setAlignment(Qt.AlignCenter)
        self.income_value.setStyleSheet("background: transparent; border: none;")

        # Income Input - Class text
        self.income_class = QLabel(self)
        self.income_class.setText("-")
        self.income_class.setFont(button_font)
        self.income_class.move(880, 290)
        self.income_class.setAlignment(Qt.AlignCenter)
        self.income_class.setStyleSheet("background: transparent; border: none;") 

        # 'Interest' sub-header of table
        self.interest_lowheader = QLabel(self)
        self.interest_lowheader.setText("Interest")
        self.interest_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.interest_lowheader.setFont(text_font)
        self.interest_lowheader.setGeometry(420, 330, 120, 30)
        self.interest_lowheader.setStyleSheet("background: transparent; border: none;") 
        self.interest_lowheader.setAlignment(Qt.AlignCenter)

        # Interest - Degree
        self.interest_value = QLabel(self)
        self.interest_value.setText("-")
        self.interest_value.setFont(button_font)
        self.interest_value.move(590, 330)
        self.interest_value.setAlignment(Qt.AlignCenter)
        self.interest_value.setStyleSheet("background: transparent; border: none;")

        # Interest - Value
        self.interest_degree = QLabel(self)
        self.interest_degree.setText("-")
        self.interest_degree.setFont(button_font)
        self.interest_degree.move(730, 330)
        self.interest_degree.setAlignment(Qt.AlignCenter)
        self.interest_degree.setStyleSheet("background: transparent; border: none;") 

        # Interest Input - Class text
        self.interest_class = QLabel(self)
        self.interest_class.setText("-")
        self.interest_class.setFont(button_font)
        self.interest_class.move(880, 330)
        self.interest_class.setAlignment(Qt.AlignCenter)
        self.interest_class.setStyleSheet("background: transparent; border: none;") 

        # Horizontal line between headers and contents
        self.in_line = QFrame(self)
        self.in_line.setGeometry(390, 160, 620, 1)
        self.in_line.setLineWidth(2)  # Çerçeve çizgi kalınlığı
        self.in_line.setStyleSheet("background-color: black;")

        # Input Graph's Show Area
        # frame1 = QFrame(self)
        # frame1.setGeometry(390, 440, 620, 380) 
        # frame1.setFrameShape(QFrame.Box)  # Çerçeve tipi
        # frame1.setLineWidth(2)  # Çerçeve çizgi kalınlığı
        # frame1.setStyleSheet("background-color: transparent; border-color: #000;")

        self.input_graph_area = QLabel(self)
        self.input_graph_area.setGeometry(390, 440, 620, 480) 

        # Input Graph's Selecting QComboBox
        self.select_input_graph = QComboBox(self)
        self.select_input_graph.addItems(['Select Graph', 'Market Value', 'Location', 'Asset', 'Income', 'Interest']) 
        self.select_input_graph.setGeometry(390, 400, 470, 30)

        # SHOW GRAPH BUTTON
        self.show_input_graph_btn = QPushButton("Show Graph", self)
        self.show_input_graph_btn.setFont(button_font)
        self.show_input_graph_btn.resize(130,30)
        self.show_input_graph_btn.move(880, 400)
        self.show_input_graph_btn.clicked.connect(self.showInputGraph)


        """ RIGHT PART OF INTERFACE: SHOWING THE OUTPUT RESULTS """

        # Part's Frame
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(1050, 40, 660, 900)  # Çerçeve çizgi kalınlığı
        self.left_frame.setStyleSheet("""
            QFrame {
                border: 0.5px solid rgba(0, 0, 0, 0.5);
            }
        """)

        # 'Output Results' Header
        self.output_results_header = QLabel(self)
        self.output_results_header.setText("Output Results & Graphs")
        self.output_results_header.setFont(header_font)
        self.output_results_header.setGeometry(QRect(1280, 50, 200, 31)) # +420
        self.output_results_header.setStyleSheet("background: transparent; border: none;") 

        # 'Output' sub-header of table
        self.output_results = QLabel(self)
        self.output_results.setText("Output")
        self.output_results.setStyleSheet("background: transparent; border: none;") 
        self.output_results.setFont(text_font)
        self.output_results.setGeometry(1140, 110, 60, 30)
        self.output_results.setStyleSheet("background: transparent; border: none;") 

        # 'Value' sub-header of table
        self.output_value_results = QLabel(self)
        self.output_value_results.setText("Value")
        self.output_value_results.setFont(text_font)
        self.output_value_results.setGeometry(1300, 110, 47, 30)
        self.output_value_results.setStyleSheet("background: transparent; border: none;") 

        # 'Degree' sub-header of table
        self.output_degree_header = QLabel(self)
        self.output_degree_header.setText("Degree")
        self.output_degree_header.setFont(text_font)
        self.output_degree_header.setGeometry(1430, 110, 50, 30)
        self.output_degree_header.setStyleSheet("background: transparent; border: none;") 

        # 'Class' sub-header of table
        self.class_results = QLabel(self)
        self.class_results.setText("Class")
        self.class_results.setFont(text_font)
        self.class_results.setGeometry(1580, 110, 45, 30)
        self.class_results.setStyleSheet("background: transparent; border: none;") 

        # Horizontal line between headers and contents
        self.out_line = QFrame(self)
        self.out_line.setGeometry(1070, 160, 620, 1)
        self.out_line.setLineWidth(2)  # Çerçeve çizgi kalınlığı
        self.out_line.setStyleSheet("background-color: black;")

        # 'House Evaluation' output type text
        self.house_eval_hdr = QLabel(self)
        self.house_eval_hdr.setText("House")
        self.house_eval_hdr.setFont(text_font)
        self.house_eval_hdr.setGeometry(1100, 170, 130, 30)
        self.house_eval_hdr.setAlignment(Qt.AlignCenter)
        self.house_eval_hdr.setStyleSheet("background: transparent; border: none;") 

        # House Evaluation - Value text
        self.house_eval_value = QLabel(self)
        self.house_eval_value.setText("-")
        self.house_eval_value.setFont(button_font)
        self.house_eval_value.move(1270, 170)
        self.house_eval_value.setAlignment(Qt.AlignCenter)
        self.house_eval_value.setStyleSheet("background: transparent; border: none;") 

        # House Evaluation - Degree
        self.house_eval_degree = QLabel(self)
        self.house_eval_degree.setText("-")
        self.house_eval_degree.setFont(button_font)
        self.house_eval_degree.move(1405, 170)
        self.house_eval_degree.setAlignment(Qt.AlignCenter)
        self.house_eval_degree.setStyleSheet("background: transparent; border: none;") 

        # House Evaluation - Class text
        self.house_eval_class = QLabel(self)
        self.house_eval_class.setText("-")
        self.house_eval_class.setFont(button_font)
        self.house_eval_class.move(1550, 170)
        self.house_eval_class.setAlignment(Qt.AlignCenter)
        self.house_eval_class.setStyleSheet("background: transparent; border: none;") 

        # 'Applicant Evaluation' output type text
        self.applicant_eval = QLabel(self)
        self.applicant_eval.setText("Applicant")
        self.applicant_eval.setFont(text_font)
        self.applicant_eval.setGeometry(1090, 230, 150, 30)
        self.applicant_eval.setAlignment(Qt.AlignCenter)
        self.applicant_eval.setStyleSheet("background: transparent; border: none;") 

        # Applicant Evaluation - Value text
        self.applicant_eval_value = QLabel(self)
        self.applicant_eval_value.setText("-")
        self.applicant_eval_value.setFont(button_font)
        self.applicant_eval_value.move(1270, 230)
        self.applicant_eval_value.setAlignment(Qt.AlignCenter)
        self.applicant_eval_value.setStyleSheet("background: transparent; border: none;") 

        # Applicant Evaluation - Degree
        self.applicant_eval_degree = QLabel(self)
        self.applicant_eval_degree.setText("-")
        self.applicant_eval_degree.setFont(button_font)
        self.applicant_eval_degree.move(1405, 230)
        self.applicant_eval_degree.setAlignment(Qt.AlignCenter)
        self.applicant_eval_degree.setStyleSheet("background: transparent; border: none;") 

        # Applicant Evaluation - Class text
        self.applicant_eval_class = QLabel(self)
        self.applicant_eval_class.setText("-")
        self.applicant_eval_class.setFont(button_font)
        self.applicant_eval_class.move(1550, 230)
        self.applicant_eval_class.setAlignment(Qt.AlignCenter)
        self.applicant_eval_class.setStyleSheet("background: transparent; border: none;") 

        # 'Credit Evaluation' output type text
        self.credit_eval = QLabel(self)
        self.credit_eval.setText("Credit")
        self.credit_eval.setFont(text_font)
        self.credit_eval.setGeometry(1100, 290, 130, 30)
        self.credit_eval.setAlignment(Qt.AlignCenter)
        self.credit_eval.setStyleSheet("background: transparent; border: none;") 

        # 'Credit Evaluation' - Value text
        self.credit_eval_value = QLabel(self)
        self.credit_eval_value.setText("-")
        self.credit_eval_value.setFont(button_font)
        self.credit_eval_value.move(1270, 290)
        self.credit_eval_value.setAlignment(Qt.AlignCenter)
        self.credit_eval_value.setStyleSheet("background: transparent; border: none;") 

        # 'Credit Evaluation' - Degree text
        self.credit_eval_degree = QLabel(self)
        self.credit_eval_degree.setText("-")
        self.credit_eval_degree.setFont(button_font)
        self.credit_eval_degree.move(1405, 290)
        self.credit_eval_degree.setAlignment(Qt.AlignCenter)
        self.credit_eval_degree.setStyleSheet("background: transparent; border: none;")         

        # 'Credit Evaluation' - Class text
        self.credit_eval_class = QLabel(self)
        self.credit_eval_class.setText("-")
        self.credit_eval_class.setFont(button_font)
        self.credit_eval_class.move(1550, 290)
        self.credit_eval_class.setAlignment(Qt.AlignCenter)
        self.credit_eval_class.setStyleSheet("background: transparent; border: none;") 
        
        # Output Graph's Selecting QComboBox
        self.select_output_graph = QComboBox(self)
        self.select_output_graph.addItems(['Select Graph', 'House', 'Applicant', 'Credit'])
        self.select_output_graph.setGeometry(1070, 400, 470, 30)

        # SHOWING THE SELECTED OUTPUT GRAPH
        self.show_output_graph = QPushButton("Show Graph", self)
        self.show_output_graph.setFont(button_font)
        self.show_output_graph.resize(130, 30)
        self.show_output_graph.move(1560, 400)
        self.show_output_graph.clicked.connect(self.showOutputGraph)
        
        # The output graph's area
        # frame2 = QFrame(self)
        # frame2.setGeometry(1070, 440, 620, 380)
        # frame2.setFrameShape(QFrame.Box)  # Çerçeve tipi: Box, Panel, HLine, VLine, vb.
        # frame2.setLineWidth(2)  # Çerçeve çizgi kalınlığı
        # frame2.setStyleSheet("background-color: transparent; border-color: #000;")

        self.output_graph_area = QLabel(self)
        self.output_graph_area.setGeometry(1070, 440, 620, 480)

 
    # Resetting the all interface
    def ResetInputs(self):
        if (self.market_value_spinbox.value() != -1 or self.location_spinbox.value() >= 0 or self.interest_spinbox.value() >= 0 or self.income_spinbox.value() != -1 or self.asset_spinbox.value() != -1):
            self.market_value_spinbox.setValue(-1)
            self.location_spinbox.setValue(-1)
            self.interest_spinbox.setValue(-1)
            self.income_spinbox.setValue(-1)
            self.asset_spinbox.setValue(-1)           
            
            self.market_value_class.setText("-")
            self.market_value_degree.setText("-")
            self.market_value_value.setText("-")

            self.location_class.setText("-")
            self.location_degree.setText("-")
            self.location_value.setText("-")

            self.asset_class.setText("-")
            self.asset_degree.setText("-")
            self.asset_value.setText("-")

            self.income_class.setText("-")
            self.income_degree.setText("-")
            self.income_value.setText("-")

            self.interest_class.setText("-")
            self.interest_degree.setText("-")
            self.interest_value.setText("-")

            self.applicant_eval_class.setText("-")
            self.applicant_eval_value.setText("-")
            self.applicant_eval_degree.setText("-")

            self.house_eval_class.setText("-")
            self.house_eval_value.setText("-")
            self.house_eval_degree.setText("-")

            self.credit_eval_class.setText("-")
            self.credit_eval_value.setText("-")
            self.credit_eval_degree.setText("-")

        else:
            "Return a QMessageBox"
            resetError = QMessageBox(self)
            resetError.setWindowTitle("Reset Error")
            resetError.setText("Interface has already reset!")
            resetError.setIcon(QMessageBox.Warning)
            resetError.setStyleSheet("""
                                     QMessageBox QLabel {
                                        background: transparent;
                                        border: none;
                                    }
                                    QMessageBox QPushButton
                                    {
                                        border: 1px solid #5a5a5a;
                                        border-radius: 4px;  
                                        min-width: 50px;  
                                        max-width: 50px; 
                                        min-height: 20px;   
                                        max-height: 20px;                                 
                                    }
                                    """) 
            resetError.exec_()              

    def ChangeMode(self):

        if self.sender() == self.mode_switch:

            if themeUpdater[0] == 0:
                themeUpdater[0] = 1
                LightMode(app)

            else:
                themeUpdater[0] = 0
                DarkMode(app)
            

    def TerminateSystem(self):

        if self.sender() == self.terminate:
            
            if (self.market_value_spinbox.value() != -1 and self.location_spinbox.value() >= 0 and self.interest_spinbox.value() >= 0 and self.income_spinbox.value() != -1 and self.asset_spinbox.value() != -1):
                
                market_value_val = self.market_value_spinbox.value()
                location_val = self.location_spinbox.value()
                asset_val = self.asset_spinbox.value()
                income_val = self.income_spinbox.value()
                interest_val = self.interest_spinbox.value()

                # Run Sim
                inputs = []
                self.input_vars = {'MarketValue':market_value_val, 'Location':location_val, 'Asset':asset_val, 'Income':income_val, 'Interest':interest_val}
                #print(self.input_vars)
                
                inputs.append(self.input_vars)
                #print(inputs)

                output, output_degrees, input_degrees, dominant_categories = main(inputs)

                # Getting the outputs and related classes
                house_out = output["House"]
                applicant_out = output["Applicant"]
                credit_out = output["Credit"]

                market_value_degrees_dict = input_degrees["MarketValue"]
                location_degrees_dict = input_degrees["Location"]
                asset_degrees_dict = input_degrees["Asset"]
                income_degrees_dict = input_degrees["Income"]
                interest_degrees_dict = input_degrees["Interest"]


                for i in market_value_degrees_dict.keys():
                    if market_value_degrees_dict[i] == max(market_value_degrees_dict.values()):
                        max_mv_class = i
                
                for i in location_degrees_dict.keys():
                    if location_degrees_dict[i] == max(location_degrees_dict.values()):
                        max_location_class = i

                for i in asset_degrees_dict.keys():
                    if asset_degrees_dict[i] == max(asset_degrees_dict.values()):
                        max_asset_class = i

                for i in income_degrees_dict.keys():
                    if income_degrees_dict[i] == max(income_degrees_dict.values()):
                        max_income_class = i

                for i in interest_degrees_dict.keys():
                    if interest_degrees_dict[i] == max(interest_degrees_dict.values()):
                        max_interest_class = i                        

                                
                house_deg = max(output_degrees["House"].values())
                applicant_deg = max(output_degrees["Applicant"].values())
                credit_deg = max(output_degrees["Credit"].values())

                house_class = dominant_categories["House"]
                applicant_class = dominant_categories["Applicant"]
                credit_class = dominant_categories["Credit"]

                # OUTPUT RESULTS ARE SHOWED ON UI
                self.house_eval_class.setText(house_class)
                self.house_eval_degree.setText(str(house_deg)[:3])
                self.house_eval_value.setText(f"{house_out:.2f}")
                
                self.applicant_eval_class.setText(applicant_class)
                self.applicant_eval_degree.setText(str(applicant_deg)[:3])
                self.applicant_eval_value.setText(f"{applicant_out:.2f}")
                
                self.credit_eval_class.setText(credit_class)
                self.credit_eval_degree.setText(str(credit_deg)[:3])
                self.credit_eval_value.setText(f"{credit_out:.2f}")

                # INPUT RESULTS ARE SHOWED ON UI
                self.market_value_class.setText(max_mv_class)
                self.location_class.setText(max_location_class)
                self.asset_class.setText(max_asset_class)
                self.income_class.setText(max_income_class)
                self.interest_class.setText(max_interest_class)

                self.market_value_value.setText(str(market_value_val))
                self.location_value.setText(str(location_val))
                self.asset_value.setText(str(asset_val))
                self.income_value.setText(str(location_val))
                self.interest_value.setText(str(interest_val))
                
                self.market_value_degree.setText(str(market_value_degrees_dict[max_mv_class]))
                self.location_degree.setText(str(location_degrees_dict[max_location_class]))
                self.asset_degree.setText(str("{:.1f}".format(asset_degrees_dict[max_asset_class])))
                self.income_degree.setText(str(income_degrees_dict[max_income_class]))
                self.interest_degree.setText(str(interest_degrees_dict[max_interest_class]))
                
            else:
                terminateError = QMessageBox(self)
                terminateError.setWindowTitle("Terminate Error")
                terminateError.setText("All inputs must be valid. Try again!")
                terminateError.setIcon(QMessageBox.Warning)
                terminateError.setStyleSheet("""
                                     QMessageBox QLabel {
                                        background: transparent;
                                        border: none;
                                    }
                                    QMessageBox QPushButton
                                    {
                                        border: 1px solid #5a5a5a;
                                        border-radius: 4px;  
                                        min-width: 50px;  
                                        max-width: 50px; 
                                        min-height: 20px;   
                                        max-height: 20px;                                 
                                    }
                                    """) 
                terminateError.exec_()


    def showInputGraph(self):

        # print(self.select_input_graph.currentText())
        if self.select_input_graph.currentText() == 'Select Graph':
            # print("Cannot showed. Plaese select a type!\n")
            # ADD A QMESSAGEBOX    
            showingError = QMessageBox(self)
            showingError.setWindowTitle("Graph Show Error")
            showingError.setText("Please select a fuzzy variable!")
            showingError.setIcon(QMessageBox.Warning)
            showingError.setStyleSheet("""
                                     QMessageBox QLabel {
                                        background: transparent;
                                        border: none;
                                    }
                                    QMessageBox QPushButton
                                    {
                                        border: 1px solid #5a5a5a;
                                        border-radius: 4px;  
                                        min-width: 50px;  
                                        max-width: 50px; 
                                        min-height: 20px;   
                                        max-height: 20px;                                 
                                    }
                                    """) 
            showingError.exec_()        
            
        else:
            fig = Figure()
            ax = fig.add_subplot(111)
            marketvalue, location, asset, income, interest = getInputMemberships()

            match self.select_input_graph.currentText():

                case "Market Value":
                    x = np.linspace(0, 1000, 1000)

                    membership_values = {}
                    for label, func in marketvalue.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_input_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()
                    

                case "Location":
                    x = np.linspace(0, 10, 100)

                    membership_values = {}
                    for label, func in location.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_input_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()               
                    

                case "Asset":
                    x = np.linspace(0, 1000, 1000)

                    membership_values = {}
                    for label, func in asset.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_input_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()
                    

                case "Income":
                    x = np.linspace(0, 100, 1000)

                    membership_values = {}
                    for label, func in income.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_input_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()               
                    

                case "Interest":
                    x = np.linspace(0, 10, 100)

                    membership_values = {}
                    for label, func in interest.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_input_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()
                    
            # CONVERTING THE GRAPH TO PIXMAP OBJECT FOR SHOWING ON THE UI
            from io import BytesIO
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # QPixmap oluştur ve dön
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            
            self.input_graph_area.setPixmap(pixmap)
        

    # SHOW OUTPUT GRAPH ON UI
    def showOutputGraph(self):

        #print(self.select_output_graph.currentText())
        if self.select_output_graph.currentText() == 'Select Graph':
            # print("Cannot showed. Plaese select a type!\n")
            showingError = QMessageBox(self)
            showingError.setWindowTitle("Graph Show Error")
            showingError.setText("Please select a fuzzy variable!")
            showingError.setIcon(QMessageBox.Warning)
            showingError.setStyleSheet("""
                                     QMessageBox QLabel {
                                        background: transparent;
                                        border: none;
                                    }
                                    QMessageBox QPushButton
                                    {
                                        border: 1px solid #5a5a5a;
                                        border-radius: 4px;  
                                        min-width: 50px;  
                                        max-width: 50px; 
                                        min-height: 20px;   
                                        max-height: 20px;                                 
                                    }
                                    """) 
            showingError.exec_()            
            
        else:

            fig = Figure()
            ax = fig.add_subplot(111)
            house, applicant, credit = getOutputMemberships()

            match self.select_output_graph.currentText():

                case "House":
                    x = np.linspace(0, 10, 100)

                    membership_values = {}
                    for label, func in house.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_output_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()
                    

                case "Applicant":
                    x = np.linspace(0, 10, 100)

                    membership_values = {}
                    for label, func in applicant.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_output_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()
                    
                            
                case "Credit":
                    x = np.linspace(0, 500, 5000)

                    membership_values = {}
                    for label, func in credit.memberships.items():
                        membership_values[label] = [func.calculate(val) for val in x]
                        ax.plot(x, membership_values[label], label=label)

                    ax.set_xlabel(self.select_output_graph.currentText())
                    ax.set_ylabel("Membership Degree")
                    ax.legend()
                    ax.grid()

        # CONVERTING THE GRAPH TO PIXMAP OBJECT FOR SHOWING ON THE UI
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # QPixmap oluştur ve dön
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        
        self.output_graph_area.setPixmap(pixmap)


# DEFINITON OF DARK MODE        
def DarkMode(app):

    dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLabel
        {
            color: #ffffff;
        }
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox, QPushButton {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #5a5a5a;
            border-radius: 4px;
        }
        QFrame {
                background: #3c3c3c;
                border: 0.5px solid rgba(0, 0, 0, 0.5);
        }
        QPushButton:hover {
            background-color: #5c5c5c;
        }

        QComboBox QAbstractItemView { 
            background-color: #5a5a5a; 
            color: #ffffff; 
            border: 1px solid #5a5a5a;
            selection-background-color: #757575;
            selection-color: #ffffff; 
        }
    """
    app.setStyleSheet(dark_style)

def LightMode(app):

    light_style = """
        QMainWindow {
            background-color: #f5f5f5;
            color: #000000;
        }
        QLabel, QLineEdit, QComboBox, QTextEdit, QTreeView, QSpinBox, QDoubleSpinBox, QMessageBox {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        QPushButton
        {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
            border-radius: 7px;
        }
        QFrame {
                background: #edebeb;
                border: 0.5px solid rgba(0, 0, 0, 0.5);
        }
        QPushButton:hover {
            background-color: #e6e6e6;
        }

        QComboBox QAbstractItemView { 
            background-color: #ffffff; 
            color: #000000; 
            border: 1px solid #ffffff;
            selection-background-color: #ebe8e8;
            selection-color: #000000; 
        }
    """

    app.setStyleSheet(light_style)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    #DarkMode(app)
    LightMode(app)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())