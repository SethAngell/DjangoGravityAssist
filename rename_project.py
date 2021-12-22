import os
import glob
import sys
from collections import namedtuple
import shutil
import pathlib
import subprocess

# Make things pretty
# Thanks https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

moon = u'\U0001F315'
rocket = u'\U0001F680'
stars = u'\U00002728'
smile = u'\U0001F604'
wave = u'\U0001F44B'

def generate_rich(text, bold=False, selected_color=None):

    if selected_color != None:
        if bold:
            return(f'{color.BOLD}{selected_color}{text}{color.END}')
        else:
            return(f'{selected_color}{text}{color.END}')
    else:
        if bold:
            return(f'{color.BOLD}{text}{color.END}')
        else:
            return(f'{text}')

names = namedtuple('conjoined', 'seperated')


# Files and directories which need altering
files_to_alter = ['app/manage.py', 'app/pytest.ini', 'app/DjangoGravityAssist/asgi.py', 
        'app/DjangoGravityAssist/settings.py', 'app/DjangoGravityAssist/wsgi.py',
        'docker-compose.yaml', '.ci/docker-compose.yaml', '.github/workflows/build.yml']

dirs_to_alter = ['app/DjangoGravityAssist']

dirs_to_delete = glob.glob('app/*/migrations')
dirs_to_delete.extend(glob.glob('app/*/__pycache__'))
dirs_to_delete.append('.git')

files_to_delete = ['app/db.sqlite3', 'readme.md']



# Introduce concept to the user and give credit to Will Vincent
print(f'\n{generate_rich("Welcome to DjangoGravityAssist {} {} {}".format(moon, rocket, stars), True) : <80}')
print(f'{"A template for new django apis" : <80}')
print("\nThis project wouldn't be possible without the William Vincent's tutorials")
print("You should really check him out: {}".format(generate_rich("https://wsvincent.com", True, color.GREEN)))
print("\nThe project beneath the /app directory will run as is")
print("or we can do some renaming to make the project yours!")

print("\n{}".format(generate_rich("This script can regenerate the application and create a fresh project of your choice", True)))
result = input("Would you like to proceed? [y/N]: ")

if result not in ('y', 'Y', 'yes', 'Yes'):
    print(f'\n{generate_rich("Have fun building!", True)}{smile}{wave}')
    sys.exit(0)


# Handle all of the root directory questions
print("\n" + generate_rich("We're going to build this project in a new directory", True))
valid_directory = False
new_proj_directory = None
while not valid_directory:
    potential_dir = input("Where would you like to create your new project? [relative or full path]: ")

    if not os.path.exists(potential_dir):
        print(generate_rich("Hmmm, that path doesn't seem to exist. Let's try again!", True, color.RED))
    else:
        valid_directory = True
        new_proj_directory = pathlib.Path(potential_dir)

root_dir = input("Would you like to create your project at the root of this directory? [y/N]: ")
if root_dir not in ('y', 'Y', 'yes', 'Yes'):
    sub_dir_name = input("What should we name the subdirectory for your project?: ")
    new_proj_directory = new_proj_directory / sub_dir_name

# Get new project name
good_name = False
project_name = None
print(generate_rich("\nNow that that's square away, we need to name the project", True))

while not good_name:
    new_name = input("What would you like to name your project?: ")
    name_elements = new_name.split(" ")
    conjoined_name = "".join([(item[0].upper() + item[1:])  for item in name_elements])
    seperated_name = "_".join([item.lower() for item in name_elements])
    print(f'Perfect. Your app will be named {generate_rich(new_name, True, color.GREEN)}' \
            f' and be stored as {generate_rich(conjoined_name, True, color.GREEN)}' \
            f' and {generate_rich(seperated_name, True, color.GREEN)}')
    accepted = input("Does this name work? Or would you like to choose a different one? [y/N]: ")
    
    if accepted not in ('y', 'Y', 'Yes', 'yes'):
        print("No worries, let's try again")
    else:
        good_name = True
        project_name = (conjoined_name, seperated_name)

print(generate_rich("Beginning project duplication process"))
# Migrate project to new folder
print(f'\n{generate_rich("1. Perfect, now we will copy over to your new directory", True, color.GREEN)}')
try:
    shutil.copytree('.', new_proj_directory)
except Exception as e:
    print("Oh No! We were unable to copy the project over")
    print(f'We captured this error: {e}')
    print(generate_rich("Sorry!", True, color.RED))
    sys.exit(1)

# Delete all the unneeded files
print(f'{generate_rich("2. Deleting soon to be invalidated files and directories", True, color.GREEN)}')
for dir in dirs_to_delete:
    targeted_dir = new_proj_directory / dir
    shutil.rmtree(targeted_dir)

for t_file in files_to_delete:
    targeted_file = new_proj_directory / t_file
    os.remove(targeted_file)

# Rename application to match new name
print(f'{generate_rich("3. Renaming application and files to match new name", True, color.GREEN)}')

for t_file in files_to_alter:
    proper_path = new_proj_directory / t_file

    with open(proper_path, 'r') as ifile:
        data =  ifile.read()
    
    data = data.replace("DjangoGravityAssist", project_name[0])
    data = data.replace("django_gravity_assist", project_name[1])

    with open(proper_path, 'w') as ifile:
        ifile.write(data)

for dir in dirs_to_alter:
    proper_path = new_proj_directory / dir
    new_path = new_proj_directory / 'app' / project_name[0]
    os.rename(proper_path, new_path)

# Initializing models and making migrations
print(f'{generate_rich("4. Initalizing models and making new migrations", True, color.GREEN)}')
os.chdir(new_proj_directory / 'app')

process = subprocess.Popen(['docker-compose', 'up', '-d', '--build'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

stdout, stderr = process.communicate()
print(stdout, stderr)

process = subprocess.Popen(['docker-compose', 'exec', 'api', 'python',
                            'manage.py', 'makemigrations', 'users'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

stdout, stderr = process.communicate()
print(stdout, stderr)

process = subprocess.Popen(['docker-compose', 'exec', 'api', 'python',
                            'manage.py', 'makemigrations'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

stdout, stderr = process.communicate()
print(stdout, stderr)

process = subprocess.Popen(['docker-compose', 'exec', 'api', 'python',
                            'manage.py', 'migrate'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

stdout, stderr = process.communicate()
print(stdout, stderr)







