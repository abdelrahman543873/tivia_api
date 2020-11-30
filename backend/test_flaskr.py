import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "scrapy"
        self.database_path = "postgres://{}/{}".format(
            'postgres:vindiesel3@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_questions_error(self):
        res = self.client().get('/categories/22222222222/questions')
        self.assertEqual(list(res.get_json().keys()), ['code', 'message'])

    def test_paging_error(self):
        res = self.client().get('/questions?page=10000000')
        self.assertEqual(list(res.get_json().keys()), [
                         'categories', 'current_category', 'questions', 'total_questions'])

    def test_questions(self):
        res = self.client().get('/categories/1/questions')
        response_keys = ['current_category', 'questions', 'total_questions']
        self.assertEqual(list(res.get_json().keys()), response_keys)

    def test_paging(self):
        res = self.client().get('/questions?page=1')
        response_keys = ['categories', 'current_category',
                         'questions', 'total_questions']
        self.assertEqual(list(res.get_json().keys()), response_keys)

    def test_search(self):
        res = self.client().post(
            '/questions', json={"searchTerm": "a"})
        keys = ['current_category', 'questions', 'total_questions']
        self.assertEqual(list(res.get_json().keys()), keys)

    def test_search_404(self):
        res = self.client().post(
            '/questions', json={"searchTerm": "12345"})
        self.assertEqual(res.get_json()['current_category'], "NONE")

    def test_delete(self):
        res = self.client().delete(
            '/questions/5'
        )
        self.assertEqual(list(res.get_json().keys()), ['question'])

    def test_delete_error(self):
        res = self.client().delete(
            '/questions/10000000000'
        )
        self.assertEqual(list(res.get_json().keys()), ['question'])

    def test_creation(self):
        res = self.client().post(
            '/questions', json={"question": "sds",
                                "answer": "sffff",
                                "difficulty": "4",
                                "category": 0}
        )
        self.assertEqual(list(res.get_json().keys()), ['success'])

    def test_creation_error(self):
        res = self.client().post(
            '/questions', json={"answer": "testing",
                                "question": "this is testing",
                                "category": "slkfjsl",
                                "difficulty": "testing"}
        )
        self.assertEqual(list(res.get_json().keys()), ['code', 'message'])

    def test_quiz(self):
        res = self.client().post(
            '/quizzes',
            json={"quiz_category": {"type": "click",
                                    "id": 0}, "previous_questions": []}
        )
        self.assertEqual(list(res.get_json().keys()), ['question'])

    def test_quiz_not_exist(self):
        res = self.client().post(
            '/quizzes',
            json={"quiz_category": {"id": "1000000"},
                  "previous_questions": ["this is hello"]}
        )
        self.assertEqual(list(res.get_json().keys()), ['code', 'message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
