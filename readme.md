# Django Gravity Assist
A starter template for Django projects which meets the following requirements:
* Dockerized for ease of startup
* Django Rest Framework installed
* Authentication endpoints set up for DjangoRest Framework
* Pytest installed for testing
* Custom User Model pre-instantiated
* Github Actions Set up for testing


## Inspiration
This project is heavily inspired by [William Vincent's DRFx Repository](https://github.com/wsvincent/drfx) and guided by his tutorial [found here](https://wsvincent.com/django-rest-framework-user-authentication-tutorial/), with a few of my opinions included as well as some niceties that I prefer in my projects:
* Whether it's used or not, it's nice to have pytest installed and set up before getting started
* Similarly, I host exclusively on Github. So a basic github actions workflow is nice
* Docker from the start, simply because it's nice to be able to jump right into a new project without setting up requirements
* pip + requirements.txt for dependency management

## ToDo
- [x] Set Up Docker
- [x] Set Up Custom User Model
- [ ] Set Up Pytest
- [x] Set Up Authentication With Endpoints
- [ ] Set up utilities for renaming base project
- [ ] Set Up Github Actions For Testing
