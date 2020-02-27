# PUR BEURRE - OPENCLASSROOM - PROJECT #8 PYTHON
This open source project was created for the OpenClassRoom's Python developer course (Project 8/13)).
It is a DJANGO application integrating a back-end part based on Python 3.7 and a front-end part developed with HTML5, CSS3 and JavaScript using Bootsrap.

Ask the application a product name, select one of the products to confirm your choice and it will give you a list of similar products with a better nutriscore.
When registered, the user can save those favorite subsitutes.

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
Open the module **pur_beurre_project/foodSearch/management/commands/settings.py**.<br/>
Change the pages from OpenFoodFacts you want to include in your database<br/>
*NB: 10 products per page (around 5 seconds per page on my mac)*
```
FIRST_PAGE =  <first page from openfoodfacts api you want to load>
LAST_PAGE = <last page from openfoodfacts api you want to load>
```
`./manage.py fill_db -f`

#### STEP 6 : Launch project
`./manage.py runserver`
With your usual browser, use the application on url http://127.0.0.1:8000/

## Find the project online

This project can be tested on url https://pbp8.herokuapp.com/

## Next Steps
Allow user to change his password or ask for an other one if he lost it
