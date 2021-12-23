import glob
import os
import pathlib
import shutil
import subprocess
import sys


# Make things pretty
# Thanks https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# Emoji Unicode
moon = "\U0001F315"
rocket = "\U0001F680"
stars = "\U00002728"
smile = "\U0001F604"
wave = "\U0001F44B"


def generate_rich(text, bold=False, selected_color=None):

    if selected_color != None:
        if bold:
            return f"{color.BOLD}{selected_color}{text}{color.END}"
        else:
            return f"{selected_color}{text}{color.END}"
    else:
        if bold:
            return f"{color.BOLD}{text}{color.END}"
        else:
            return f"{text}"


def standard_error_message(error_message):
    print("Weird, We just encountered an error we never expected to see")
    print("To keep your machine safe, we'll terminate here")
    print(generate_rich("Sorry :(", True, color.RED))
    print(
        "\n\nIf you don't mind - Please screenshot the following block and open a github issue containing it"
    )
    print(f"Error: {error_message}")
    sys.exit(1)


# Files and directories which need altering
files_to_alter = [
    "app/manage.py",
    "app/pytest.ini",
    "app/DjangoGravityAssist/asgi.py",
    "app/DjangoGravityAssist/settings.py",
    "app/DjangoGravityAssist/wsgi.py",
    "app/Dockerfile.prod"
    "docker-compose.yaml",
    ".ci/docker-compose.yaml",
    ".github/workflows/build.yml",
]

dirs_to_alter = ["app/DjangoGravityAssist"]

dirs_to_delete = [".git"]
dirs_to_delete.extend(glob.glob("app/*/migrations"))
dirs_to_delete.extend(glob.glob("app/*/__pycache__"))

files_to_delete = [
    "app/db.sqlite3",
    "readme.md",
    "rename_project.py",
    "demo.gif",
    "ManualRenameToDos.md",
]


# Introduce concept to the user and give credit to Will Vincent
print(
    f'\n{generate_rich("Welcome to DjangoGravityAssist {} {} {}".format(moon, rocket, stars), True) : <80}'
)
print(f'{"A template for new django apis" : <80}')

print("\nThis project wouldn't be possible without William Vincent's tutorials")
print(
    "You should really check him out: {}".format(
        generate_rich("https://wsvincent.com", True, color.GREEN)
    )
)

print("\nThe project beneath the /app directory will run as is")
print(
    "or we can generate a fresh copy in a new directory personalized just for you and your project"
)


print(
    f'\n{generate_rich("This script will create a copy of the project in /app and make some config changes based off your input",True,)}'
)
result = input("Would you like to proceed? [y/N]: ")

if result not in ("y", "Y", "yes", "Yes"):
    print(f'\n{generate_rich("Have fun building!", True)}{smile}{wave}')
    sys.exit(0)


# Handle all of the root directory questions
print(
    "\n"
    + generate_rich(
        "Perfect! We're going to build this project in a new directory", True
    )
)

valid_directory = False
new_proj_directory = None
while not valid_directory:
    potential_dir = input(
        "Where would you like to create your new project? [relative or full path]: "
    )

    if not os.path.exists(potential_dir):
        print(
            generate_rich(
                "Hmmm, that path doesn't seem to exist. Let's try again!",
                True,
                color.RED,
            )
        )
    else:
        valid_directory = True
        new_proj_directory = pathlib.Path(potential_dir)

root_dir = input(
    f"Would you like to create your project at the root of this directory ({new_proj_directory})? [y/N]: "
)
if root_dir not in ("y", "Y", "yes", "Yes"):
    sub_dir_name = input("What should we name the subdirectory for your project?: ")
    new_proj_directory = new_proj_directory / sub_dir_name

print(
    f"We will create your new project at {generate_rich(new_proj_directory, True, color.GREEN)}"
)


# Get new project name
good_name = False
project_name = None
print(
    generate_rich("\nNow that that's squared away, we need to name the project", True)
)

while not good_name:
    new_name = input("What would you like to name your project?: ")
    name_elements = new_name.split(" ")
    conjoined_name = "".join([(item[0].upper() + item[1:]) for item in name_elements])
    seperated_name = "_".join([item.lower() for item in name_elements])
    print(
        f"Perfect. For project naming purposes we will use 2 variations of your name:"
        f" {generate_rich(conjoined_name, True, color.GREEN)} and {generate_rich(seperated_name, True, color.GREEN)}"
    )
    accepted = input(
        "Does this name work? Or would you like to choose a different one? [y/N]: "
    )

    if accepted not in ("y", "Y", "Yes", "yes"):
        print("No worries, let's try again")
    else:
        good_name = True
        project_name = (conjoined_name, seperated_name)

user_commands = []
print(generate_rich("\nBeginning project generation process", True))
# Migrate project to new folder
print(
    f'{generate_rich("1. Copying template project over to new directory", True, color.GREEN)}'
)
try:
    shutil.copytree(".", new_proj_directory, ignore=shutil.ignore_patterns("app/env"))
except (PermissionError, NotADirectoryError, FileExistsError) as e:
    print("Oh No! We were unable to copy the project over")
    print(f"We captured this error: {e}")
    print(generate_rich("Sorry!", True, color.RED))
    sys.exit(1)
except Exception as e:
    standard_error_message(e)

# Delete all the unneeded files
print(
    f'{generate_rich("2. Deleting soon to be invalidated files and directories", True, color.GREEN)}'
)
try:
    for dir in dirs_to_delete:
        targeted_dir = new_proj_directory / dir
        shutil.rmtree(targeted_dir)

    for t_file in files_to_delete:
        targeted_file = new_proj_directory / t_file
        os.remove(targeted_file)
except (
    FileNotFoundError,
    FileExistsError,
    IsADirectoryError,
    NotADirectoryError,
    PermissionError,
) as e:
    print("Oops, it looks like we weren't able to delete all of the files we needed to")
    print("It's no worries, just means some of the automation magic won't work")
    print(
        "We'll leave a list of files to manually delete at the root of your new directory"
    )
    print(generate_rich("Sorry :(", True, color.RED))

    user_commands.append("Files and Directories to delete before use:")
    for file in files_to_delete:
        user_commands.append(f"- [ ] {file}")
    for dir in dirs_to_delete:
        user_commands.append(f"- [ ] {dir}")
except Exception as e:
    standard_error_message(e)


# Rename application to match new name
print(
    f'{generate_rich("3. Renaming application and files to match new name", True, color.GREEN)}'
)

try:
    for t_file in files_to_alter:
        proper_path = new_proj_directory / t_file

        with open(proper_path, "r") as ifile:
            data = ifile.read()

        data = data.replace("DjangoGravityAssist", project_name[0])
        data = data.replace("django_gravity_assist", project_name[1])

        with open(proper_path, "w") as ifile:
            ifile.write(data)

    for dir in dirs_to_alter:
        proper_path = new_proj_directory / dir
        new_path = new_proj_directory / "app" / project_name[0]
        os.rename(proper_path, new_path)
except (
    FileNotFoundError,
    FileExistsError,
    IsADirectoryError,
    NotADirectoryError,
    PermissionError,
) as e:
    print(
        "Oops, it looks like we weren't able to change all of the text we needed to within the project"
    )
    print("It's no worries, just means some of the automation magic won't work")
    print(
        "We'll leave a list of files and directories to manually delete at the root of your new directory"
    )
    print(generate_rich("Sorry :(", True, color.RED))

    user_commands.append(
        f"For the following files, find and replace all instances of DjangoGravityAssist and django_gravity_assist to {project_name[0]} or {project_name[1]}"
    )
    for file in files_to_alter:
        user_commands.append(f"- [ ] {file}")

    user_commands.append(
        f"For the following directories, find and replace all instances of DjangoGravityAssist and django_gravity_assist to {project_name[0]} or {project_name[1]}"
    )
    for dir in files_to_delete:
        user_commands.append(f"- [ ] {dir}")
except Exception as e:
    standard_error_message(e)


# Initializing models and making migrations
print(
    f'{generate_rich("4. Initalizing models and making new migrations", True, color.GREEN)}'
)

os.chdir(new_proj_directory / "app")

docker_commands = [
    ["docker-compose", "up", "-d", "--build"],
    ["docker-compose", "exec", "api", "python", "manage.py", "makemigrations", "users"],
    ["docker-compose", "exec", "api", "python", "manage.py", "makemigrations"],
    ["docker-compose", "exec", "api", "python", "manage.py", "migrate"],
]

error_encountered = False
for command in docker_commands:
    if error_encountered:
        user_commands.append(f'- [ ] {" ".join(command)}')
    else:
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = process.communicate()
        except (PermissionError, subprocess.CalledProcessError) as e:
            print("Oops, it looks like our Docker calls failed")
            print("It's no worries, just means some of the automation magic won't work")
            print(
                "We'll leave some docker commands to run at the root of your directory"
            )
            print(generate_rich("Sorry :(", True, color.RED))

            user_commands.append(
                "After all file changes and deletions are complete. Run these commands:"
            )
            user_commands.append(f'- [ ] {" ".join(command)}')
            error_encountered = True
        except Exception as e:
            standard_error_message(e)

# Recreate a git directory
print(f'{generate_rich("5. Creating fresh git repo", True, color.GREEN)}')
os.chdir("..")

try:
    process = subprocess.Popen(
        ["git", "init", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
except (PermissionError, subprocess.CalledProcessError) as e:
    print("Oops, it looks like our git initialization call failed")
    print("It's no worries, just means some of the automation magic won't work")
    print("We'll add that to the ToDo list")
    print(generate_rich("Sorry :(", True, color.RED))

    user_commands.append("Once the project is ready. Run this command:")
    user_commands.append(f'- [ ] {" ".join(["git", "init", "."])}')
except Exception as e:
    standard_error_message(e)

# Recreate a git directory
print(f'{generate_rich("6. Creating a new Readme", True, color.GREEN)}')
try:
    readme_contents = [
        f"# {project_name[0]}\n",
        "This project was generated by [DjangoGravityAssist](https://github.com/SethAngell/DjangoGravityAssist)",
    ]

    with open((new_proj_directory / "readme.md"), "w") as ifile:
        ifile.writelines(readme_contents)
except (FileNotFoundError, FileExistsError, PermissionError) as e:
    print("No readme generated")
except Exception as e:
    standard_error_message(e)

try:
    process = subprocess.Popen(
        [
            "docker",
            "ps",
            "--filter",
            f"name={project_name[1]}",
            "--format",
            "{{.Status}}",
        ],
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    if "Up" in stdout.split(" "):
        print("-- Your django app is up and running :)")
        print(
            f'-- Check it out at {generate_rich("http://localhost:8009", True, color.GREEN)}'
        )
except Exception as e:
    # this isn't crucial, so if it fails just keep trucking
    pass


# output todos if there are any
if len(user_commands) != 0:
    try:
        with open("todos_generated_by_rename_project.md", "w") as ofile:
            ofile.write(command + "\n" for command in user_commands)
    except Exception as e:
        print(
            "To really tie it all together, we weren't even able to write the todos to your new directory lol"
        )
        print("We'll print them all pretty for you right here")
        print("Sorry about that :)")

        print(
            generate_rich(
                "Tasks to complete the duplication process", True, color.GREEN
            )
        )
        for command in user_commands:
            if command[0] != "-":
                print(generate_rich(command, True))
            else:
                print(command)

# Say our goodbyes
print("\n" + ("-" * 80))
print(
    "I hope this script helped reduce some of the boilerplate work of setting up your django projects"
)
print(
    "If you found this project useful, feel free to check out my little corners of the internet"
)
print(
    generate_rich(
        "Twitter: @SethAngell, Github: SethAngell, The Open Web: https://SethAngell.com",
        True,
        color.GREEN,
    )
)
print(generate_rich("Happy Building!", True))
