#===============================================================================
# some reusable functions
#   - Paul Gainer
#   - Last modified: 15/08/2016
#===============================================================================
import tkFileDialog
from Tkinter import *

def parse_xml_text(text, num_tabs):
    string = ""
    line_list = [line for line in list(text.split("\n"))
                 if line and (not line.isspace())]
    icount = 1
    for line in line_list:
        num_extra_tabs = re.match(r"\t*", line).group().count("\t") - num_tabs
        string += "\t" * num_extra_tabs + line.strip()
        if icount < len(line_list):
            string = string + "\n"
        icount = icount + 1
    return string

def are_substrings_of_string(strings, string):
    for s in strings:
        if s not in string:
            return False
    return True

def replace_strings_in_string(strings, string):
    for original, new in strings:
        string = string.replace(original, new)
    return string

def get_file_as_text(filename):
    file = open(filename, 'r')
    file_text = file.read()
    file.close()
    return file_text

def get_file_with_dialog(root):
    file = tkFileDialog.askopenfile(mode = "r", defaultextension = ".py",
                                    filetypes = [("python files", ".py")],
                                    parent = root,
                                    title = "Please select your python file...")
    return file

def deactivate(component):
    component.config(state = DISABLED)

def activate(component):
    component.config(state = NORMAL)

def clear_text(component):
    component.delete("1.0", END)

