from flask import render_template, redirect, url_for, flash, request, abort
from issues_blog import app, db, bcrypt
from issues_blog.models import User, Issue
from issues_blog.forms import RegisterForm, LoginForm, ReportForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc, asc

@app.route('/', methods = ['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Login Successful.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email or password.', 'danger')
    return render_template('index.html', form = form)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Create a hashed password for the user
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname = form.firstname.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form = form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/report/new', methods = ['POST', 'GET'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        flash('Your issue has been added, a technician will be sent promptly.', 'success')
        issue = Issue(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(issue)
        db.session.commit()
        return redirect(url_for('issues'))
    return render_template('report.html', form = form)

# Updating my issues
@app.route('/issue/<int:issue_id>', methods = ['POST', 'GET'])
@login_required
def issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return render_template('issue.html', title = issue.title, issue = issue)

@app.route('/issue/<int:issue_id>/update', methods = ['POST', 'GET'])
@login_required
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.author != current_user:
        abort(403)
    form = ReportForm()
    # Update the Issue in the database
    if form.validate_on_submit():
        issue.title =  form.title.data
        issue.content =  form.content.data
        db.session.commit()
        flash('Your Issue has been updated!', 'success')
        return redirect(url_for('issue', issue_id = issue.id))

    # Populate the report form with the current information
    elif request.method == 'GET':
        form.title.data = issue.title
        form.content.data = issue.content
    return render_template('report.html', form = form)

@app.route('/issues')
@login_required
def issues():
    issues = Issue.query.order_by(Issue.date_created.desc()).all()
    return render_template('issues.html', issues = issues)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))