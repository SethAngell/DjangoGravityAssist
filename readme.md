# Django Gravity Assist
A starter template for Django projects which meets the following requirements:
* Dockerized for ease of startup
* Django Rest Framework installed
* Authentication endpoints set up for DjangoRest Framework
* Pytest installed for testing
* Custom User Model pre-instantiated
* Github Actions Set up for testing
* .ci directory containing a production version of the Dockerfile as well as docker-compose.yaml

![A gif displaying the terminal interface for rename_project.py. This contains a series of questions about where to save the new project and what it should be named. Alongside this, there are a number of updates that occur to inform the user of what the script is actively doing - such as copying directories over and deleting unnecessary files](demo.gif)


## Inspiration
This project is heavily inspired by [William Vincent's DRFx Repository](https://github.com/wsvincent/drfx) and guided by his tutorial [found here](https://wsvincent.com/django-rest-framework-user-authentication-tutorial/), with a few of my opinions included as well as some niceties that I prefer in my projects:
* Whether it's used or not, it's nice to have pytest installed and set up before getting started
* Similarly, I host exclusively on Github. So a basic github actions workflow is nice
* Docker from the start, simply because it's nice to be able to jump right into a new project without setting up requirements
* pip + requirements.txt for dependency management

## How to use
There are 2 ways to use the project:

### 1. Clone the directory and get to building
At it's core, this repo contains a greenfield django application with minimal configuration. It defines a custom user model for flexibility later on, and imports django-rest-auth and django-all-auth in order to provide api endpoints for authentication and registration. Alongside that are all the Docker files needed to spin up a new project. A simple `docker-compose up -d` should result in the Django hello world page running at [http://localhost:8009](https://localhost:8009). To help make the project your own, the [ManualRenameToDo.md](./ManualRenameToDo.md) file contains a list of files and directories that need to be changed in order to make the project completely yours.

### 2. As a project generator
If you're constantly spinning up new Django Projects, this library can also be used as a generator for new Django repos. The `rename_project.py` script uses the python core library to create and prepare a duplicate of the project in the `/app` directory, modified by your input (new project name, directory location, etc). This script uses exclusively the python standard library, so no external packages are needed. Any interpreter 3.6 or higher should be able to run it.

