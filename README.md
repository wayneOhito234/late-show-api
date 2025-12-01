# late-show-api

## 2. Installation and setup
### a) clone the repo
```bash
git@github.com:wayneOhito234/late-show-api.git
```
### b) Create and activate your virtual environment
```bash
python -m venv env
env\Scripts\activate
```
### c) Installing dependecies
```bash
pip install -r requirements.txt
```
## 3 Database Setup
This project uses SQLite (app.db).
You must initialize the database before running the server.

### a) Run the app once to create the database
```bash
python -m server.seed
```
## 4. Run the server
```bash
python -m server.app
```
## 5 . API endpoints
Episodes
GET /episodes
DELETE /episodes/<id>
Guests
GET /guests
Appearances
POST /appearances

## 6. Running Tests
Make sure your virtual environment is active, then:
```bash
pytest -x
```