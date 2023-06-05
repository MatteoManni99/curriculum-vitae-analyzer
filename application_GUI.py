import spacy
import openai
import fitz
import zipfile

def from_path_to_text(cv_path):
    fitz_doc = fitz.open(cv_path)
    fitz_text = ""
    for page in fitz_doc:
        fitz_text += page.get_text()

    fitz_tx = " ".join(fitz_text.split('\n'))  # for removing the next line character '/n'
    return(fitz_tx)


def gpt_query(request, cv):
    request = ". " + request
    query = cv + request

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )

    return completion.choices[0].message.content


def load_nlp_model():
    global nlp_model
    nlp_model = spacy.load('model-last')
    print(nlp_model)


def initilize_cv_elaborator():
    #with zipfile.ZipFile('model-last.zip', 'r') as zip_ref:
    #    zip_ref.extractall('model-last')
    #load_nlp_model()
    openai.api_key = "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"


def compute_entities(cv_path):
    return ''


def compute_softskills(cv_path):
    cv = from_path_to_text(cv_path)
    softskills = gpt_query('List me the softskills', cv)
    return softskills


def compute_weaknesses(cv_path):
    cv = from_path_to_text(cv_path)
    weaknesses = gpt_query('What are the areas of this cv that can be improved?', cv)
    return weaknesses

def compute_evaluation(cv_path):
    cv = from_path_to_text(cv_path)
    evaluation = gpt_query('do Summative evaluation of this CV', cv)
    return evaluation

import tkinter as tk
import time
from tkinter import ttk, filedialog
import os
import tkinter.font as font

initilize_cv_elaborator()

root = tk.Tk()
root.geometry('1650x700+50+50')
root.title('Curriculum Vitae Smart Reviewer')
root['background']='#F9DCA8'
root.resizable(0, 0)
root.attributes('-topmost', 1)
#root.iconbitmap('./assets/icon.ico')
myFont = "Calibri 13 bold"
myFont2 = font.Font(size=15)

def select_directory():
    global cv_directory
    global cv_list_box
    cv_directory = filedialog.askdirectory(title='Select CVs Directory')
    cv_list = os.listdir(cv_directory)
    label_cv_list.config()
    for cv in cv_list:
        cv_list_box.insert(tk.END, cv)


#button
label_cv_selected = tk.Label(root, fg='#f00', borderwidth=1, relief="solid")
label_cv_selected['font'] = myFont2

directory_button = tk.Button(root, text = 'Select CVs Directory', command = select_directory)
directory_button['font'] = myFont
directory_button.place(x=10, y=10)

'''#entities
label_entities = tk.Label(root, text='Entities:',  bg="#6FAFE7", borderwidth=5)
label_entities['font'] = myFont
label_entities.place(x=400, y=60)

text_entities = tk.Text(root, width=50, height=30)
text_entities.place(y=100, x=230)
text_entities['font'] = myFont
text_entities['state'] = 'disabled'
'''

label_evaluation = tk.Label(root, text='Evaluation:',  bg="#6FAFE7", borderwidth=5)
label_evaluation['font'] = myFont
label_evaluation.place(x=400, y=60)

text_evaluation = tk.Text(root, width=50, height=30)
text_evaluation.place(y=100, x=230)
text_evaluation['font'] = myFont
text_evaluation['state'] = 'disabled'

#weaknesses
label_weaknesses = tk.Label(root, text='Weaknesses:', borderwidth=5, bg="#6FAFE7")
label_weaknesses['font'] = myFont
label_weaknesses.place(y=60, x=900)

text_weaknesses = tk.Text(root, width=50, height=30)
text_weaknesses.place(y=100, x=700)
text_weaknesses['font'] = myFont
text_weaknesses['state'] = 'disabled'

#softskills
label_softskills = tk.Label(root, text='Soft Skills:', borderwidth=5, bg="#6FAFE7")
label_softskills['font'] = myFont
label_softskills.place(y=60, x=1350)

text_softskills = tk.Text(root, width=50, height=30)
text_softskills.place(y=100, x=1170)
text_softskills['font'] = myFont
text_softskills['state'] = 'disabled'


#listbox
label_cv_list = tk.Label(root, text='CVs:', borderwidth=5, bg="#6FAFE7")
label_cv_list['font'] = myFont
label_cv_list.place(x=75, y=60)

cv_list_box = tk.Listbox(
    root,
    width=20, height=20,
    selectmode=tk.EXTENDED)
cv_list_box['font'] = myFont
cv_list_box.place(x=10, y=100)

def items_selected(event):
    #get selected index
    selected_indices = cv_list_box.curselection()
    #get selected items
    cv_selected = cv_list_box.get(selected_indices)
    #msg = f'You selected: {selected_langs}'

    #set selected cv label
    label_cv_selected.place(x=230, y=10)
    label_cv_selected.config(text=cv_selected)

    global cv_directory
    complete_cv_path = cv_directory + '/' + cv_selected

    '''#fill entities
    entities = cumpute_entities(complete_cv_path)
    text_entities['state'] = 'normal'
    text_entities.delete('1.0', tk.END)
    text_entities.insert('1.0', entities)
    text_entities['state'] = 'disabled'
    '''

    #fill evaluation
    evaluation = compute_evaluation(complete_cv_path)
    text_evaluation['state'] = 'normal'
    text_evaluation.delete('1.0', tk.END)
    text_evaluation.insert('1.0', evaluation)
    text_evaluation['state'] = 'disabled'

    #fill weakness
    weaknesses = compute_weaknesses(complete_cv_path)
    text_weaknesses['state'] = 'normal'
    text_weaknesses.delete('1.0', tk.END)
    text_weaknesses.insert('1.0', weaknesses)
    text_weaknesses['state'] = 'disabled'

    #fill soft-skills
    softskills = compute_softskills(complete_cv_path)
    text_softskills['state'] = 'normal'
    text_softskills.delete('1.0', tk.END)
    text_softskills.insert('1.0', softskills)
    text_softskills['state'] = 'disabled'
    

cv_list_box.bind('<<ListboxSelect>>', items_selected)


#ctypes try to fix the blur UI
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()