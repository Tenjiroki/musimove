About: it is the basis for the platform to sell music instrument, which includes:
* registering the user
* post offers
* book offers
* display all the viable options

How to run:
Clone the repository
git clone https://github.com/твій_нік/musimove.git
cd musimove

Activate the virtual environment
python -m venv venv
source venv/bin/activate  or venv\Scripts\activate on Win

Install dependencies
pip install -r requirements.txt

Create .env and add the data:
SECRET_KEY= secret key
DEBUG=True
DB_NAME= postgres
DB_USER= postgres
DB_PASSWORD= your password
DB_HOST= localhost
DB_PORT= 5432

Do database migrations and create a superuser:
python manage.py migrate
python manage.py createsuperuser

Start server:
python manage.py runserver
