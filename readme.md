## MELON RESTAURANT RESERVATION APP

Learn more about the developer: https://www.linkedin.com/in/katherineaadams/

DESCRIPTION

This app allows the user to create and store restaurant reservations. This is an initial version in the final stages of developing its MVP.

TECHNOLOGIES

I chose these technologies because I was working with limited time and was already familiar with them - with the exception of FullCalendar, which I decided to incorporate because of its features (will be utilized in Version 2.0).

- Python, Flask, PostgreSQL, SQLAlchemy
- Python Datetime
- JavaScript FullCalendar
- HTML/CSS, Bootstrap

DATABASE

I used PostgreSQL to create my very basic database. I created two classes: User and Reservation, a one-to-many relationship. 

The user class only had user_id and email as its columns, while Reservation had reservation_id, user_id (as a foreign key), reservation_date, and reservation_time.

It was useful to have the date and time listed as two columns because then I could manipulate both separately; if I wanted to create a list of times only, I didn't have to pull those times out of Datetime objects that contained both dates and times, but could simply query for reservation_time instead.

VERSION 2.0: WHAT'S NEXT?

- Fix the time list bug. Currently, the available reservation time list will exclude the time of ANY reservation stored in the database, when it should only exclude the time(s) of any reservation(s) associated with a SPECIFIC DATE. This can be fixed with SQLAlchemy queries, but I came across this bug right at the six-hour mark so it'll have to wait.

- Add password to the User class, and utilize in the login process.

- Incorporate features of FullCalendar. For example, if you click on a date on the calendar, it should autopopulate in the datetime input field. Additionally, display any reservations the user already scheduled in the calendar.

- Formatting! I did not have time to format thoroughly, but the entire site would benefit from a bit of CSS and Bootstrap magic.