#!/usr/bin/env python
#===============================================================================
# EV3 Python Loader
#   - Paul Gainer
#   - Last modified: 19/08/2016
#===============================================================================
import Tkinter, os, paramiko, py_compile, tkFont, stat
from ScrolledText import ScrolledText
from xml.etree import ElementTree
from utils import *

#===============================================================================
# Constants
#===============================================================================
#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
TEMPLATE_FILE = "template.py"
OUTPUT_FILE = "output.py"
TEMP_FILE = "temp.py"
FUNCTIONS_XML_FILE = "xml/functions.xml"
UPLOAD_IMAGE_FILE = "images/upload.png"
UPLOAD_IMAGE_HIGHLIGHTED_FILE = "images/upload_highlighted.png"
DEFINITIONS_IMAGE_FILE = "images/definitions.png"
DEFINITIONS_IMAGE_HIGHLIGHTED_FILE = "images/definitions_highlighted.png"
#-------------------------------------------------------------------------------
# Connecting to the EV3
#-------------------------------------------------------------------------------
EV3_LOCALHOST = "ev3dev.local"
EV3_USERNAME = "robot"
EV3_PASSWORD = "maker"
#-------------------------------------------------------------------------------
# Motor/Sensors
#-------------------------------------------------------------------------------
MOTOR_NAMES = ["OUTPUT_A", "OUTPUT_B", "OUTPUT_C", "OUTPUT_D"]
SENSOR_NAMES = ["INPUT_1", "INPUT_2", "INPUT_3", "INPUT_4"]
MOTOR_LEFT = 0
MOTOR_RIGHT = 1
MOTOR_HEAD = 2
SENSOR_T_LEFT = 3
SENSOR_T_RIGHT = 4
MOTOR_PORT_A = 0
MOTOR_PORT_B = 1
MOTOR_PORT_C = 2
MOTOR_PORT_D = 3
SENSOR_PORT_1 = 0
SENSOR_PORT_2 = 1
SENSOR_PORT_3 = 2
SENSOR_PORT_4 = 3
MOTOR_LEFT_DEFAULT = MOTOR_PORT_B
MOTOR_RIGHT_DEFAULT = MOTOR_PORT_C
MOTOR_HEAD_DEFAULT = MOTOR_PORT_A
SENSOR_T_LEFT_DEFAULT = SENSOR_PORT_1
SENSOR_T_RIGHT_DEFAULT = SENSOR_PORT_4
#-------------------------------------------------------------------------------
# Code colour schemes
#-------------------------------------------------------------------------------
LIGHT_BACKGROUND_COLOUR = "white"
LIGHT = {
    "code_foreground_colour": "black",
    "code_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_highlight_foreground_colour": LIGHT_BACKGROUND_COLOUR,
    "code_highlight_background_colour": "red",
    "code_keyword_foreground_colour": "medium blue",
    "code_keyword_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_comment_foreground_colour": "gray40",
    "code_comment_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_function_foreground_colour": "medium purple",
    "code_function_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_function_arg_foreground_colour": "steelblue3",
    "code_function_arg_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_ev3_function_foreground_colour": "purple",
    "code_ev3_function_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_ev3_function_arg_foreground_colour": "steelblue3",
    "code_ev3_function_arg_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_ev3_constant_foreground_colour": "orange",
    "code_ev3_constant_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_string_foreground_colour": "dark green",
    "code_string_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_string_esc_foreground_colour": "sienna1",
    "code_string_esc_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_number_foreground_colour": "blue",
    "code_number_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_tuple_foreground_colour": "brown3",
    "code_tuple_background_colour": LIGHT_BACKGROUND_COLOUR,
    "code_font_family": "monospace",
    "code_font_size": "10",
    "code_font_weight": "normal",
    "code_tuple_font_weight": "normal",
    "code_comment_font_weight": "normal",
    "code_string_font_weight": "normal",
    "code_string_esc_font_weight": "normal",
    "code_number_font_weight": "normal",
    "code_arg_font_weight": "normal",
    "code_ev3_function_font_weight": "normal",
    "code_function_font_weight": "normal",
    "error_foreground_colour": "red"
}
DARK_BACKGROUND_COLOUR =  "#303537"
DARK = {
    "code_foreground_colour": "white",
    "code_background_colour": DARK_BACKGROUND_COLOUR,
    "code_highlight_foreground_colour": "red",
    "code_highlight_background_colour": "white",
    "code_keyword_foreground_colour": "plum2",
    "code_keyword_background_colour": DARK_BACKGROUND_COLOUR,
    "code_comment_foreground_colour": "gray55",
    "code_comment_background_colour": DARK_BACKGROUND_COLOUR,
    "code_function_foreground_colour": "steelblue1",
    "code_function_background_colour": DARK_BACKGROUND_COLOUR,
    "code_function_arg_foreground_colour": "lightblue3",
    "code_function_arg_background_colour": DARK_BACKGROUND_COLOUR,
    "code_ev3_function_foreground_colour": "royalblue1",
    "code_ev3_function_background_colour": DARK_BACKGROUND_COLOUR,
    "code_ev3_function_arg_foreground_colour": "lightblue3",
    "code_ev3_function_arg_background_colour": DARK_BACKGROUND_COLOUR,
    "code_ev3_constant_foreground_colour": "orange",
    "code_ev3_constant_background_colour": DARK_BACKGROUND_COLOUR,
    "code_string_foreground_colour": "olivedrab1",
    "code_string_background_colour": DARK_BACKGROUND_COLOUR,
    "code_string_esc_foreground_colour": "sienna1",
    "code_string_esc_background_colour": DARK_BACKGROUND_COLOUR,
    "code_number_foreground_colour": "gold",
    "code_number_background_colour": DARK_BACKGROUND_COLOUR,
    "code_tuple_foreground_colour": "rosybrown1",
    "code_tuple_background_colour": DARK_BACKGROUND_COLOUR,
    "code_font_family": "monospace",
    "code_font_size": "10",
    "code_font_weight": "normal",
    "code_tuple_font_weight": "normal",
    "code_comment_font_weight": "normal",
    "code_string_font_weight": "normal",
    "code_string_esc_font_weight": "normal",
    "code_number_font_weight": "normal",
    "code_arg_font_weight": "normal",
    "code_ev3_function_font_weight": "normal",
    "code_function_font_weight": "normal",
    "error_foreground_colour": "red"
}
NONE_FOREGROUND_COLOUR = "black"
NONE_BACKGROUND_COLOUR = "white"
NONE = {
    "code_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_background_colour": NONE_BACKGROUND_COLOUR,
    "code_highlight_foreground_colour": NONE_BACKGROUND_COLOUR,
    "code_highlight_background_colour": NONE_FOREGROUND_COLOUR,
    "code_keyword_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_keyword_background_colour": NONE_BACKGROUND_COLOUR,
    "code_comment_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_comment_background_colour": NONE_BACKGROUND_COLOUR,
    "code_function_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_function_background_colour": NONE_BACKGROUND_COLOUR,
    "code_function_arg_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_function_arg_background_colour": NONE_BACKGROUND_COLOUR,
    "code_ev3_function_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_ev3_function_background_colour": NONE_BACKGROUND_COLOUR,
    "code_ev3_function_arg_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_ev3_function_arg_background_colour": NONE_BACKGROUND_COLOUR,
    "code_ev3_constant_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_ev3_constant_background_colour": NONE_BACKGROUND_COLOUR,
    "code_string_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_string_background_colour": NONE_BACKGROUND_COLOUR,
    "code_string_esc_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_string_esc_background_colour": NONE_BACKGROUND_COLOUR,
    "code_number_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_number_background_colour": NONE_BACKGROUND_COLOUR,
    "code_tuple_foreground_colour": NONE_FOREGROUND_COLOUR,
    "code_tuple_background_colour": NONE_BACKGROUND_COLOUR,
    "code_font_family": "monospace",
    "code_font_size": "10",
    "code_font_weight": "normal",
    "code_tuple_font_weight": "normal",
    "code_comment_font_weight": "normal",
    "code_string_font_weight": "normal",
    "code_string_esc_font_weight": "normal",
    "code_number_font_weight": "normal",
    "code_arg_font_weight": "normal",
    "code_ev3_function_font_weight": "normal",
    "code_function_font_weight": "normal",
    "error_foreground_colour": NONE_FOREGROUND_COLOUR
}
COLOUR_SCHEME_LIGHT = 0
COLOUR_SCHEME_NONE = 1
COLOUR_SCHEME_DARK = 2
COLOUR_SCHEMES = [LIGHT, NONE, DARK]
#-------------------------------------------------------------------------------
# GUI attributes
#-------------------------------------------------------------------------------
DEFAULT_COLOUR_SCHEME = COLOUR_SCHEME_LIGHT
DEFAULT_BACKGROUND_COLOUR = "#d9d9d9"
BUTTON_HOVER_CURSOR = "hand2"
OUTPUT_HOVER_CURSOR = "left_ptr"
ERROR_BACKGROUND_COLOUR = "#eee"
MESSAGE_FOREGROUND_COLOUR = "black"
MESSAGE_BACKGROUND_COLOUR = "#eee"
CODE_WIDTH = 80
CODE_ROWS = 26
ERROR_ROWS = 6
MESSAGE_ROWS = 6
TAB_SIZE_IN_CHARS = 4
TAB = " " * TAB_SIZE_IN_CHARS
FUNCTION_DESCRIPTION_FONT_FAMILY = "monospace"
FUNCTION_DESCRIPTION_FONT_SIZE = "10"
FUNCTION_DESCRIPTION_FONT_WEIGHT = "normal"
FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_FAMILY = "monospace"
FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_SIZE = "10"
FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_WEIGHT = "bold"
FUNCTION_DESCRIPTION_TEXT_WIDTH = 60
FUNCTION_LIST_WIDTH = 52
IMAGE_SUBSAMPLE_SIZE = 10
MOTOR_PORT_LABELS = ["A", "B", "C", "D"]
SENSOR_PORT_LABELS = ["1", "2", "3", "4"]
BUTTON_ROW_LABELS = ["LEFT MOTOR", "RIGHT MOTOR", "HEAD MOTOR", "LEFT BUMPER",
					 "RIGHT BUMPER"]
CODE_LABEL = "Code"
ERROR_LABEL = "Errors"
MESSAGE_LABEL = "Messages"
STARTUP_FILE = "test.py"
#-------------------------------------------------------------------------------
# Regex
#-------------------------------------------------------------------------------
REPLACE_TEXT = "__________"
#-------------------------------------------------------------------------------
# XML
#-------------------------------------------------------------------------------
NUM_INDENT_TABS_CODE = 3
#-------------------------------------------------------------------------------
# Replacement strings
#-------------------------------------------------------------------------------
R_MAIN = "REPLACE_ME_MAIN"
R_LEFT = "REPLACE_ME_LEFT"
R_RIGHT = "REPLACE_ME_RIGHT"
R_HEAD = "REPLACE_ME_HEAD"
R_T_LEFT = "REPLACE_ME_T_LEFT"
R_T_RIGHT = "REPLACE_ME_T_RIGHT"
R_FUNCTIONS = "REPLACE_ME_FUNCTIONS"
R_FUNCTION_LIST = "REPLACE_ME_LIST_OF_FUNCTIONS"
#-------------------------------------------------------------------------------
# Python syntax highlighting
#-------------------------------------------------------------------------------
PYTHON_KEYWORDS = ["and", "as", "assert", "break", "class", "continue",
                   "def", "del", "elif", "else", "except", "exec", "finally",
                   "for", "from", "global", "if", "import", "in", "is",
                   "lambda", "not", "or", "pass", "print", "raise", "return",
                   "try", "while", "with", "yield"]
EV3_CONSTANTS = ["LEFT", "RIGHT", "HEAD", "T_LEFT", "T_RIGHT", "COLOUR",
                 "INFRARED", "AMBER", "GREEN", "ORANGE", "RED", "YELLOW", "C_4",
                 "D_4", "E_4", "F_4", "G_4", "A_4", "B_4", "C_5"]


#===============================================================================
# Classes
#===============================================================================
#-------------------------------------------------------------------------------
# EV3PyUI - An interface to upload python files to the Lego EV3 Robot
#-------------------------------------------------------------------------------
class EV3PyGUI(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        self.function_list = self.load_functions_from_xml_file(
            FUNCTIONS_XML_FILE)
        self.build_gui()

    def build_gui(self):
        self.root = root
        root.resizable(width = False, height = False)
        self.build_menu()
        self.build_scheme_selector()
        self.build_upload_button()
        self.build_configuration_panel()
        self.build_definitions_button()
        self.build_code_panel()
        self.build_error_window()
        self.build_message_window()
        self.pack()
        self.activate_all()
        self.set_colour_scheme(COLOUR_SCHEMES[DEFAULT_COLOUR_SCHEME])
        if os.path.isfile(STARTUP_FILE):
            text = get_file_as_text(STARTUP_FILE)
            self.write_code(text)
            activate(self.input_code)
            self.refresh_code()

    def build_menu(self):
        self.menu_bar = Menu(self)
        self.menu_bar_file = Menu(self.menu_bar, tearoff = 0)
        self.menu_bar_file.add_command(
            label = "Load Program File",
            command = self.load_code_from_file)
        self.menu_bar_file.add_separator()
        self.menu_bar_file.add_command(
            label = "Exit", command = lambda: root.destroy())
        self.menu_bar.add_cascade(label = "File", menu = self.menu_bar_file)
        root.config(menu = self.menu_bar)

    def build_scheme_selector(self):
        label_frame = Frame(self.root, relief = RIDGE)
        self.scheme_selector = Scale(
            label_frame, from_ = 0, to = 2, orient = HORIZONTAL,
            showvalue = False, length = 660)
        self.scheme_selector.grid(column = 0, row = 0, columnspan = 3)
        self.scheme_selector.bind("<ButtonRelease-1>", self.update_scheme)
        self.scheme_selector.set(DEFAULT_COLOUR_SCHEME)
        Label(label_frame, text = "LIGHT").grid(sticky = W, column = 0,row = 1)
        Label(label_frame, text = "NONE").grid(column = 1, row = 1)
        Label(label_frame, text = "DARK").grid(sticky = E, column = 2, row = 1)
        label_frame.pack(side = "bottom")
        Label(root, text = "Code Colour Scheme").pack(side = "bottom")

    def update_scheme(self, event):
        self.set_colour_scheme(COLOUR_SCHEMES[self.scheme_selector.get()])

    def build_configuration_panel(self):
        self.button_vars = [IntVar() for i in range(5)]
        self.button_vars[MOTOR_LEFT].set(MOTOR_LEFT_DEFAULT)
        self.button_vars[MOTOR_RIGHT].set(MOTOR_RIGHT_DEFAULT)
        self.button_vars[MOTOR_HEAD].set(MOTOR_HEAD_DEFAULT)
        self.button_vars[SENSOR_T_LEFT].set(SENSOR_T_LEFT_DEFAULT)
        self.button_vars[SENSOR_T_RIGHT].set(SENSOR_T_RIGHT_DEFAULT)
        port_frame = Frame(self)
        port_frame_buttons = Frame(self, bd = 2, relief = SUNKEN,
                                   cursor = BUTTON_HOVER_CURSOR)
        button_labels = [MOTOR_PORT_LABELS, MOTOR_PORT_LABELS,
                         MOTOR_PORT_LABELS, SENSOR_PORT_LABELS,
                         SENSOR_PORT_LABELS]
        button_commands =\
            [lambda i = i: self.set_button_var(i) for i in range(5)]
        for row in range(5):
            for column in range(4):
                Radiobutton(port_frame_buttons,
                            text = button_labels[row][column],
                            variable = self.button_vars[row], value = column,
                            command = button_commands[row]).grid(
                    row = row, column = column)
        for i in range(5):
            Label(port_frame, text = BUTTON_ROW_LABELS[i], anchor = W,
                  width = 12, bd = 2, relief = GROOVE).grid(column = 1, row = i)
        port_frame_buttons.pack(side = RIGHT)
        port_frame.pack(side = RIGHT, expand = 1, fill = X, pady = 10, padx = 5)

    def set_button_var(self, i):
        ith_val = self.button_vars[i].get()
        if i < 3:
            other_button_indexes = [0, 1, 2]
            other_button_indexes.remove(i)
            other_var_values = [0, 1, 2, 3]
            other_var_values.remove(ith_val)
            for o in other_button_indexes:
                oth_val = self.button_vars[o].get()
                if ith_val == oth_val:
                    other_button_indexes.remove(o)
                    last_index = other_button_indexes[0]
                    other_var_values.remove(self.button_vars[last_index].get())
                    self.button_vars[o].set(other_var_values[0])
                    return
        else:
            other_button_indexes = [3, 4]
            other_button_indexes.remove(i)
            other_var_values = [0, 1, 2, 3]
            other_var_values.remove(ith_val)
            for o in other_button_indexes:
                oth_val = self.button_vars[o].get()
                if ith_val == oth_val:
                    self.button_vars[o].set(other_var_values[0])
                    return

    def build_upload_button(self):
        self.upload_img = PhotoImage(file = UPLOAD_IMAGE_FILE).subsample(
			IMAGE_SUBSAMPLE_SIZE, IMAGE_SUBSAMPLE_SIZE)
        self.upload_highlighted_img = PhotoImage(
            file = UPLOAD_IMAGE_HIGHLIGHTED_FILE).subsample(
			IMAGE_SUBSAMPLE_SIZE, IMAGE_SUBSAMPLE_SIZE)
        self.upload_button = Button(
            self, image = self.upload_img, command = self.upload_code_to_robot,
            state = DISABLED, relief = FLAT,
            activebackground = DEFAULT_BACKGROUND_COLOUR,
            cursor = BUTTON_HOVER_CURSOR)
        self.upload_button.pack(side = RIGHT, padx = 35)
        self.upload_button.bind("<Enter>", self.upload_highlight)
        self.upload_button.bind("<Leave>", self.upload_unhighlight)

    def build_definitions_button(self):
        self.definitions_img = PhotoImage(
        file = DEFINITIONS_IMAGE_FILE).subsample(IMAGE_SUBSAMPLE_SIZE,
			IMAGE_SUBSAMPLE_SIZE)
        self.definitions_highlighted_img = PhotoImage(
            file = DEFINITIONS_IMAGE_HIGHLIGHTED_FILE).subsample(
				IMAGE_SUBSAMPLE_SIZE, IMAGE_SUBSAMPLE_SIZE)
        self.definitions_button = Button(
            self, image = self.definitions_img,
            command = self.create_function_description_window,
            relief = FLAT,
            activebackground = DEFAULT_BACKGROUND_COLOUR,
            cursor = BUTTON_HOVER_CURSOR)
        self.definitions_button.pack(side = LEFT, padx = 35)
        self.definitions_button.bind("<Enter>", self.definitions_highlight)
        self.definitions_button.bind("<Leave>", self.definitions_unhighlight)

    def set_colour_scheme(self, scheme):
        font = tkFont.Font(root = self.root,
                           family = scheme["code_font_family"],
                           size = scheme["code_font_size"],
                           weight = scheme["code_font_weight"])
        tab_width_in_cm = str(font.measure("a") * 4)
        self.input_code.config(font = font, tabs = tab_width_in_cm,
                               foreground = scheme["code_foreground_colour"],
                               background = scheme["code_background_colour"])
        self.input_code.tag_configure(
            "highlight",
            foreground = scheme["code_highlight_foreground_colour"],
            background = scheme["code_highlight_background_colour"])
        self.input_code.tag_configure(
            "keyword",
            foreground = scheme["code_keyword_foreground_colour"],
            background = scheme["code_keyword_background_colour"])
        self.input_code.tag_configure(
            "comment",
            foreground = scheme["code_comment_foreground_colour"],
            background = scheme["code_comment_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_comment_font_weight"]))
        self.input_code.tag_configure(
            "function", foreground = scheme["code_function_foreground_colour"],
            background = scheme["code_function_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_function_font_weight"]))
        self.input_code.tag_configure(
            "function_arg",
            foreground = scheme["code_function_arg_foreground_colour"],
            background = scheme["code_function_arg_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_arg_font_weight"]))
        self.input_code.tag_configure(
            "ev3_function",
            foreground = scheme["code_ev3_function_foreground_colour"],
            background = scheme["code_ev3_function_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_ev3_function_font_weight"]))
        self.input_code.tag_configure(
            "ev3_function_arg",
            foreground = scheme["code_ev3_function_arg_foreground_colour"],
            background = scheme["code_ev3_function_arg_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_arg_font_weight"]))
        self.input_code.tag_configure(
            "ev3_constant",
            foreground = scheme["code_ev3_constant_foreground_colour"],
            background = scheme["code_ev3_constant_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_arg_font_weight"]))
        self.input_code.tag_configure(
            "string",
            foreground = scheme["code_string_foreground_colour"],
            background = scheme["code_string_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_string_font_weight"]))
        self.input_code.tag_configure(
            "string_esc",
            foreground = scheme["code_string_esc_foreground_colour"],
            background = scheme["code_string_esc_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_string_esc_font_weight"]))
        self.input_code.tag_configure(
            "number",
            foreground = scheme["code_number_foreground_colour"],
            background = scheme["code_number_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_number_font_weight"]))
        self.input_code.tag_configure(
            "tuple",
            foreground = scheme["code_tuple_foreground_colour"],
            background = scheme["code_tuple_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_tuple_font_weight"]))
        self.input_code.tag_configure(
            "normal",
            foreground = scheme["code_foreground_colour"],
            background = scheme["code_background_colour"],
            font = (scheme["code_font_family"],
                    scheme["code_font_size"],
                    scheme["code_font_weight"]))
        self.output_errors.configure(
            foreground = scheme["error_foreground_colour"])

    def build_code_panel(self):
        self.input_code = ScrolledText(
            root, width = CODE_WIDTH, height = CODE_ROWS, bd = 4,
            relief = RIDGE,
            state = NORMAL)
        self.input_code.pack(side = "bottom")
        self.input_code.bind("<FocusIn>", self.clear_code_highlights)
        self.input_code.bind("<KeyRelease>",
                             self.update_code_text_on_key_press)
        self.input_code.bind("<Tab>", self.insert_custom_tab)
        self.input_code.bind("<Return>", self.return_keep_indent)
        Label(root, text = CODE_LABEL).pack(side = "bottom")

    def build_error_window(self):
        self.output_errors = ScrolledText(
            root, width = 92, height = ERROR_ROWS, bd = 4, relief = RIDGE,
            background = ERROR_BACKGROUND_COLOUR,
            state = DISABLED,
            cursor = OUTPUT_HOVER_CURSOR)
        self.output_errors.pack(side = "bottom")
        Label(root, text = ERROR_LABEL).pack(side = "bottom")

    def build_message_window(self):
        self.output_messages = ScrolledText(
            root, width = 92, height = MESSAGE_ROWS, bd = 4, relief = RIDGE,
            foreground = MESSAGE_FOREGROUND_COLOUR,
            background = MESSAGE_BACKGROUND_COLOUR,
            state = DISABLED,
            cursor = OUTPUT_HOVER_CURSOR)
        self.output_messages.pack(side = "bottom")
        Label(root, text = MESSAGE_LABEL).pack(side = "bottom")

    def load_functions_from_xml_file(self, filename):
        xml_tree = ElementTree.parse(filename)
        xml_root = xml_tree.getroot()
        function_list = []
        for function in xml_root.findall("function"):
            fname = function.get("name")
            fdescription = parse_xml_text(
                function.find("fdescription").text, NUM_INDENT_TABS_CODE)
            param_list = []
            for param in function.find("parameters").findall("param"):
                param_list.append((param.get("name"),
                                   param.get("type"),
                                   param.get("min"),
                                   param.get("max"),
                                   param.get("pdescription")))
            fcode = parse_xml_text(function.find("code").text,
                                   NUM_INDENT_TABS_CODE)
            function_list.append((fname, fdescription, param_list, fcode))
        function_list = sorted(function_list, key = lambda item: item[0])
        return function_list

    def load_code_from_file(self):
        try:
            self.deactivate_all()
            file = get_file_with_dialog(self)
            if not file:
                return
            code = file.read()
            if not code or code.isspace():
                self.write_error("File \'" + file.name + "\' was empty.\n")
            else:
                self.clear_all_text()
                self.write_code(code)
            self.write_message("Loaded code from file \'" + file.name + "\'.\n")
            self.refresh_code()
        except Exception as error:
            self.write_error(str(error))
            self.write_message(
                "An error occurred while opening the file.\n")
        finally:
            self.activate_all()
            self.refresh_code()

    def upload_code_to_robot(self):
        self.upload_button.focus_set()
        self.reset_errors()
        self.reset_messages()
        self.deactivate_all()
        if self.validate_code():
            try:
                template_text = get_file_as_text(TEMPLATE_FILE)
            except Exception as error:
                self.write_error(str(error))
                self.write_message(
                    "An error occurred while opening the template Python " + \
                    "file.\n")
                self.activate_all()
                return
            try:
                template_text = self.replace_all_replacement_strings(
                    template_text)
            except Exception as error:
                self.write_error("Missing replacement string \'" + \
                                 str(error) +  "\' in file " + \
                                 TEMPLATE_FILE + "\'\n")
                self.write_message(
                    "An error occurred while opening the template Python " + \
                    "file.\n")
                self.activate_all()
                return
            try:
                self.upload_code_and_configure(template_text)
                self.write_message("File upload to EV3 Robot was successful.\n")
            except Exception as error:
                self.write_message("File upload to EV3 Robot was not " +\
                                   "successful:\n")
                self.write_error(str(error))
        self.activate_all()

    def replace_all_replacement_strings(self, text):
        for replacement_string in [R_MAIN, R_LEFT, R_RIGHT, R_HEAD, R_T_LEFT,
                                   R_T_RIGHT, R_FUNCTIONS, R_FUNCTION_LIST]:
            if replacement_string not in text:
                raise Exception(replacement_string)
        return replace_strings_in_string(
            [
                (R_MAIN, self.get_code()),
                (R_LEFT, MOTOR_NAMES[self.button_vars[MOTOR_LEFT].get()]),
                (R_RIGHT, MOTOR_NAMES[self.button_vars[MOTOR_RIGHT].get()]),
                (R_HEAD, MOTOR_NAMES[self.button_vars[MOTOR_HEAD].get()]),
                (R_T_LEFT, SENSOR_NAMES[self.button_vars[SENSOR_T_LEFT].get()]),
                (R_T_RIGHT, SENSOR_NAMES[
                    self.button_vars[SENSOR_T_RIGHT].get()]),
                (R_FUNCTION_LIST, str(self.function_list)),
                (R_FUNCTIONS, self.build_replace_me_function_list())
            ], text)

    def validate_code(self):
        code = self.get_code()
        valid = True
        if not code:
            self.write_error("There is no Python code to validate.\n")
            return False
        try:
            self.write_message(
                "Performing local code validation...\n")
            lines = [line for line in code.split("\n")
                     if line.lstrip() and (not line.lstrip().startswith("#"))]
            if not lines[0].startswith("def main():"):
                raise Exception(
                    "All code must be in the function \'main\'.\n" + \
                    "The first line of your code should read \'def main():'.\n")
            temp_file = self.create_temp_file(code)
            py_compile.compile(temp_file.name, doraise = True)
            self.write_message("Local code validation successful.\n")
            os.remove(TEMP_FILE + "c")
        except Exception as e:
            self.write_error("Local code validation failed:\n")
            self.write_error(str(e))
            valid = False
            lines = str(e).split("\n")
            activate(self.input_code)
            for line in lines:
                matches = re.findall("line ([0-9]+)", line)
                for match in matches:
                    num_lines = int(
                        self.input_code.index("end-1c").split('.')[0])
                    if num_lines == 1:
                        self.input_code.tag_add("highlight", match + ".0",
                                                END)
                    else:
                        self.input_code.tag_add("highlight", match + ".0",
                                                str(int(match) + 1) + ".0")
            deactivate(self.input_code)
        finally:
            self.delete_temp_file()
            return valid

    def upload_code_and_configure(self, text):
        try:
            temp_file = self.create_temp_file(text)
            st = os.stat(TEMP_FILE)
            os.chmod(TEMP_FILE, st.st_mode | stat.S_IEXEC)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramiko.util.log_to_file("ssh_paramiko.log")
            ssh.connect(EV3_LOCALHOST, username = EV3_USERNAME,
                        password = EV3_PASSWORD)
            sftp = ssh.open_sftp()
            sftp.put(temp_file.name, OUTPUT_FILE)
            sftp.chmod(OUTPUT_FILE, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            self.write_message("Python file \'" + OUTPUT_FILE + \
                               "\' was successfully copied to the robot.\n")
            self.write_message(
                "Validating EV3 motor/sensor configuration for file \'" + \
                OUTPUT_FILE + "\'...\n")
            stdin, stdout, stderr = ssh.exec_command("python " + OUTPUT_FILE + \
                                                     " -init")
            error = stdout.read()
            ssh.close()
            if error:
                raise Exception("EV3 motor/sensor configuration failed for " + \
                                "Python file \'" + OUTPUT_FILE + "\':\n" + \
                                error)
            else:
                self.write_message(
                    "EV3 motor/sensor configuration succeeded for Python " + \
                    "file \'" +  OUTPUT_FILE + "\'.\n")
        except Exception as error:
            self.write_error(
                "There was an error connecting to the EV3 robot:\n")
            self.write_error(str(error))
        finally:
            self.delete_temp_file()

    def build_replace_me_function_list(self):
        text = ""
        for fname, fdescription, param_list, code in self.function_list:
            text += "def " + fname + "(*args):\n"
            text += TAB + "validate_parameters(\"" + fname + "\", *args)\n"
            pcount = 0
            if len(param_list) > 0:
                text += TAB
                if len(param_list) == 1:
                    pname, type, min, max, pdescription = param_list[0]
                    text += pname + " = list(args)[0]\n"
                else:
                    for param in param_list:
                        pname, type, min, max, pdescription = param
                        text += pname
                        if pcount < (len(param_list) - 1):
                            text += ", "
                        pcount += 1
                    text += " = args\n"
            for line in code.split("\n"):
                text += TAB + line + "\n"
            text += "\n"
        return text

    def create_function_description_window(self):
        deactivate(self.definitions_button)
        self.function_description_window = \
            FunctionDescriptionWindow(self,
                                      self.function_list)
        self.function_description_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.destroy_function_description_window())

    def destroy_function_description_window(self):
        self.function_description_window.destroy()
        activate(self.definitions_button)

    def insert_custom_tab(self, event):
        self.input_code.insert(INSERT, TAB)
        return "break"

    def definitions_highlight(self, event):
        if self.definitions_button.cget("state") != DISABLED:
            self.definitions_button.config(
                image = self.definitions_highlighted_img)

    def definitions_unhighlight(self, event):
        if self.definitions_button.cget("state") != DISABLED:
            self.definitions_button.config(image = self.definitions_img)

    def upload_highlight(self, event):
        if self.upload_button.cget("state") != DISABLED:
            self.upload_button.config(image = self.upload_highlighted_img)

    def upload_unhighlight(self, event):
        if self.upload_button.cget("state") != DISABLED:
            self.upload_button.config(image = self.upload_img)

    def return_keep_indent(self, event):
        line, column = (self.input_code.index(INSERT).split("."))
        leading_whitespace = re.match(r"\s*", self.input_code.get(
                line + ".0", line + ".end")).group()
        self.input_code.insert(INSERT, "\n" + leading_whitespace)
        return "break"

    def clear_code_highlights(self, event):
        self.input_code.tag_remove("highlight", "1.0", END)

    def update_code_text_on_key_press(self, event):
        self.refresh_code()

    def refresh_code(self):
        code = self.get_code()
        if code.isspace():
            deactivate(self.upload_button)
        else:
            activate(self.upload_button)
        self.clear_all_tags()
        self.highlight_words(
            code, PYTHON_KEYWORDS, {1: "keyword"},
            "(^|(?<![a-zA-Z0-9_]))(" + REPLACE_TEXT + ")"
            "($|(?![a-zA-Z0-9_]))", [1], False)
        self.highlight_words(
            code, ["[a-zA-Z0-9_]+"], {1: "function", 3: "function_arg"},
            "(^|(?<![a-zA-Z0-9_]))(" + REPLACE_TEXT + ")"
            "(\()([^\n()]*)(\))", [1, 3], False)
        self.highlight_words(
            code, ["(^|(?<![a-zA-Z0-9_]))(\()(.*)(\))"],
            {2 : "tuple"}, REPLACE_TEXT, [2], False)
        self.highlight_words(
            code, [function[0] for function in self.function_list],
            {1: "ev3_function", 3: "ev3_function_arg"},
             "(^|(?<![a-zA-Z0-9_]))(" + REPLACE_TEXT + ")"
            "(\()(.*)(\))", [1, 3], False)
        self.highlight_words(
            code, EV3_CONSTANTS, {1: "ev3_constant"},
            "(^|(?<![a-zA-Z0-9_]))(" + REPLACE_TEXT + ")"
            "($|(?![a-zA-Z0-9_]))", [1], False)
        self.highlight_words(
            code, ["(^|(?<![" + r"\\" + "a-zA-Z0-9_]))"
                   "(([0-9]+[0-9]*)(\.?)[0-9]*)"
                   "($|(?![a-zA-Z0-9_]))"], {1: "number"},
            REPLACE_TEXT, [1], False)
        self.highlight_words(code, ["(,)"], {0: "normal"},
                             REPLACE_TEXT, [0], False)
        self.highlight_words(code, ["(\(|\))"], {0: "normal"},
                             REPLACE_TEXT, [0], False)
        self.highlight_words(
            code, ["(((\")([^\n\"]*)(\"))|((\')([^\n\']*)(\')))"],
            {0 : "string"}, REPLACE_TEXT, [0], False)
        self.highlight_words(code, ["(#.*[\n|$])"], {0: "comment"},
                             REPLACE_TEXT, [0], True)
        self.input_code.tag_raise("tuple")
        self.input_code.tag_raise("function_arg")
        self.input_code.tag_raise("function")
        self.input_code.tag_raise("ev3_function_arg")
        self.input_code.tag_raise("ev3_function")
        self.input_code.tag_raise("ev3_constant")
        self.input_code.tag_raise("number")
        self.input_code.tag_raise("keyword")
        self.input_code.tag_raise("normal")
        self.input_code.tag_raise("string")
        self.input_code.tag_raise("comment")
        self.input_code.tag_raise("highlight")

    def clear_all_tags(self):
        self.remove_tag("function_arg")
        self.remove_tag("tuple")
        self.remove_tag("function")
        self.remove_tag("ev3_function_arg")
        self.remove_tag("ev3_function")
        self.remove_tag("ev3_constant")
        self.remove_tag("number")
        self.remove_tag("keyword")
        self.remove_tag("normal")
        self.remove_tag("string")
        self.remove_tag("string_esc")
        self.remove_tag("comment")

    def remove_tag(self, tag):
        self.input_code.tag_remove(tag, "1.0", END)

    def highlight_words(self, text, words, group_tag_dictionary,
                        pattern, groups, to_end_of_line):
        for word in words:
            it = re.finditer(
                pattern.replace(REPLACE_TEXT, word), text)
            for match in it:
                start, end = match.start(), match.end()
                match_groups = match.groups()
                col_offset = 0
                for i in range(len(match_groups)):
                    if match_groups[i] != None:
                        length = len(match_groups[i])
                        if i in groups:
                            start_index, end_index =\
                                self.get_tkinter_text_indexes(
                                    start + col_offset,
                                    start + col_offset + length,
                                    to_end_of_line)
                            self.input_code.tag_add(
                                group_tag_dictionary[i], start_index, end_index)
                        col_offset += length

    def get_tkinter_text_indexes(self, start, end, to_end_of_line):
        code = self.get_code()
        start_row = 1 + code[0:end - 1].count("\n")
        last_linebreak = code[0:end - 1].rfind("\n")
        if last_linebreak == -1:
            start_col = start
        else:
            start_col = start - last_linebreak - 1
        start_index = "%s.%s" % (start_row, start_col)
        end_index = "%s.%s" % (
            start_row, (start_col + (end - start), "end")[to_end_of_line])
        return start_index, end_index

    def deactivate_all(self):
        deactivate(self.upload_button)
        deactivate(self.input_code)
        self.menu_bar.entryconfig("File", state = DISABLED)
        self.root.update_idletasks()

    def activate_all(self):
        if self.get_code().isspace():
            deactivate(self.upload_button)
        else:
            activate(self.upload_button)
        activate(self.input_code)
        self.menu_bar.entryconfig("File", state = NORMAL)
        self.root.update_idletasks()

    def clear_all_text(self):
        self.reset_messages()
        self.reset_errors()
        self.reset_code()

    def reset_messages(self):
        activate(self.output_messages)
        clear_text(self.output_messages)
        deactivate(self.output_messages)

    def reset_errors(self):
        activate(self.output_errors)
        clear_text(self.output_errors)
        deactivate(self.output_errors)

    def reset_code(self):
        activate(self.input_code)
        clear_text(self.input_code)
        deactivate(self.input_code)

    def write_code(self, text):
        activate(self.input_code)
        self.input_code.insert(END, text)
        deactivate(self.input_code)
        self.root.update_idletasks()

    def write_message(self, text):
        activate(self.output_messages)
        self.output_messages.insert(END, text)
        deactivate(self.output_messages)
        self.root.update_idletasks()

    def write_error(self, text):
        activate(self.output_errors)
        self.output_errors.insert(END, text)
        deactivate(self.output_errors)
        self.root.update_idletasks()

    def create_temp_file(self, text):
        temp_file = open(TEMP_FILE, "w")
        temp_file.write(text)
        temp_file.close()
        return temp_file

    def delete_temp_file(self):
        if os.path.isfile(TEMP_FILE):
            os.remove(TEMP_FILE)

    def get_code(self):
        return self.input_code.get("1.0", END)


#-------------------------------------------------------------------------------
# FunctionDescriptionWindow - A window that displays information about each of
# the functions that are defined in the given list
#-------------------------------------------------------------------------------
class FunctionDescriptionWindow(Toplevel):
    def __init__(self, root, function_list):
        Toplevel.__init__(self, root)
        self.root = root
        self.function_list = function_list
        self.wm_title("Function Descriptions")
        self.resizable(width = False, height = False)
        self.build_gui()

    def build_gui(self):
        font = tkFont.Font(root = self.root,
                           family = FUNCTION_DESCRIPTION_FONT_FAMILY,
                           size = FUNCTION_DESCRIPTION_FONT_SIZE,
                           weight = FUNCTION_DESCRIPTION_FONT_WEIGHT)
        tab_width_in_cm = str(font.measure("a") * 4)
        self.descriptions = Text(self,
                                 width = FUNCTION_DESCRIPTION_TEXT_WIDTH,
                                 height = 20, bd = 4, relief = RIDGE,
                                 font = font,
                                 foreground = "black",
                                 background = "#eee",
                                 state = DISABLED,
                                 cursor = "left_ptr",
                                 tabs = tab_width_in_cm)
        self.descriptions.pack(side = "bottom")
        self.descriptions.tag_configure(
            "function_name",
            font = (
                FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_FAMILY,
                FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_SIZE,
                FUNCTION_DESCRIPTION_HIGHLIGHT_FONT_WEIGHT))
        Label(self, text = "Description").pack(side = "bottom")
        scrollbar = Scrollbar(self, orient = VERTICAL)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.listbox = Listbox(self, width = FUNCTION_LIST_WIDTH)
        self.listbox.pack(side = LEFT, fill = Y)
        scrollbar.config(command = self.listbox.yview)
        self.listbox.config(yscrollcommand = scrollbar.set)
        for function in self.function_list:
            fname, fdescription, param_list, fcode = function
            self.listbox.insert(END, fname)
        self.listbox.pack(side = "bottom")
        self.listbox.bind("<<ListboxSelect>>", self.definition_select)
        Label(self, text = "Function").pack(
            side = "bottom")

    def definition_select(self, event):
        index = list(self.listbox.curselection())[0]
        fname, fdescription, param_list, code = self.function_list[index]
        text = fname + "("
        pcount = 0
        for param in param_list:
            pname, type, min, max, pdescription = param
            text += pname
            if pcount < (len(param_list) - 1):
                text += ", "
            pcount += 1
        text += ")\n\n"
        for param in param_list:
            pname, type, min, max, pdescription = param
            type = eval(type)
            min = eval(min)
            max = eval(max)
            text += pname + ": " + pdescription + " (" + type.__name__ + ")"
            if type == int:
                if (min != None) & (max != None):
                    text += " [" + str(min) + "-" + str(max) + "]"
                elif min != None:
                    text += " " + u"\u2265" + " " + str(min)
                elif max != None:
                    text += " " + u"\u2264" + " " + str(max)
            text += "\n"
        if len(param_list) > 0:
            text += "\n"
        text += fdescription
        activate(self.descriptions)
        clear_text(self.descriptions)
        self.descriptions.insert(END, text)
        self.descriptions.tag_add("function_name", "1.0",
                                  "1.end")
        line = 3
        for param in param_list:
            pname, type, min, max, pdescription = param
            self.descriptions.tag_add("function_name", str(line) + ".0",
                                      str(line) + "." + str(len(pname)))
            line += 1
        deactivate(self.descriptions)

#===============================================================================
# main
#===============================================================================
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.wm_title("EV3 Python Loader")
    EV3PyGUI(root).pack()
    root.mainloop()
