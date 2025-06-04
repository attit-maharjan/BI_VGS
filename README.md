# BI_VGS
Django project for Web application ELE-3921

**BIVGS** is a Django-based High School Management System that redefines how academic performance is interpreted. Instead of simple grades, BIVGS delivers rich, visual narratives and AI-generated feedback—empowering students, parents, and educators alike.

## 🚀 Features

- 🎓 **Role-Based Dashboards**  
  Tailored interfaces for Admin, Principal, Vice Principal, HOD, Teachers, Students, and Parents.

- 📊 **Visual Performance Reports**  
  Charts, grade bands, and comparative insights replace raw scores.

- 🤖 **AI-Powered Feedback**  
  Smart, contextual comments based on performance vs. class averages.

- ⚙️ **Real-Time Customization**  
  School logos, profiles, and settings can be updated live.

- 📥 **Downloadable Reports**  
  Print-ready visual narratives for student performance.

---

## 🔐 User Roles

- **Administrator**
- **Principal / Vice Principal**
- **Head of Department (HOD)**
- **Subject & Classroom Teachers**
- **Students**
- **Parents**

Each role gets a unique dashboard and access level tailored to their responsibilities.

---

## 📷 Screens & Flows (Demo Highlights)

### 🏠 Welcome Page

- Public access to **About**, **Terms**, **Privacy**, **Contact**
- Option to _"Continue without logging in"_

### 🏫 School Profile

- Admin can set:
  - School name, logo, motto
  - Address and contact info
- Custom per-school database instance

### 👤 Admin Panel

- Register/edit users
- Assign/unassign roles
- Update logos and school settings instantly

### 🎓 Student Dashboard

- Dashboard with:
  - Subjects, grades, exam schedules
  - Class average comparisons
  - Grade distribution charts

### 🧑‍🏫 Teacher Tools

- Enter and manage exam scores
- View subject performance insights
- Understand class distribution

### 📈 Principal / VP Analytics

- View all students
- Filter by:
  - Gender, Grade Level, Department, Performance
- Access global school stats

### 📚 HOD View

- Department-specific student lists
- Auto-generated feedback like:  
  _"You are above class average of 67.66. Keep on going."_

---

## 💡 Key Technologies

- **Backend**: Django, PostgreSQL
- **Frontend**: Django templates, Chart.js/D3.js (for visualizations)
- **AI Comments**: Rule-based generation (with ML-ready structure)
- **Auth**: Role-based access control (RBAC)

---

## 📦 Installation 

Setup instructions for local development and deployment
1.	Extract the Zip Archive
 •	Unzip BIVGS.zip to get the main project folder named BIVGS.
2.	Navigate to the Root Directory
 •	Open Command Prompt (Windows) or Terminal (Mac/Linux).
 •	Navigate into the BIVGS folder where manage.py is located.
3.	Create and Activate Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
4.	Install Dependencies
pip install -r requirements.txt
5.	Run the Development Server
python manage.py runserver
Access the app via browser: http://127.0.0.1:8000
________________________________________
🔐 Authentication Notes
•	You can access the app without logging in by using the link labeled accordingly on the login page.
•	For role-based testing, use the following credentials:
________________________________________
🎭 User Roles and Login Credentials
1. Admin Role
•	Login as Superuser :
•	Example Email:sales@walsoftcomputers.com
Password: (Shared privately)
•	To find all superusers via Django shell________________________________________
2. Teacher Role
a. Classroom Teachers
These have full dashboards available.
•	Emails:
naomi_bruno@testteacher.no  
lydia_canova@testteacher.no  
joanna_eriksen@testteacher.no  
abigail_fiva@testteacher.no
•	Password: @0BusiaKenya
•	To list Classroom Teachers via Django shell:
b. Other Subroles 
Subroles:
•	Principal
•	Vice Principal
•	Head of Department (HOD)
•	Subject Teacher
•	Example Emails:
PRINCIPALS:- simon_galle@testteacher.no

VICE PRINCIPALS:- benny_geys@testteacher.no

HODS:- anna_nerstad@testteacher.no

SUBJECT TEACHERS:
- mary_warlop@testteacher.no
•	Password for All: @0BusiaKenya
•	To list teachers by subrole via Django shell:
3. Parent Role
a. Parents with One Child
•	Sample Email:
parker_eide@inbox.com
•	Password: @0BusiaKenya
•	To find more parents with one child:
b. Parents with Two or More Children
•	Example Emails:
bailey_walekhwa@yahoo.com  
elliot_kedibone@aol.com
•	Password: @0BusiaKenya
•	To find more such parents:
________________________________________
4. Student Role
•	One student per class group: Example:
2025-G9: nathan_kowalski@bivgs.com
•	Password for all students: @0BusiaKenya
•	To fetch one student per class group via Django shell:

📁 File Structure & Other Notes
•	Main Project Folder: BIVGS
•	Requirements File: requirements.txt – contains all dependencies.
•	Virtual Environment: Not included (venv) for portability.
•	Database: SQLite (used for development/testing).
•	Future Plans: PostgreSQL for production.
•	Extensibility: You can continue building features for current roles.
________________________________________
🛠️ Useful Commands
•	Start Django Shell:
python manage.py shell
•	Check Migrations:
python manage.py makemigrations
python manage.py migrate


---

## 📄 License

[MIT License](LICENSE)

---

## 🙌 Contributing

Pull requests and suggestions welcome. For major changes, open an issue first to discuss what you’d like to change.

---

## 📞 Contact

For inquiries, reach out via the **Contact** page on the live demo or open an issue here on GitHub.

---

> **BIVGS** bridges the gap between raw grades and real understanding—turning data into dialogue.

