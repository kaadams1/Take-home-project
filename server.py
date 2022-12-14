"""Server for reservations app."""

import os
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Reservation
import pandas as pd
from datetime import datetime, timedelta
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "veryverysecretkey2239"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage/user registration & login."""

    return render_template("homepage.html")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")

    user = User.get_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = User.create(email)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")

    user = User.get_by_email(email)

    if not user:
        flash("The email you entered was incorrect.")
        return redirect('/')
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        user = User.get_by_email(session["user_email"])
        flash(f"Welcome back, {user.email}!")

    return render_template("view.html", user=user)


@app.route("/view", methods=["GET"])
def view_user():
    """Show homepage for a particular user."""

    if "user_email" in session:
        user = User.get_by_email(session["user_email"])
        user_id = user.user_id

        reservation_list = Reservation.query.filter(Reservation.user_id == user.user_id).all()

    else:
        flash("Please log in!")
        return redirect("/")

    return render_template("view.html", user=user, user_id=user_id, reservation_list=reservation_list)


@app.route('/logout')
def logout():
    """User logout."""

    session.pop('email', None)
    return redirect('/')


@app.route("/search", methods=["GET"])
def search():
    """Search for available reservations."""

    start = datetime.strptime("16:00:00", "%H:%M:%S")
    end = datetime.strptime("21:00:00", "%H:%M:%S")

    min_gap = 30

    time_list = [(start + timedelta(hours=min_gap*i/60)).strftime("%I:%M %p")
       for i in range(int((end-start).total_seconds() / 60.0 / min_gap))] #list of strings

    user = User.get_by_email(session["user_email"])
    user_id = user.user_id
    reservation_list = Reservation.query.filter(Reservation.user_id==user_id)

    reservation_time_list = []
    for reservation in reservation_list:
        time_to_format = reservation.reservation_time
        formatted_time = time_to_format.strftime("%I:%M %p")
        reservation_time_list.append(formatted_time)

    #if reservation_time in time_list, need to remove it
    for reservation_time in reservation_time_list:
        if reservation_time in time_list:
            time_list.remove(reservation_time)

    return render_template("search.html", time_list=time_list)
    

@app.route("/schedule", methods=["POST"])
def search_times():
    """Select reservation time."""

    if "user_email" not in session:
        flash("You must log in to make a reservation.")

    else:
        user = User.get_by_email(session["user_email"])
        user_id = user.user_id
        reservation_list = Reservation.query.filter(Reservation.user_id==user_id)
        
        reservation_date_list = []

        for reservation in reservation_list:
            reservation_date_list.append(str(reservation.reservation_date))

        chosen_date = request.form.get("date")
        chosen_time = request.form.get("value")
        reservation_date = datetime.strptime(chosen_date, '%Y-%m-%d')
        reservation_time = datetime.strptime(chosen_time, '%I:%M %p')

        if chosen_date in reservation_date_list:
            flash("You already have a reservation on that day!")
            return redirect('/search')

        else:
            scheduled_reservation = Reservation.create(user.user_id, reservation_date, reservation_time)
            db.session.add(scheduled_reservation)
            db.session.commit()
            flash("Success! Your reservation has been made.")
            return redirect("/view")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
