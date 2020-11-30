import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category, db
from random import randrange
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
      @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
       completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def categories():
        categories = Category.query.order_by(Category.type).all()
        return jsonify({'categories':
                        {category.id:
                         category.type for category in categories}})
    '''
      @TODO:
      Create an endpoint to handle GET requests for questions,
      including pagination (every 10 questions).
      This endpoint should return a list of questions,
      number of total questions, current category, categories.

      TEST: At this point, when you start the application
      you should see questions and categories generated,
      ten questions per page and pagination at the bottom of the screen for
       three pages.
      Clicking on the page numbers should update the questions.
      '''
    def paginatation(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @ app.route('/questions')
    def question_page():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginatation(request, selection)
        categories = Category.query.order_by(Category.type).all()
        return jsonify({
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id:
                           category.type for category in categories},
            'current_category': None
        })

    @ app.route('/categories/<int:category_id>/questions')
    def category_question(category_id):
        current = Category.query.get(category_id)
        if current is None:
            abort(404)
        questions = [i.format() for i in Question.query.filter_by(
            category=str(category_id)).all()]
        return jsonify({"questions": questions,
                        "total_questions": len(questions),
                        "current_category": category_id})

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
     be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @ app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        if question is None:
            return jsonify({
                "question": "question doesn't exist"
            })
        question_text = question.question
        try:
            Question.delete(question)
            return jsonify({
                "question": question_text
            })
        except:
            db.session.rollback()
            return jsonify({
                "database_error": str(sys.exc_info()[1])
            })
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the
     last page
    of the questions list in the "List" tab.
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @ app.route('/questions', methods=['POST'])
    def questions():
        if 'searchTerm' in request.get_json():
            query = request.get_json()['searchTerm']
            results = Question.query.filter(
                Question.question.ilike("%" + query + "%")).all()
            questions = [i.format() for i in results]
            total_questions = len(questions)
            if len(results) > 0:
                current_category = Category.query.get(
                    int(results[0].category)).format()
            else:
                current_category = "NONE"
            return jsonify({
                "questions": questions,
                "total_questions": total_questions,
                "current_category": current_category
            })

        else:
            try:
                question = Question(
                    answer=request.get_json()['answer'],
                    question=request.get_json()['question'],
                    category=request.get_json()['category'],
                    difficulty=request.get_json()['difficulty'])
                Question.insert(question)
                return jsonify({
                    "success": True,
                })
            except:
                db.session.rollback()
                abort(404)

    '''
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        quiz_category = request.get_json()['quiz_category']
        previous_questions = request.get_json()['previous_questions']
        if "type" not in quiz_category.keys():
            abort(404)
        if quiz_category['type'] == "click":
            category_questions = Question.query.filter(
                Question.id.notin_((previous_questions))).all()
        else:
            category_questions = Question.query.filter_by(
                category=str(int(quiz_category['id']))).filter(
                    Question.id.notin_((previous_questions))).all()
        new_question = category_questions[
            randrange(0, len(category_questions))
        ].format() if len(category_questions) > 0 else False
        return jsonify({"question": new_question})
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @ app.errorhandler(400)
    def bad_request(code):
        return jsonify({
            "message": str(code),
            "code": 400
        })

    @ app.errorhandler(401)
    def unauthorize(code):
        return jsonify({
            "message": str(code),
            "code": 401
        })

    @ app.errorhandler(403)
    def forbidden(code):
        return jsonify({
            "message": str(code),
            "code": 403
        })

    @ app.errorhandler(404)
    def not_found(code):
        return jsonify({
            "message": str(code),
            "code": 404
        })

    @ app.errorhandler(405)
    def method_not_allowed(code):
        return jsonify({
            "message": str(code),
            "code": 405
        })

    @ app.errorhandler(406)
    def not_acceptable(code):
        return jsonify({
            "message": str(code),
            "code": 406
        })

    @ app.errorhandler(408)
    def request_timeout(code):
        return jsonify({
            "message": str(code),
            "code": 408
        })

    @ app.errorhandler(409)
    def conflict(code):
        return jsonify({
            "message": str(code),
            "code": 409
        })

    @ app.errorhandler(410)
    def gone(code):
        return jsonify({
            "message": str(code),
            "code": 410
        })

    @ app.errorhandler(411)
    def length_required(code):
        return jsonify({
            "message": str(code),
            "code": 411
        })

    @ app.errorhandler(412)
    def precondition_faled(code):
        return jsonify({
            "message": str(code),
            "code": 412
        })

    @ app.errorhandler(413)
    def not_processable(code):
        return jsonify({
            "message": str(code),
            "code": 413
        })

    @ app.errorhandler(414)
    def long_request(code):
        return jsonify({
            "message": str(code),
            "code": 414
        })

    @ app.errorhandler(416)
    def not_statisfiable(code):
        return jsonify({
            "message": str(code),
            "code": 416
        })

    @ app.errorhandler(417)
    def expectation_failed(code):
        return jsonify({
            "message": str(code),
            "code": 417
        })

    @ app.errorhandler(418)
    def teapot(code):
        return jsonify({
            "message": str(code),
            "code": 418
        })

    @ app.errorhandler(422)
    def processable(code):
        return jsonify({
            "message": str(code),
            "code": 422
        })

    @ app.errorhandler(423)
    def locked(code):
        return jsonify({
            "message": str(code),
            "code": 423
        })

    @ app.errorhandler(424)
    def dependency(code):
        return jsonify({
            "message": str(code),
            "code": 424
        })

    @ app.errorhandler(429)
    def too_many(code):
        return jsonify({
            "message": str(code),
            "code": 429
        })

    @ app.errorhandler(431)
    def not_large(code):
        return jsonify({
            "message": str(code),
            "code": 431
        })

    @ app.errorhandler(451)
    def leagal(code):
        return jsonify({
            "message": str(code),
            "code": 451
        })

    @ app.errorhandler(500)
    def serverError(code):
        return jsonify({
            "message": str(code),
            "code": 500
        })

    @ app.errorhandler(501)
    def not_implemented(code):
        return jsonify({
            "message": str(code),
            "code": 501
        })

    @ app.errorhandler(502)
    def gateway(code):
        return jsonify({
            "message": str(code),
            "code": 502
        })

    @ app.errorhandler(503)
    def service(code):
        return jsonify({
            "message": str(code),
            "code": 503
        })

    @ app.errorhandler(504)
    def timeout(code):
        return jsonify({
            "message": str(code),
            "code": 504
        })

    return app
