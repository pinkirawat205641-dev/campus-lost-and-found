# Lost & Found Portal for College Campus

This plan outlines the steps to build a complete, production-ready web application for a campus Lost & Found system. The platform will allow students to report lost items, post found items, search, and update item statuses dynamically. Based on the requirements, we'll use Python Flask for the backend, SQLite for the database, and HTML/CSS/JavaScript for a modern, responsive frontend.

## User Review Required

> [!IMPORTANT]
> Please review the proposed architecture, database schema, and planned features. Let me know if you approve this approach or if you would like me to adjust any specific aspect before I begin coding.

## Proposed Changes

We will develop this application systematically in the following phases:

### 1. System Setup & Architecture
**Stack:** Flask, Flask-SQLAlchemy (ORM), Flask-Login (Auth), Werkzeug (Security), Jinja2 (Templates).
- Setup the project skeleton.
- Initialize `app.py` for routing and configurations.
- Create `uploads/` directory for saving uploaded item images.
- Create `static/` directory for CSS and JS assets.
- Create `templates/` directory for HTML files.

### 2. Database Schema Design (SQLite)
We will use SQLAlchemy to abstract the database operations.
*   **Users Table:**
    *   `id` (PK), `name`, `email` (Unique), `password_hash`
*   **Items Table:**
    *   `id` (PK)
    *   `title`, `description`, `category` (Electronics, Books, Accessories, Others)
    *   `status` (Lost, Found, Claimed)
    *   `image_path` (storing relative path or filename)
    *   `date_reported`
    *   `location`
    *   `contact_info`
    *   `user_id` (FK to Users)

### 3. Backend Implementation (Flask)
- Define DB models within `app.py` or `models.py`.
- Create Authentication Routes: Register, Login, Logout.
- Create Item Management Routes:
    - `/` (Home page with items, search and filter capability)
    - `/item/add` (Form to post a new item)
    - `/item/<id>` (Detailed view of a specific item)
    - `/item/<id>/update_status` (Update item status to Found/Claimed)
- Implement secure file upload functionality (allowed extensions: png, jpg, jpeg).

### 4. Frontend Construction & Styling
Design a modern, premium UI with bright aesthetics and smooth animations.
- **base.html:** Main layout, responsive navigation bar.
- **index.html:** Interactive grid/flexbox based list showcasing item cards with filtering UI.
- **login.html & register.html:** Clean access forms.
- **add_item.html:** User-friendly form with image upload.
- **item_detail.html:** Dedicated page showcasing full item info with status update buttons.
- **CSS:** Custom CSS file providing best practices in modern web design, responsive layouts, and dynamic elements.

### 5. Testing & Validation
We will implement automated testing using standard libraries to ensure functionality.
- Form validation tests.
- Image upload and routing tests.
- Database relationship/schema tests.

### 6. Final Project Documentation
A comprehensive `README.md` will be provided detailing:
- Project Overview and architecture.
- Setup steps and running the project locally.
- Test report.

## Open Questions

> [!NOTE]
> 1. Do you want basic email session validation, or is an arbitrary email string okay for simple signups? (I will use normal string emails by default)
> 2. By default, I will restrict the "status update" feature so that only the user who created the post can mark it as 'Claimed'. Is that fine?

## Verification Plan

### Automated Tests
- Create test file (e.g. `test_app.py`) to systematically execute unit tests as requested.

### Manual Verification
- We will execute the Flask local testing server and use the browser tool (or guide you to) to verify the UI workflows (Reg/Login -> Post Item -> Upload Image -> Search -> Status Update).
