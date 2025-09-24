# ERP Lite - Django ERP System

A comprehensive Educational Resource Planning (ERP) system built with Django, featuring AI-powered analytics for student performance tracking.

## Features

- **Student Admissions**: Dynamic forms for school/college students with conditional fields
- **AI Analytics**: Performance forecasting, dropout risk assessment, career recommendations
- **Dashboard**: Separate interfaces for students and staff with real-time insights
- **Fee Management**: Payment tracking and receipt generation
- **Hostel Management**: Room allocation and occupancy tracking
- **Exam Management**: Mark entry and result analysis

## Deployment to PythonAnywhere

### Prerequisites
- PythonAnywhere account
- Git repository (optional)

### Step 1: Upload Project to PythonAnywhere
1. Create a new PythonAnywhere account or log in
2. Go to the "Files" tab
3. Upload all project files, or clone from Git if available

### Step 2: Set up Virtual Environment
```bash
# In PythonAnywhere bash console
mkvirtualenv --python=/usr/bin/python3.10 erplite-env
workon erplite-env
pip install -r requirements.txt
```

### Step 3: Database Setup
```bash
cd /home/yourusername/erplite
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 4: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 5: Configure Web App
1. Go to "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration" and Python 3.10
4. Set the source code path to `/home/yourusername/erplite`
5. Set the working directory to `/home/yourusername/erplite`
6. In the WSGI configuration file, update the path:
   ```python
   import os
   import sys

   path = '/home/yourusername/erplite'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_lite.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### Step 6: Environment Variables
In PythonAnywhere, go to "Web" → "Environment variables" and add:
- `DJANGO_SECRET_KEY`: A secure random key
- `DJANGO_DEBUG`: False

### Step 7: Static Files
Make sure the static files are served correctly by updating the web app configuration.

### Step 8: Reload Web App
Click "Reload" in the Web tab to apply changes.

## Local Development

### Setup
```bash
git clone <repository-url>
cd erplite
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Default Users
- Admin: admin/admin123
- Staff: staff/staff123
- Student: student/student123

## Project Structure

```
erplite/
├── admissions/          # Student admission management
├── dashboard/           # Dashboard views for staff/students
├── exams/              # Exam and marks management
├── fees/               # Fee payment tracking
├── hostel/             # Hostel room allocation
├── main/               # User profiles and authentication
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
└── erp_lite/           # Django settings and configuration
```

## AI Features

The system includes AI-powered analytics:

- **Performance Forecasting**: Predicts final GPA based on current performance
- **Dropout Risk Assessment**: Calculates risk scores using attendance, GPA, and study habits
- **Career Recommendations**: Suggests suitable career paths
- **Intervention Suggestions**: Provides actionable recommendations for at-risk students

## License

This project is licensed under the MIT License.