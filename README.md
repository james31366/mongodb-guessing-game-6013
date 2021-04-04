# Guessing Game 6013 Mongo DB

This is the online guessing game web application for Database homework. <br>

## Requirements

- Docker
- Python3.6 or Higher
- pip

## Setup for Guessing Game Web application

Download the code from git using `git clone`. Do the following step to use this application.

`python3` refers to the Python 3 command using in Linux and Mac system. For window use `python` or `py`.

1. Run and  install the docker container

   ```bash
   docker-compose up -d
   ```

2. Check python version (it should be 3.6 or 3.7).

   ```bash
   python --version
   ```

3. Install all required packages.

   ```bash
   cd app
   pip install -r requirements.txt
   ```

4. After finish all development of this program
   You have to cd into the top directories that is inside the clone folder and then

   ```bash
   docker-compose down -v
   ```

## Running the application

1. Run and install the docker container

   ```bash
   docker-compose up -d
   ```

2. You can run the web application in [localhost:80](http://localhost/)
