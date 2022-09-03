# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database for main development and the test one

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

To run the test

```bash 
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Referrence
### Getting started
  - Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
  - Authentication: This version of the application does not require authentication or API keys.

### Run the Server

To run the application run the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Error Handling
Errors are returned as JSON objects in the following format:

```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return these error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal Server Error

### Endpoints

#### GET /categories

- General:

  - Returns a list of categories, and success value

Sample: 
```bash 
curl http://127.0.0.1:5000/categories
```

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
#### GET /categories/{id}/questions

- General:

  - Returns a list of questions, in the given category, category total_questions and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
  - Sample: 
  ```bash 
  curl http://127.0.0.1:5000/categories/3/questions
  ```

```bash
{
  {
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 
1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about 
a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### DELETE /questions/{id}

- General:

  - Deletes the question of the given ID if it exists. Returns success value.
  - Sample:
  ```bash
  curl -X DELETE http://127.0.0.1:5000/questions/16?page=2
  ```

```bash
{
  "success": true
}
```

#### POST /questions/{id}

- General:

  - Creates a new question using the submitted title, answer, category and difficulty. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend
  - Sample: 
  ```bash
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is the King of Bollywood?", "answer": "SRK","category" :"4", "difficulty":"2"}'
  ```

```bash
{
  {
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
    "current_category": null,
    "questions": [
    {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
    },
    {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
    },
    {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
    },
    {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
    }
    ],
    "success": true,
    "total_questions": 19
    }
```
#### POST /search

- General:

    - searches for a question using the submitted search term. Returns the results, success value, total questions.
    - Sample: 
    ```bash
    curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'
    ```

```bash
{
  {
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Lungs",
      "category": 1,
      "difficulty": 2,
      "id": 25,
      "question": "Name a body organ"
    },
    {
      "answer": "Sputnik 1",
      "category": 1,
      "difficulty": 2,
      "id": 27,
      "question": "What was the name of the first man-made satellite launched by the Soviet Union in 1957?"
    },
    {
      "answer": "Sputnik 1",
      "category": 1,
      "difficulty": 2,
      "id": 28,
      "question": "What was the name of the first man-made satellite launched by the Soviet Union in 1957?"
    }
  ],
  "success": true,
  "total_questions": 5
}
```

#### POST /quizzes

- General:

  - gets the question and its category
  - returns the next question in the same category and success value.
  - Sample: 
  ```bash
  curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'
  ```

```bash
{
  "previous_question": "previous_quizzes", 
  "question": {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}
```





