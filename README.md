## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install trivia api.
by going to the backend folder and writing the following command

```bash
pip install -r requirements.txt
```

then install the frontend dependencies by going to the frontend folder and doing

```bash
npm install
```

and then go to models.py and change the database url path

and to run tests you go to backend folder and run the following command after you have changed
the database url in the test_flaskr.py

```bash
python test_flaskr.py
```

## Usage

in order to run the frontend server write the following command

```bash
npm start
```

and to run the backend server run the following command go to the backend folder and then

```bash
set flask_py=flaskr
flask run
```

## end points

```bash
Get /categories
```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains key: object pairs.
  {'1' : "Science"}

```bash
Get /questions
```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: page
- Returns: An object with a single key, categories, that contains key: object pairs.
  {'1' : "Science"}

```bash
Get /categories
```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object that has a list of questions objects, a list of categories, and the number of questions and the current category.
  <br>{'questions' : [{"id": 1,"current_category":"food", "question":"Some question","answer":"some answer","category":"category","difficutly":"hard"}], "total_questions":1,"categories",["science"]}

```bash
DELETE /questions
```

- deletes a question from the database
- Request Arguments: the id of the question
  {'1' : "Science"}
- returns the text of the question that was deleted <br>
  {"question":"some_question"} and database error in case of failure like this
  {"question":"some database error"}

```bash
POST /questions
```

- does one of two functionalities , either search for something or creates a new question in
  the database depending on the paramter passed
- if the paramter passed is a search term like this {"searchTerm":"term"} then the result would
  be an object that has the result question and the total number of questions that are the in the search result and the current category , the object is <br>
  {"questions":["question1","question2"],"total_questions": 1 , "current_category":"food"}
- if the paramter passed was a question object then the question object would be created and the question created would be returned in an object

```bash
POST /quizzes
```

- recieves a list of questions that was asked to the user before in the game and a question category and returns a random question that wasn't asked before
  -paramters would be like this {"previous_questions":["some question"], "quiz_category":"food"}
- the return would be a question object like this {"question":"question"}
