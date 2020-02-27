# PB_P8
PureBeurreP8

## How to install this project

### 1 - Fork the project
### 2 - Clone the project on your PC
### 3 - Create and set the database
This project was conceived with postgresql, but we can use an other db engine.

#### STEP 1 : Create a database.
`createdb <your database name>`

#### STEP 2: Create your virtualenv in this path: Projet OpenClassRoom/Projet-8-Pur-Beurre
(on mac and linux)<br/>
`cd PB_P8`<br/>
`virtualenv env -p python3`<br/>
`source env/bin/activate`<br/>
`pip install -r requirements.txt`<br/>
`cd pur_beurre_project`<br/>

#### STEP 3 : Setting up the database in pur_beurre_project/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your database name>',
        'USER': '<your username>',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}
```

#### STEP 4 : Migrate the model into the database
you must be at this location to launch the command: Projet **PB_P8/pur_beurre_project**<br/>
`./manage.py migrate`

#### STEP 5 : Load database
open the module **pur_beurre_project/foodSearch/management/commands/settings.py**.<br/>
Change the pages from OpenFoodFacts you want to include in your database
```
FIRST_PAGE =  <first page from openfoodfacts api you want to load>
LAST_PAGE = <last page from openfoodfacts api you want to load>
```
*NB:* 10 products per page (around 5 seconds per page on my mac)

`./manage.py fill_db -f`

#### STEP 6 : Launch project
`./manage.py runserver`
With your usual browser, use the application on url http://127.0.0.1:8000/
