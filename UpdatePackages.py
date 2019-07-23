import os
import threading
import itertools

from PyInquirer import prompt, style_from_dict
from time import sleep

def worker():
    
    msg = 'Procesando paquetes... '

    ciclo = itertools.cycle(r'\|/-')

    #for i in range(1, 200):
    #    print(msg + next(ciclo) if i+1 < 200 else msg + "done", end='\r')
    #    sleep(0.1)

    while getattr(t, "do_exec", True):
        print(msg + next(ciclo), end='\r')
        sleep(0.1)

t = threading.Thread(target=worker)
t.start()

# Get packages outdates
CMD = 'pip list --outdated --format=freeze > requeriments.txt'
os.system(CMD)

t.do_exec = False

# Read in the file
with open('requeriments.txt', 'r') as file:
    # get content
    filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('==', '>=')

# close
file.close()

# Read in the file
with open('requeriments.txt', 'r') as file:
    filedata = file.read().split('\n')

# empty array
dicts = []

# generate list packages
for line in filedata:
    if line.strip():
        dicts.append({'name': line})

if dicts:

    # Generate the questions
    questions = [
        {
            'type': 'checkbox',
            'qmark': '>',
            'message': 'Paquetes por actualizar',
            'name': 'packages',
            'choices': dicts
        }
    ]

    answers = prompt(questions)

    with open('requeriments.txt', 'w') as file:
        for item in answers['packages']:
            file.write("{}\n".format(item))

    if answers['packages']:

        # Exec update
        CMD = 'pip install -r requeriments.txt --upgrade'
        os.system(CMD)

    else:

        print('\nNo se ha seleccionado nada o el archivo de requerimientos esta vacio.')

else:

    print('\nNo se encontraron paquetes por actualizar.')