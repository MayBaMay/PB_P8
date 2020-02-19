# PB_P8
PureBeurreP8

## Use the project

### 1 - Fork the project
### 2 - Clone the project on your PC
### 3 - Create and set the database
In this case i use postgresql, but we can use an other db engine.

#### STEP 1 : Create a database.
`createdb <your database name>`

####STEP 2: Create your virtualenv in this path: Projet OpenClassRoom/Projet-8-Pur-Beurre.
`virtualenv env -p python3`
`source env/bin/activate`
`pip install -r requirement.txt`
`cd pur_beurre_poject`

#### STEP 3 : Setting up the database in PurBeurre/settings.py
`DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your database name>',
        'USER': '<your username>',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}`

#### STEP 4 : Migrate the model into the database
you must be at this location to launch the command: Projet OpenClassRoom/Projet-8-Pur-Beurre/PurBeurre
`./manage.py migrate`

#### STEP 5 : Load database
open the module pur_beurre_project/foodSearch/management/commands/settings.py.<br/>
Change the pages from OpenFoodFacts you want to include in your database
`FIRST_PAGE =  <first page>
LAST_PAGE = <last page>`

`./manage.py fill_db -f`

#### STEP 6 : Launch project
`./manage.py runserver`
With your usual browser, use the application on url http://127.0.0.1:8000/
