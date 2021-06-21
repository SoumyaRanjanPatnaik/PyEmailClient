#!/bin/bash
mv token_gmail_v1.pickle token_gmail_v1.pickle.old
touch token_gmail_v1.pickle
python -m eel Main.py Static -n "PyEmailClient" --add-data "client_secret.json:." --add-data "token_gmail_v1.pickle:." --noconsole --icon = ./assets/logo.icns

rm ./dist/PyEmailClient/token_gmail_v1.pickle
mv token_gmail_v1.pickle.old token_gmail_v1.pickle
