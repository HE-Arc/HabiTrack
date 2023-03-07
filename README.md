# HabiTrack
Habit tracker using Django

## Lauch project after clone/pull
### Setting .env in api
1. `cd api/habitrack`
2. `cp .env.example .env`
### Setting .env in frontend
3. `cd ../../frontend`
4. `cp .env.example .env`
5. 
    - On the server: comment localhost line
    - Locally: comment habitrack line
### Setting up and starting frontend
6. `npm install`
7. 
    - On the server: `npm run build`
    - Locally: `npm run dev`
### Setting up and starting api
8. In a new terminal: `cd api`
9. Locally if no venv instanciated: `pipenv install`
10. `[path_to_venv]/Scripts/activate`
11. `pipenv install -r requirements.txt`
12. `python manage.py migrate` (in cas of errors `python manage.py flush` to clear database, then migrate again)
13. If no superuser instaciated, create a new one: `python manage.py createsuperuser --email admin@example.com --username admin`
14. `python manage.py runserver`