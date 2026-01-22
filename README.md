# DP-COMPASS

**Digital Personal Data Protection Compliance Management & Assessment System**

A comprehensive Django web framework for managing and assessing compliance with India's Digital Personal Data Protection (DPDP) Act, 2023.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- **Role-Based Access Control** - Admin, Auditor, and Developer roles with granular permissions
- **Application Registry** - Register and track applications processing personal data
- **Compliance Audits** - Execute structured audits against DPDP checklist items
- **Real-time Scoring** - Automatic compliance score calculation
- **Remediation Tracking** - Track and manage compliance gaps
- **Report Generation** - Generate compliance reports for stakeholders
- **Modern UI** - Dark theme with glassmorphism effects

---

## 📋 Prerequisites

- Python 3.10+
- MySQL 8.0+ (optional, SQLite supported for development)
- pip

---

## 🚀 Quick Start

### 1. Clone & Setup Virtual Environment

```bash
cd /path/to/DPPP
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

**Minimum `.env` configuration:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
USE_SQLITE=True  # Set to False for MySQL
```

### 4. Initialize Database

```bash
python manage.py migrate
python manage.py load_checklist    # Load DPDP compliance checklist
python manage.py load_sample_data  # Load demo data (optional)
```

### 5. Run Development Server

```bash
python manage.py runserver 8001
```

Access at: **http://127.0.0.1:8001**

---

## 👤 Default User Accounts

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | `admin` | `admin123` | Full system access |
| Auditor | `auditor1` | `auditor123` | Execute audits, view compliance |
| Developer | `developer1` | `developer123` | View applications & results |

> ⚠️ **Change default passwords in production!**

---

## 📁 Project Structure

```
DPPP/
├── dp_compass/              # Django project configuration
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI deployment
├── apps/
│   ├── core/                # Base models, dashboard views
│   ├── users/               # Authentication & user management
│   ├── audits/              # Compliance audit functionality
│   ├── compliance/          # Application registry & remediations
│   └── reports/             # Report generation
├── templates/               # HTML templates
├── static/                  # CSS, JavaScript, images
├── manage.py                # Django CLI
└── requirements.txt         # Python dependencies
```

---

## ⚙️ Configuration

### MySQL Database (Production)

Set in `.env`:
```env
USE_SQLITE=False
DB_NAME=dp_compass
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `USE_SQLITE` | Use SQLite instead of MySQL | `False` |
| `DB_NAME` | MySQL database name | `dp_compass` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | - |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |

---

## 📜 Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py load_checklist` | Load DPDP compliance checklist (17 sections, 8 categories, 29 items) |
| `python manage.py load_sample_data` | Load demo users, applications, and audits |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py collectstatic` | Collect static files for production |

---

## 🔒 Security Considerations

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Change all default passwords
4. Configure `ALLOWED_HOSTS` in settings
5. Use HTTPS
6. Run `python manage.py check --deploy`

---

## 📄 DPDP Act Coverage

DP-COMPASS covers key sections of the DPDP Act 2023:

- **Section 4** - Processing of Personal Data
- **Section 5** - Ground for Processing (Consent)
- **Section 6** - Legitimate Uses
- **Section 7** - Notice Requirements
- **Section 8** - Data Principal Rights
- **Section 10** - Duties of Data Principals
- **Section 11** - Obligations of Data Fiduciaries
- **Section 17** - Penalties

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Support

For issues or questions, please open an issue on the repository.
