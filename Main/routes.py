from flask import render_template, redirect, url_for, flash, request
from Main import app, db
from Main.models import Contact, User
from Main.forms import ContactFrom, LoginForm, RegisterForm
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
# for email
import smtplib
from email.message import EmailMessage
# To load the email user and passkey
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
def email_alerts(subject, body, to):
    passkey=EMAIL_PASS
    user = EMAIL_USER

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, passkey)
    server.send_message(msg)
    

    server.quit()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/about')
@login_required
def about_page():
    return render_template('about.html')
    pass
@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact_page():
    form = ContactFrom()
    # print(form.validate_on_submit)
    if form.validate_on_submit():
        pushing_sumit_to_database = Contact(name = form.name.data, 
                                            email_address = form.email_address.data,
                                            phone = form.phone.data,
                                            description = form.description.data)
        db.session.add(pushing_sumit_to_database)
        db.session.commit()
        flash("Thanks for Contacting.", category='info')
        subject = f"Hello {pushing_sumit_to_database.name}, Thanks for Contacting Us!"
        body = (
            f"Dear {pushing_sumit_to_database.name},\n\n"
            "Thank you for reaching out. We have received your message with the following details:\n\n"
            f"📧 Email: {pushing_sumit_to_database.email_address}\n"
            f"📞 Phone: {pushing_sumit_to_database.phone}\n"
            "We will get back to you as soon as possible.\n\n"
            "Best regards,\nTeam 5AM"
        )
        # Email message to send the user - contacted person
        email_alerts(subject, body, pushing_sumit_to_database.email_address)
        
        body1 =  (
            f"Hey, {pushing_sumit_to_database.name} just contacted you!\n\n"
            "Here are the submitted details:\n"
            f"📧 Email: {pushing_sumit_to_database.email_address}\n"
            f"📞 Phone: {pushing_sumit_to_database.phone}\n"
            f"🏠 Feedback: {pushing_sumit_to_database.description}\n"
        )
        # Email message to send the owner of the company
        email_alerts(f'New Contact Form Submission by {pushing_sumit_to_database.name}', body1, 'bigyanmishra022@gmail.com')
        return redirect(url_for('home_page'))

    
    return render_template('contact.html', form=form)



@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method=='POST':
        user_name = request.form['name']
        password = request.form['password']
        
        attempted_user = User.query.filter_by(user_name = user_name).first()
        if attempted_user and check_password_hash(attempted_user.password, password):
            login_user(attempted_user)
            flash(f"Login Successful! {attempted_user.user_name}", category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid Username or Password. Try again.', category='danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        user_name = request.form['name']
        password1 = request.form['password1']
        password2 = request.form['confirm_password']
        email = request.form['email']
        print(user_name, password1, password2, email)
    
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_username = User.query.filter_by(user_name=user_name).first()
        if password1 != password2:
            flash('Password Must be equal! Try Again.', category='danger')
        else:
            if existing_user_email:
                flash("Email already registered. Try another email address.", category="danger")
            elif existing_user_username:
                flash("Username already taken. Pick a new one.", category="danger")
            else:
                
                user_to_create = User(
                    user_name=user_name,
                    email=email,
                    password = generate_password_hash(password2)
                )
                db.session.add(user_to_create)
                db.session.commit()
                login_user(user_to_create)  # yo vaneko , yedi naya account setup vayo vane, then entered the user into the logged in page
                flash(f"Account created successfully! You are logged in as {user_to_create.user_name}", category="success")
                email_alerts('Account Created!', 'Welcome to Team 5AM! Your account has been created successfully. Enjoy!', user_to_create.email)
                email_alerts('New Account Creation!', f'Mr.{user_to_create.user_name} is added to your platform. Look forward!', 'bigyanmishra022@gmail.com')
                return redirect(url_for('home_page'))
                
   
    
    return render_template('register.html')




@app.route('/logout')
def logout_page():
    logout_user()
    flash("Successfully Logged Out!", category='info')
    return redirect(url_for('home_page'))