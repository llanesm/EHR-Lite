# CS 340 Database Project
## A "Lite" EHR System done in Python/Flask
### By Kevin Benoit and Matthew Llanes

This webapp branch is meant for hosting on OSU server

Initial setup:
```bash
bash
virtualenv venv -p $(which python3)
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
```
Then change db_credentials.py to your credentials

###For routine coding:
```bash
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p XXXX --reload
```
Replace XXXX with port number

Website will be at http://flipN.engr.oregonstate.edu:XXXX
Remember what putty flip you are in, N = 1, 2, or 3


###To run persistently:
```bash
gunicorn run:webapp -b 0.0.0.0:XXXX -D
```


###To kill old gunicorn:
```bash
ps ufx | grep gunicorn
```

*Credit to knightsamar/CS340_starter_flask_app repo for initial webapp setup*