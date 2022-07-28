from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)

    #backref to reservations

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, email):
       return cls(email=email)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()




class Reservation(db.Model):
    """A reservation datetime."""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))    
    reservation_time = db.Column(db.String, unique=True)

    user = db.relationship("User", backref="reservations")    

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} reservation_time={self.reservation_time}>"

    @classmethod
    def create(cls, user_id, reservation_time):
       """Create and return a new reservation."""
       return cls(user_id=user_id, reservation_time=reservation_time)

    @classmethod
    def get_by_id(cls, reservation_id):
        """Return and view a single itinerary."""
        grab_reservation = Reservation.query.get(reservation_id)
        return grab_reservation

    @classmethod
    def return_reservations(cls, user_id=User.user_id):
        """Return a list of reservations associated with a user."""
        get_reservations = Reservation.query.filter_by(user_id=User.user_id).all()
        return get_reservations


def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)