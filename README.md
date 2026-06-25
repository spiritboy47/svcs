# SVCS Catering — FastAPI Booking + Admin Dashboard

A FastAPI web application for **Siddi Vinayaka Catering Service (SVCS)**.

- Public pages (Home, About, Services, Menu, Gallery, Alumni, Contact)
- Catering **booking form** with validation
- Stores bookings in **SQLite**
- Sends **HTML email confirmation** to the customer
- Admin portal for **login / view / edit / delete** bookings (JWT in an HttpOnly cookie)

---

## Features

- ✅ Booking submission with server-side validation
- ✅ Email confirmation after booking (SMTP via Gmail)
- ✅ Admin dashboard showing all bookings
- ✅ Admin can edit or delete bookings
- ✅ Jinja2 templates + static assets
- ✅ Swagger docs available at `/docs`

---

## Tech Stack

- **FastAPI** (API + template rendering)
- **Jinja2** (HTML templates)
- **SQLAlchemy** (SQLite persistence)
- **python-jose** (JWT handling)
- **fastapi-mail** (email sending)

---

## Project Structure

```text
svcs/
  app/
    main.py
    core/
      config.py
      security.py
    database/
      connection.py
      models.py
    routes/
      pages.py
      booking.py
      admin.py
    services/
      email_service.py
    schemas/
      booking.py
    templates/
      *.html
    static/
      style.css
  catering.db              # SQLite file (generated/used by SQLAlchemy)
  .env                     # Environment variables (create your own)
```

---

## Requirements

- Python 3.9+ recommended

---

## Setup (Local Development)

### 1) Create a virtual environment

```bash
python -m venv .venv
```

Activate:

- Windows (PowerShell):
```bash
.venv\Scripts\Activate.ps1
```
- Windows (cmd.exe):
```bash
.venv\Scripts\activate.bat
```

### 2) Install dependencies

Install dependencies from your project (ensure you have a `requirements.txt` if present in your setup):

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, install the needed packages used by the code:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `python-dotenv`
- `python-jose`
- `fastapi-mail`

### 3) Configure environment variables

Create a `.env` file at the project root (`svcs/.env`).

Example:

```env
SECRET_KEY=change-me

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin-password

# Email (Gmail SMTP)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
```

> **Email note (important):** For Gmail, you typically must use a **Gmail App Password** (not your normal password) and ensure SMTP access is allowed.

### 4) Run the server

```bash
uvicorn app.main:app --reload
```

Then open:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc UI: `http://localhost:8000/redoc`

---

## Web Endpoints

### Public Pages
- `GET /` → `index.html`
- `GET /about` → `about.html`
- `GET /services` → `services.html`
- `GET /menu` → `menu.html`
- `GET /gallery` → `gallery.html`
- `GET /alumni` → `alumni.html`
- `GET /contact` → `contact.html`

### Booking
- `GET /booking` → booking form (`booking.html`)
- `POST /booking` → creates a booking, stores it, sends email confirmation, then re-renders the page with `success` or `error`.

**Booking fields (form):**
- `name`
- `email`
- `phone` (digits only, exactly 10 digits)
- `event_type` (allowed: `Wedding`, `Corporate`, `Birthday`)
- `guests` (must be > 0)
- `date` (YYYY-MM-DD; must be at least **3 days after today**)
- `time_slot` (allowed: `Morning`, `Afternoon`, `Night`)
- `message` (optional)

### Admin (Cookie + JWT)

Authentication:
- Login sets cookie: `access_token` (HttpOnly)
- Token is validated using `SECRET_KEY`

Admin routes:
- `GET /admin/login` → login page (`admin_login.html`)
- `POST /admin/login` → verifies admin username/password and sets cookie
- `GET /admin/dashboard` → lists all bookings (`admin_dashboard.html`)
- `GET /admin/edit/{id}` → edit page (`admin_edit_booking.html`)
- `POST /admin/edit/{id}` → updates booking
- `POST /admin/delete/{id}` → deletes booking
- `GET /admin/logout` → clears cookie and redirects to login

---

## Database

- Database: **SQLite**
- File: `catering.db`
- Table: `bookings`

Booking model fields:
- `id` (primary key)
- `name`, `email`, `phone`
- `event_type`, `guests`
- `date` (stored as `DD/MM/YYYY` string)
- `time_slot`
- `message`

The database tables are created on startup via:
- `Base.metadata.create_all(bind=engine)` in `app/main.py`

---

## Security Notes

- Admin auth uses JWT stored in an **HttpOnly cookie** (`access_token`).
- Token expires in **60 minutes**.

---

## Common Commands

Run server:
```bash
uvicorn app.main:app --reload
```

---

## Troubleshooting

1. **Email not sent**
   - Confirm `.env` values for `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_FROM`.
   - Ensure you’re using a Gmail **App Password**.

2. **Admin login fails**
   - Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`.

3. **SQLite file permissions**
   - Ensure you have write access to the project directory so `catering.db` can be created/updated.

