from pydantic import BaseModel

class BookingCreate(BaseModel):
    name: str
    email: str
    phone: str
    event_type: str
    guests: int
    date: str
    message: str