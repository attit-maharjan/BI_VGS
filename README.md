# BI_VGS  
**Django Project for Web Application ELE-3921**

**BIVGS** is a Django-based High School Management System that redefines how academic performance is interpreted. Instead of simple grades, BIVGS delivers rich, visual narratives and AI-generated feedback—empowering students, parents, and educators alike.

---

## Features

### Role-Based Dashboards
Tailored interfaces for:
- Admin
- Principal
- Vice Principal
- Head of Department (HOD)
- Teachers
- Students
- Parents

### Visual Performance Reports
- Charts, grade bands, and comparative insights replace raw scores.

### AI-Powered Feedback
- Smart, contextual comments based on performance vs. class averages.

### Real-Time Customization
- School logos, profiles, and settings can be updated live.

### Downloadable Reports
- Print-ready visual narratives for student performance.

---

## User Roles

- Administrator  
- Principal / Vice Principal  
- Head of Department (HOD)  
- Subject & Classroom Teachers  
- Students  
- Parents  

Each role gets a unique dashboard and access level tailored to their responsibilities.

---

## Screens & Flows (Demo Highlights)

### Welcome Page
- Public access to About, Terms, Privacy, Contact
- Option to "Continue without logging in"

### School Profile
- Admin can set:
  - School name, logo, motto
  - Address and contact info
  - Custom per-school database instance

### Admin Panel
- Register/edit users
- Assign/unassign roles
- Update logos and school settings instantly

### Student Dashboard
- Subjects, grades, exam schedules
- Class average comparisons
- Grade distribution charts

### Teacher Tools
- Enter and manage exam scores
- View subject performance insights
- Understand class distribution

### Principal / Vice Principal Analytics
- View all students
- Filter by: Gender, Grade Level, Department, Performance
- Access global school stats

### HOD View
- Department-specific student lists
- Auto-generated feedback (e.g., "You are above class average of 67.66. Keep on going.")

---

## Key Technologies

- **Backend**: Django, PostgreSQL  
- **Frontend**: Django Templates, Chart.js/D3.js  
- **AI Comments**: Rule-based generation (with ML-ready structure)  
- **Authentication**: Role-Based Access Control (RBAC)  

---

## Installation

1. **Extract the Zip Archive**  
   - Unzip `BIVGS.zip` to get the main project folder named `BIVGS`.

2. **Navigate to the Root Directory**  
   - Open Command Prompt (Windows) or Terminal (Mac/Linux).  
   - Navigate into the `BIVGS` folder where `manage.py` is located.

3. **Create and Activate Virtual Environment (Recommended)**  
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Development Server**  
   ```bash
   python manage.py runserver
   ```
   Access the app via browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Authentication Notes

- You can access the app without logging in via the guest link on the login page.  
- For role-based testing, use the following credentials:

---

## User Roles and Login Credentials

### Admin Role
- Superuser Login  
- **Email**: `sales@walsoftcomputers.com`  
- **Password**: (shared privately)

### Teacher Role

#### Classroom Teachers
- Emails:
  - `naomi_bruno@testteacher.no`
  - `lydia_canova@testteacher.no`
  - `joanna_eriksen@testteacher.no`
  - `abigail_fiva@testteacher.no`
- Password: `@0BusiaKenya`

#### Other Teacher Subroles

- **Principals**:
  - `simon_galle@testteacher.no`
- **Vice Principals**:
  - `benny_geys@testteacher.no`
- **HODs**:
  - `anna_nerstad@testteacher.no`
- **Subject Teachers**:
  - `mary_warlop@testteacher.no`

- Password for all: `@0BusiaKenya`

### Parent Role

#### Parents with One Child
- Email: `parker_eide@inbox.com`
- Password: `@0BusiaKenya`

#### Parents with Two or More Children
- Emails:
  - `bailey_walekhwa@yahoo.com`
  - `elliot_kedibone@aol.com`
- Password: `@0BusiaKenya`

### Student Role

- Example: `nathan_kowalski@bivgs.com` (class group: 2025-G9)
- Password for all students: `@0BusiaKenya`

---

## File Structure & Notes

- **Main Project Folder**: `BIVGS`  
- **Dependencies**: `requirements.txt`  
- **Virtual Environment**: Not included (`venv`)  
- **Database**: SQLite (for development/testing)  
- **Production**: PostgreSQL planned  
- **Extensibility**: Project is modular and scalable  

---

## Useful Commands

```bash
# Start Django Shell
python manage.py shell

# Manage Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py flush

# Load Sample Data
python manage.py loaddata data_dump.json
```

---

## License

This project is licensed under the **MIT License**.

---

## Contributing

Pull requests and suggestions are welcome.  
For major changes, please open an issue first to discuss what you'd like to change.

---

## Contact

For inquiries, reach out via the Contact page on the live demo or open an issue here on GitHub.

---

**BIVGS bridges the gap between raw grades and real understanding—turning data into dialogue.**
