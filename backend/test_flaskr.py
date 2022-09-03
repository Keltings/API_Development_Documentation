import os
from tkinter.messagebox import QUESTION
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = database_path = 'postgresql://postgres:{}/{}'.format('#Datascience1@localhost:5432', self.database_name)
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

    def test_get_categories(self):        
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['categories'], data['categories'])

    def test_404_get_categories_failed(self): 
        res = self.client().get('/categoriess')
        data =json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'resources not found')  


    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'],None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_beyond_valid_page(self):
        res =self.client().get('/questions?page=20000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"resources not found")

    
    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 13)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question,None)
    
    def test_422_delete_question_failed(self):
        res = self.client().delete('/questions/336')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")


    def test_create_question(self):
        new_question = {
            'question': 'Who is the King of bollywood?',
            'answer': 'SRK',
            'category': '5',
            'difficulty': 4}

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created']),
        self.assertTrue(len(data['questions'])),
        self.assertTrue(data['total_questions'])
    
    def test_405_add_new_question_not_allowed(self):
        new_question = {
            'question': 'Testing?',
            'answer': '',
            'category': 2,
            'difficulty': ''}

        res = self.client().post('/questions', json =new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")    
         
    
    def test_get_question_search_found(self):
        res = self.client().post('/search', json={'searchTerm': 'name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_get_book_search_not_found(self): 
        res = self.client().post('/questions', json={'search': 'In'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'], 0)
        self.assertTrue(len(data['questions']), 0)   


    def test_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_questions_based_on_category_not_found(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)


    def test_play_quiz(self):
        data = {
            'previous_questions': [1, 4, 20, 15],
        'quiz_category': 'current category'
 }
        res = self.client().post('/quizzes', json={
                                                'previous_questions':[19,20],
                                                'quiz_category':{'id':'1','type':'Science'}
                                                     })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
     
    def test_play_quiz_not_found(self):
        res = self.client().post('/play', json={})   
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resources not found")    
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()