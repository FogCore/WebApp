from WebApp.models import User
from WebApp import app, jwt, APIGateway
from WebApp.forms import SignUpForm, SignInForm, CloudletsFindForm
from flask import render_template, url_for, flash, redirect, make_response, request
from flask_jwt_extended import (
    jwt_optional, jwt_required, set_access_cookies,
    current_user, unset_jwt_cookies, get_jwt_claims
)


# Forwards the user to the authentication page if the access token is not valid
@jwt.expired_token_loader
@jwt.claims_verification_failed_loader
@jwt.invalid_token_loader
@jwt.user_loader_error_loader
def failed_token_callback(reason):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


# Forwards the user to the authentication page and adds the next parameter when accessing protected resources
# The next parameter defines the current page and allows to redirect the user to it after successful authentication
@jwt.unauthorized_loader
def unauthorized_loader_callback(reason):
    return redirect(url_for('login', next=request.url_rule))


# Creates an instance of the User class from the access token
@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    claims = get_jwt_claims()
    if claims:
        return User(username=identity, first_name=claims['first_name'], last_name=claims['last_name'], admin=claims['admin'])
    else:
        return None


# Homepage
@app.route('/')
@app.route('/home')
@jwt_optional
def home():
    if current_user:
        return render_template('home.html', user=current_user)
    else:
        return render_template('home.html')


# Documentation page
@app.route('/documentation')
@jwt_optional
def documentation():
    if current_user:
        return render_template('documentation.html', title='Documentation', user=current_user)
    else:
        return render_template('documentation.html', title='Documentation')


# System registration page for a new user
@app.route('/join', methods=['GET', 'POST'])
@jwt_optional
def join():
    if current_user:
        return redirect(url_for('home'))

    form = SignUpForm()
    if form.validate_on_submit():
        api_response = APIGateway.User.add_user(first_name=form.first_name.data,
                                                last_name=form.last_name.data,
                                                username=form.username.data,
                                                password=form.password.data)
        json = api_response.json()
        if api_response.status_code == 201:
            flash(json['message'], 'success')
            response = make_response(redirect(url_for('home')))
            set_access_cookies(response, json['access_token'])
            return response
        else:
            flash(json['message'], 'danger')
    return render_template('join.html', title='Sign Up', form=form)


# System user authentication page
@app.route('/login', methods=['GET', 'POST'])
@jwt_optional
def login():
    if current_user:
        return redirect(url_for('home'))

    form = SignInForm()
    if form.validate_on_submit():
        api_response = APIGateway.User.login(username=form.username.data, password=form.password.data)
        json = api_response.json()
        if api_response.status_code == 200:
            flash('You have successfully logged in.', 'success')
            next_page = request.args.get('next')
            response = make_response(redirect(next_page)) if next_page else make_response(redirect(url_for('home')))
            set_access_cookies(response, json['access_token'])
            return response
        else:
            flash(json['message'], 'danger')
    return render_template('login.html', title='Sign In', form=form)


# Logout method
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    unset_jwt_cookies(response)
    return response


# User account page
@app.route('/account')
@jwt_required
def account():
    username = request.values.get('username', type=str)
    token = request.cookies.get('access_token')
    api_response = APIGateway.User.get_user_info(username=username if username else current_user.username,
                                                 token=token)
    return render_template('account.html', title='Account', response=api_response, user=current_user)


# Fog application images page
@app.route('/images')
@jwt_required
def images():
    token = request.cookies.get('access_token')
    username = '' if current_user.admin else current_user.username
    api_response = APIGateway.Images.list(username=username, token=token)
    return render_template('images.html', title='Images', user=current_user, response=api_response)


# The image page of specified fog application
@app.route('/image/<string:username>/<string:image_name>')
@jwt_required
def image(username, image_name):
    token = request.cookies.get('access_token')
    api_response = APIGateway.Images.find(username=username, image_name=image_name, token=token)
    return render_template('image.html', title='Image', user=current_user, response=api_response)


# Method of removing the image of a fog application
@app.route('/image/delete/<string:username>/<string:image_name>')
@jwt_required
def delete_image(username, image_name):
    token = request.cookies.get('access_token')
    api_response = APIGateway.Images.delete(username=username, image_name=image_name, token=token)
    flash(api_response.json()['message'], 'success' if api_response.status_code == 200 else 'danger')
    return redirect(url_for('images'))


# Fog devices page
@app.route('/cloudlets', methods=['GET', 'POST'])
@jwt_required
def cloudlets():
    params = {}
    for key, value in request.form.items():
        if value and key != 'csrf_token' and key != 'submit':
            params[key] = value
    form = CloudletsFindForm()
    if form.validate_on_submit():
        return redirect(url_for('cloudlets'))
    token = request.cookies.get('access_token')
    api_response = APIGateway.Cloudlets.find(cloudlet=params, token=token)
    return render_template('cloudlets.html', title='Cloudlets', form=form, user=current_user, response=api_response)


# The specified fog device page
@app.route('/cloudlet/<string:id>')
@jwt_required
def cloudlet(id):
    token = request.cookies.get('access_token')
    api_response = APIGateway.Cloudlets.find(cloudlet={'id': id}, token=token)
    return render_template('cloudlet.html', title='Cloudlet', user=current_user, response=api_response)
