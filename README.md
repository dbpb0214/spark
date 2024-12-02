## Intro

Python script that parses a csv file (e.g. slcsp.csv) and finds the missing data using other csv files (1. zips.csv & 2. plans.csv)

### To run

In order to run this script you need to have a directory inside of the project called `slcsp` with the following 3 csv files:
1. plans.csv
2. slcsp.csv
3. zips.csv

Once you have the directory and files in place we can open up a terminal and from the root of the project call:

``
python3 app.py 
``

This will output a new file called `new_updated_csv.csv`
