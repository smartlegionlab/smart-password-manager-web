# Smart Password Manager Web <sup>v2.0.1</sup>

---

**Smart Password Manager (web version)**

> **Powered by** [smartpasslib](https://github.com/smartlegionlab/smartpasslib) - The core library for deterministic password generation.

Your passwords don't need to be stored because they were never created—they already exist as mathematically valid data waiting to be discovered.

> Note: This is a production-ready password manager. For academic research on the underlying security paradigms, see [The Pointer-Based Security Paradigm](https://doi.org/10.5281/zenodo.17204738), [Local Data Regeneration Paradigm](https://doi.org/10.5281/zenodo.17264327)

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager)](https://github.com/smartlegionlab/smart-password-manager)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager)](https://github.com/smartlegionlab/smart-password-manager/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager)](https://github.com/smartlegionlab/smart-password-manager/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager?style=social)](https://github.com/smartlegionlab/smart-password-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager?style=social)](https://github.com/smartlegionlab/smart-password-manager/network/members)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-password-manager/blob/master/DISCLAIMER.md)

---

## 🔄 Important: smartpasslib v3.0.0 Breaking Change

> **⚠️ This release (v2.0.1) uses [smartpasslib](https://github.com/smartlegionlab/smartpasslib) v3.0.0, which is NOT backward compatible with v1.x.x**

### Why the change?

**Smartpasslib v3.0.0 introduces fundamental improvements:**
- **Stronger cryptographic algorithm** — enhanced deterministic generation with better entropy distribution
- **Improved performance** — faster password generation, especially for longer passwords
- **Better cross-platform consistency** — identical results guaranteed across all platforms
- **Extended character set support** — wider range of special characters for stronger passwords
- **Future-proof architecture** — easier updates and security patches

### What changed:

- The core password generation algorithm has been completely redesigned
- Smart passwords created with v1.3.7 or earlier **cannot be regenerated** using v2.0.1
- Existing password entries in the database will produce **different passwords** if regenerated with v2.0.1

### What you need to do:

1. **Before upgrading** — retrieve and save all your existing passwords from the old version
2. **After upgrading** — recreate each password using the same secret phrases + lengths
3. **Update** your passwords on all websites/services
4. **Existing database entries remain** but will generate different passwords

**No automatic migration** — you must manually regenerate every password.

📖 **Full migration instructions** → see [Migration Section](#migration-section)

---

## Quick Start

### Prerequisites
- **Python 3.8+** 
- **PostgreSQL**
- **Redis** (for Celery tasks, optional)

### Installation

#### 1. Install PostgreSQL
```bash
# Arch Linux
sudo pacman -S postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Initialize database cluster (Arch Linux)
sudo su - postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 2. Project Setup
```bash
# Clone repository
git clone https://github.com/smartlegionlab/smart-password-manager.git
cd smart-password-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install PostgreSQL adapter
pip install psycopg2-binary

# Install smartpasslib v3.0.0
pip install smartpasslib==3.0.0
```

#### 3. Database Configuration
```sql
-- Access PostgreSQL shell
sudo -u postgres psql

-- Create database
CREATE DATABASE smart_password_manager_db
    OWNER postgres
    ENCODING 'UTF-8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;
```

#### 4. Environment Configuration
Create `.env` file in project root:
```ini
# Core Settings
DJANGO_ENV=development
SECRET_KEY=your-generated-secret-key-here
DEBUG=True

# Database Settings
DB_NAME=smart_password_manager_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Optional: Redis/Celery Settings
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
```

Generate secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5. Database Migration & Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

#### 6. Run Development Server
```bash
python manage.py runserver
```

Access the application at: [http://localhost:8000](http://localhost:8000)
Admin interface: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Migration Section

### Migrating from v1.x.x to v2.0.1

**⚠️ Before upgrading — follow these steps carefully**

**Step 1: Document your existing passwords**
- Open your current Smart Password Manager Web (v1.3.7 or earlier)
- For each password entry, retrieve the actual password using your secret phrase
- Save passwords in a secure temporary location (e.g., encrypted note)

**Step 2: Backup your database (optional)**
```bash
# Dump your database before upgrading
pg_dump -U postgres smart_password_manager_db > backup_v1.sql
```

**Step 3: Upgrade to v2.0.1**
```bash
# Update smartpasslib
pip install smartpasslib==3.0.0

# Pull latest code
git pull origin master

# Apply migrations (if any)
python manage.py migrate
```

**Step 4: Migrate your data**
- Option A: Delete old password entries and add new ones manually
- Option B: Keep entries but manually verify each password (not recommended)

**Step 5: Update passwords in all your services**
- After regenerating passwords with v2.0.1, update them in each website/service
- Test login before removing old access

**Important**: v1.x.x and v2.0.1 cannot share the same password entries. Keep them completely separate or manually migrate each password.

---

## What's New in v2.0.1

### Breaking Change: smartpasslib v3.0.0

- **New cryptographic algorithm** — stronger and faster password generation
- **NOT backward compatible** with v1.x.x — all smart passwords must be regenerated
- **See migration section above** for detailed upgrade instructions

### Security Enhancements

- **Minimum 12 characters** enforced for secret phrases
- **Minimum password length** set to 12 characters (default 16)
- **Client-side validation** with visual feedback
- **Strong secret examples** in the UI

### Previous Features

- **Web-based interface** for smart password management
- **PostgreSQL backend** for reliable data storage
- **Django admin integration** for easy management
- **REST API support** for programmatic access
- **User authentication** and session management

---

## Interface Preview

![Web Interface](https://github.com/smartlegionlab/smart-password-manager/raw/master/data/images/smart_password_manager.png)
*Modern web interface for smart password management*

## Architecture

### Technology Stack
- **Backend**: Django 5.2+
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Task Queue**: Celery with Redis (optional)

### Security Requirements

| Field | Minimum | Default | Maximum |
|-------|---------|---------|---------|
| Secret phrase | 12 chars | - | 255 chars |
| Password length | 12 chars | 16 chars | 100 chars |
| Description | 1 char | - | 255 chars |

### Database Configuration
Default development credentials:
- **User**: postgres
- **Password**: postgres
- **Database**: smart_password_manager_db
- **Host**: localhost
- **Port**: 5432

---

## Version History

| Version | smartpasslib | Status | Migration Required |
|---------|--------------|--------|---------------------|
| v1.3.7 and below | v2.x.x | ❌ Deprecated/Unsupported | Must migrate to v2.0.1 |
| v2.0.1+ | v3.0.0 | ✅ Current | N/A |

---

## Smart Password Ecosystem

This web application is part of a comprehensive suite:

### Desktop Applications
- [**Desktop Manager**](https://github.com/smartlegionlab/smart-password-manager-desktop) - Cross-platform desktop application

### Console Tools
- [**CLI PassGen**](https://github.com/smartlegionlab/clipassgen/) - Command-line password generator
- [**CLI PassMan**](https://github.com/smartlegionlab/clipassman/) - Console-based password manager

### Core Technology
- [**SmartPassLib**](https://github.com/smartlegionlab/smartpasslib) - Core password generation library

---

## License

BSD 3-Clause License

Copyright (©) 2026, Alexander Suvorov

---

