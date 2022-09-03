import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


#--------------------------NUMBER OF QUESTIONS DISPLAYED-----------------------

def paginate_questions(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


#-----------------------CINFIGURING FLASK,CONNECTING TO DB AND CORS---------------
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app) #, resources={r"*/api/*" : {'origins': "*"}})
    
    
  #------------------------ALLOW HEADERS AND METHODS---------------------------  
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


  #--------------------------GET REQUESTS END POINTS----------------------------  
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
          categories = Category.query.all()
          #get the id and the type of each category
          cats ={}
          for cat in categories:
            cats[cat.id] = cat.type


          if not categories:
              abort(422)
                
          return jsonify({
            "success":True,
            "categories": cats
          })
        except:
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
          questions = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request,questions)

          categories = Category.query.all()
          #get the id and the type of each category
          cats ={}
          for cat in categories:
            cats[cat.id] = cat.type

          if (len(current_questions) == 0):
            abort(404)  
          return jsonify({
            "success":True,
            "questions":current_questions,
            "total_questions": len(questions),
            "current_category": None, #cats[cat.id].format(),
            "categories": cats
          })
        except:
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
          questions = Question.query.all()
          category = Category.query.filter_by(id=id).one_or_none()
          selection = Question.query.filter_by(category=category.id).all()
          question_page = paginate_questions(request, selection)

          return jsonify({
                    'success':True,
                    'questions':question_page,
                    'total_questions': len(questions),
                    'current_category': category.format()['type']})
        except:
          abort(500) 
    
  #------------------------DELETE METHODS FOR IDs------------------------------  
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>',methods=['DELETE'])
    def delete_question(id):
        try:
          question =  Question.query.filter( Question.id ==id).one_or_none()

          if question is None:
            abort(404)
            
          question.delete()
          selection = Question.query.order_by(Question.id).all()
          current_qestions = paginate_questions(request, selection)

          return jsonify({
                'success':True,
                'deleted' : id,
                'questions': current_qestions,
                'total_questions': len(Question.query.all())})
            
        except:
          abort(422)

   
    
  #------------------CREATING QUESTIONS, CREATING BASED ON SEARCH TERMS--------------- 
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
    def create_question():
        try:
          body = request.get_json()
          new_question = body.get('question')
          new_answer = body.get('answer')
          new_category = body.get('category')
          new_difficulty = body.get('difficulty')
    
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)
          
          return jsonify({
                'success':True,
                'created' :question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())})
          
        except:
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
          search = body.get('searchTerm')
          questions = Question.query.filter(Question.question.ilike('%' + search + '%')).all()
          current_questions = paginate_questions(request,questions)
          
          category = Category.query.order_by(Category.id).all()

                  
          return jsonify({
              'success':True,
              'questions': current_questions,
              'total_questions': len(Question.query.all()),
            })
        except:
          abort(404)
    
    
    
    
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

    @app.route('/quizzes', methods=['GET', 'POST'])
    def play_quiz():
      questions = None
      try:
        body = request.get_json()
        questions = None
        previous_quizzes = body.get('previous_questions')
        category_quiz = body.get('quiz_category') 
        
    
        if ((previous_quizzes is None) or (category_quiz is None)):
              abort(400)
        
               
        if (category_quiz['id'] == 0):
            questions = Question.query.all()
            selected_quiz = questions[random.randrange(0,len(questions), 1)]

        else:
          questions = Question.query.filter_by(category=category_quiz['id']).all()
          selected_quiz = questions[random.randrange(0,len(questions), 1)]

        #potential_questions = [quiz for quiz in questions if quiz['id'] not in previous_quizzes]  
          
        return jsonify({
            'success':True,
            'question': {"answer": selected_quiz.answer,
                        "category": selected_quiz.category,
                        "difficulty": selected_quiz.difficulty,
                        "id": selected_quiz.id,
                        "question": selected_quiz.question
                    },
            'previous_question': 'previous_quizzes'
            #'previous_question': potential_questions.format()
          }) 
      except:
        abort(404)  




  #--------------------------ERROR HANDLING----------------------------------
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': "resources not found"
        }),404
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': "unprocessable"
        }),422
        
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
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

