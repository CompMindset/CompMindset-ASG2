from flask import Blueprint, render_template, jsonify, request, flash, redirect
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.controllers.auth_controller import AuthController

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = AuthController.login(data['username'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password given')
        return response, 401
    flash('Login Successful')
    set_access_cookies(response, token)
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = AuthController.login(data['username'], data['password'])
    if not token:
        return AuthController.error_response('Bad username or password given', 401)
    
    response = jsonify(AuthController.success_response({
        'access_token': token
    }))
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response