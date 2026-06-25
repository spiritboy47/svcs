from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String)
    phone = Column(String)

    event_type = Column(String)

    guests = Column(Integer)

    date = Column(String)

    time_slot = Column(String)

    message = Column(String)