# SpaceX-Trello

Requirements:
Python 3.6 at least

To set up local server:

1. Use pip to install virtualenv
python get-pip.py
pip install virtualenv

2. Create a virtualenv
virtualenv name_of_env
\path\to\env\Scripts\activate

3. Initialize app
Go to 'SPACEX-Trello' directory and run 'pip freeze -r requirements.txt' to install dependencies
Create 'settings.py' file and add your Trello api key and token
uvicorn main:app --reload