# Campus Lost & Found Portal

A complete, production-ready web application built for a college campus environment allowing students to easily report lost items and post found items.

## 🚀 Features

*   **User & Admin Roles**: Complete Role-Based Access Control protecting routes appropriately.
*   **Item Management**: Add items (lost/found) with details, category, and images.
*   **Dynamic Status Updates**: Easily mark an item as Lost, Found, or Claimed.
*   **Advanced Search & Filters**: Find items fast using keywords, category filtering, and status filtering.
*   **Modern Premium UI**: Built with a "dark glassmorphism" aesthetic, providing a responsive and beautiful web experience.
*   **Security**: Encrypted passwords (`werkzeug.security`), safe file upload limits.

## 🛠️ Technology Stack

*   **Backend**: Python Flask 3.0.0
*   **Database**: MySQL Server (via PyMySQL adapter) & Flask-SQLAlchemy (ORM)
*   **Authentication**: Flask-Login
*   **Frontend**: HTML5, CSS3, JavaScript ES6 

## 📋 Setup & Run Instructions

To run this project locally, execute the following steps exactly:

1.  **Start Your MySQL Server**
    *   Ensure MySQL is running on your machine natively or via XAMPP/WAMP.
    *   Ensure your MySQL Username is **`root`** and Password is **`root`**.

2.  **Create a Virtual Environment & Activate (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate 
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Required Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database Automation**
    *   This script connects to your MySQL instance directly and establishes the `lost_and_found_db` database automatically!
    ```bash
    python create_mysql_db.py
    ```

5.  **Run the Server**
    *   Execute `app.py`. This connects to the generated DB, creates all schema tables mapping the application architecture natively, and initiates an automatic global admin account.
    ```bash
    python app.py
    ```

6.  **Access the Portal**
    *   Open your Browser and browse to: `http://localhost:5000`
    *   **Default Admin Account:** 
        *   Email: `admin@college.edu`
        *   Password: `admin`

## 🧪 Testing

The system includes automated tests suitable for educational validation. To execute:
```bash
python -m unittest test_app.py
```
