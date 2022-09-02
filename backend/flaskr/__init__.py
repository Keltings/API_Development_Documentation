import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


#--------------------------lkh------------------------

def paginate_questions(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)#, resources={r"*/api/*" : {'origins': "*"}})
    
    
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        try:
          categories = Category.query.order_by(Category.type).all()
          
          if not categories:
              abort(422)
                
          return jsonify({
            "success":True,
            "categories": {'id':categories.id,
            'type':categories.type}#json.load(categories)#{cat.id:cat.type for cat in categories}
          })
        except Exception as e:
          print(e)
          abort(404)


    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
          questions = Question.query.all()
          current_questions = paginate_questions(request,questions)
          categories = Category.query.all()
          if (len(current_questions) == 0):
            abort(404)  
          return jsonify({
            "success":True,
            "questions":current_questions,
            "total_questions": len(questions),
            "current_category":None,
            "categories": {cat.id:cat.type for cat in categories}
          })
        except Exception as e:
          print(e)
          abort(404)
    
    
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>',methods=['DELETE'])
    def delete_question(id):
        question =  Question.query.filter( Question.id ==id).one_or_none()
        if not question:
              abort(404)
        try:
            question.delete()
            return jsonify({
                'sucecss':True,
                'deleted' :id})
            
        except Exception as e:
          print(e)
          abort(402)
    
    
   
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions',methods=['POST'])
    def add_question():
        try:
          body = request.get_json()
          new_question = body.get('question')
          new_answer = body.get('answer')
          new_difficulty = body.get('difficulty')
          new_category = body.get('category')
          
          if ((new_question is None) or (new_answer is None) 
              or (new_difficulty is None) or (new_category is None)):
            abort(422)
    
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()
          
          return jsonify({
                'sucecss':True,
                'created' :question.id})
          
        except Exception as e:
          print(e)
          abort(422)
    
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/search',methods=['POST'])
    def search_question():
        try:
          body = request.get_json()
          searchTerm = body.get('searchTerm')
          questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
          current_quesitons = paginate_questions(request,questions)
          total_questions = len(Question.query.all())
          category = Category.query.order_by(Category.id).all()

          if (len(questions) == 0) or not category:
              abort(404)
                  
          return jsonify({
              'sucecss':True,
              'questions': current_quesitons,
              'total_questions': total_questions,
              'current_categroy': category[0].format()['type']
            })
        except Exception as e:
          print(e)
          abort(404)
    
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        try:
          category = Category.query.filter_by(id=id).one_or_none()
          selection = Question.query.filter_by(category=category.id).all()
          question_paginate = paginate_questions(request, selection)
          return jsonify({
                    'success':True,
                    'questions':question_paginate,
                    'total_questions': len(Question.query.all()),
                    'current_categroy': category.format()['type']})
        except Exception as e:
          print(e)
          abort(500)  
    
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/play', methods=['POST'])
    def play_quiz():
        questions = None  
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')
    
        if ((previous_questions is None) or (category is None)):
              abort(400)
        try:
               
          if (category['id'] == 0):
            questions = Question.query.all()

          else:
            questions = Question.query.filter_by(category=category['id']).all()
            question = questions[random.randrange(0,len(questions),1)]
        
          # for q in questions:
          #   if q.id not in previous_questions:
          #     current_question = q.format()
          #     break
            
          return jsonify({
            'sucecss':True,
            'question': question.format()
          }) 
        except Exception as e:
          print(e)
          abort(400)  


    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'sucecss': False,
          'error': 404,
          'message': "resources not found"
        }),404
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'sucecss': False,
          'error': 422,
          'message': "unprocessable"
        }),422
        
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'sucecss': False,
          'error': 400,
          'message': "bad request"
        }),400
        
    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500     
        
    if __name__ == '__main__':
        app.run(debug=True)
        
    

    return app

