# Smart Password Manager Web <sup>v2.0.3</sup>

---

**Web-based smart password manager with deterministic password generation. Generate, manage, and retrieve passwords without storing them. Your secret phrase never leaves your browser.**

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager-web)](https://github.com/smartlegionlab/smart-password-manager-web)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager-web)](https://github.com/smartlegionlab/smart-password-manager-web/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager-web)](https://github.com/smartlegionlab/smart-password-manager-web/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager-web?style=social)](https://github.com/smartlegionlab/smart-password-manager-web/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager-web?style=social)](https://github.com/smartlegionlab/smart-password-manager-web/network/members)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-password-manager-web/blob/master/DISCLAIMER.md)

---

## 🔄 Important: Breaking Change from v1.x.x

> **⚠️ This release (v2.0.3) uses a completely redesigned cryptographic algorithm that is NOT backward compatible with v1.x.x**

### What changed:

- The core password generation algorithm has been completely redesigned
- **All generation now happens in your browser** — secret never leaves your device
- **Cross-platform compatibility** — same passwords as Python, Go, Kotlin, JS versions
- Smart passwords created with v1.3.7 or earlier **cannot be regenerated** using v2.0.3
- Existing password entries in the database will produce **different passwords** if regenerated

### What you need to do:

1. **Before upgrading** — retrieve and save all your existing passwords from the old version
2. **After upgrading** — recreate each password using the same secret phrases + lengths
3. **Update** your passwords on all websites/services

**No automatic migration** — you must manually regenerate every password.

📖 **Full migration instructions** → see [Migration Section](#migration-section)

---

## Core Principles

- **Zero-Password Storage**: No passwords are ever stored or transmitted
- **Deterministic Regeneration**: Passwords are recreated identically from your secret phrase
- **Metadata Management**: Store only descriptions and verification keys
- **Client-Side Generation**: All cryptographic operations happen in your browser
- **Cross-Platform**: Same passwords as Python, Go, Kotlin, JS implementations
- **On-Demand Discovery**: Passwords exist only when you generate them

## Key Features

- **Smart Password Generation**: Deterministic from secret phrase
- **Client-Side Processing**: Secret phrase never leaves your browser
- **Cross-Platform Compatible**: Same passwords as desktop, CLI, and mobile apps
- **Public Key Verification**: Verify secret knowledge without exposure
- **Web-Based Interface**: Access from any device with a browser
- **Secure Input**: Hidden secret phrase entry with show/hide toggle
- **Copy to Clipboard**: One-click password copying
- **Export/Import**: Backup and restore your password metadata
- **User Authentication**: Secure login with Django
- **PostgreSQL Backend**: Reliable data storage

## Security Model

- **Proof of Knowledge**: Public keys verify secrets without exposing them
- **Deterministic Security**: Same secret + length = same password, always
- **Metadata Separation**: Non-sensitive data stored on server
- **Local Processing**: Secret and password never leave your browser
- **No Recovery Backdoors**: Lost secret = permanently lost access (by design)

---

## Research Paradigms & Publications

- **[Pointer-Based Security Paradigm](https://doi.org/10.5281/zenodo.17204738)** - Architectural Shift from Data Protection to Data Non-Existence
- **[Local Data Regeneration Paradigm](https://doi.org/10.5281/zenodo.17264327)** - Ontological Shift from Data Transmission to Synchronous State Discovery

---

## Technical Foundation

Powered by **[smartpasslib-js](https://github.com/smartlegionlab/smartpasslib-js)** — JavaScript implementation of deterministic password generation.

**Key derivation (same as Python/Go/Kotlin versions):**

| Key Type    | Iterations | Purpose                                               |
|-------------|------------|-------------------------------------------------------|
| Private Key | 30         | Password generation (never stored, never transmitted) |
| Public Key  | 60         | Verification (stored on server)                       |

**Character Set:** `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&*-_`

## Quick Start

### Prerequisites
- **Python 3.8+** 
- **PostgreSQL**

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
git clone https://github.com/smartlegionlab/smart-password-manager-web.git
cd smart-password-manager-web

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install PostgreSQL adapter
pip install psycopg2-binary
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

# Email settings
EMAIL_ON=True
EMAIL_HOST=smtp.server.com
EMAIL_HOST_USER=email@example.com
EMAIL_HOST_PASSWORD=password
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

### Migrating from v1.x.x to v2.0.3

**⚠️ Before upgrading — follow these steps carefully**

**Step 1: Document your existing passwords**
- Open your current Smart Password Manager Web (v1.3.7 or earlier)
- For each password entry, retrieve the actual password using your secret phrase
- Save passwords in a secure temporary location (e.g., encrypted note)

**Step 2: Backup your database (optional)**
```bash
pg_dump -U postgres smart_password_manager_db > backup_v1.sql
```

**Step 3: Upgrade to v2.0.3**
```bash
# Pull latest code
git pull origin master

# Apply migrations (if any)
python manage.py migrate
```

**Step 4: Migrate your data**
- Delete old password entries and add new ones manually using the same secret phrases

**Step 5: Update passwords in all your services**
- After regenerating passwords with v2.0.3, update them in each website/service
- Test login before removing old access

**Important**: v1.x.x and v2.0.3 passwords are NOT compatible. You must regenerate all passwords.

---

## What's New in v2.0.3

### Complete Rewrite with Client-Side Generation

- **Secret phrase never leaves your browser** — all cryptographic operations happen locally
- **Cross-platform compatible** — same passwords as desktop, CLI, and mobile apps
- **Server stores only metadata** — description, length, public key
- **Public key verification** — secret verified locally without transmission
- **No Python crypto dependencies** — pure JavaScript in the browser

### Security Enhancements

- **Minimum 12 characters** enforced for secret phrases
- **Minimum password length** set to 12 characters (default 16)
- **Client-side validation** with visual feedback
- **Strong secret examples** in the UI

## Interface Preview

![Web Interface](https://github.com/smartlegionlab/smart-password-manager-web/raw/master/data/images/smart_password_manager.png)

## Architecture

### Technology Stack
- **Backend**: Django 5.2+ (only for auth, metadata storage, and session management)
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Client Crypto**: smartpasslib-js (Web Crypto API)

### Security Requirements

| Field           | Minimum  | Default  | Maximum   |
|-----------------|----------|----------|-----------|
| Secret phrase   | 12 chars | -        | unlimited |
| Password length | 12 chars | 16 chars | 100 chars |
| Description     | 1 char   | -        | 255 chars |

## Security Requirements

### Secret Phrase
- **Minimum 12 characters** (enforced)
- Case-sensitive
- Use mix of: uppercase, lowercase, numbers, symbols, emoji, or Cyrillic
- Never store digitally
- **NEVER use your password description as secret phrase**

### Strong Secret Examples
```
✅ "MyCatHippo2026"          — mixed case + numbers
✅ "P@ssw0rd!LongSecret"     — special chars + numbers + length
✅ "КотБегемот2026НаДиете"   — Cyrillic + numbers
✅ "GitHubPersonal2026!"     — description + extra chars (not description alone)
```

### Weak Secret Examples (avoid)
```
❌ "GitHub Account"          — using description as secret (weak!)
❌ "password"                — dictionary word, too short
❌ "1234567890"              — only digits, too short
❌ "qwerty123"               — keyboard pattern
❌ Same as description       — never use the same value as password description
```

## Cross-Platform Compatibility

Smart Password Manager Web produces **identical passwords** to:

| Platform   | Application                                                                                                               |
|------------|---------------------------------------------------------------------------------------------------------------------------|
| Desktop    | [Desktop Manager](https://github.com/smartlegionlab/smart-password-manager-desktop)                                       |
| CLI        | [CLI PassMan](https://github.com/smartlegionlab/clipassman) / [CLI PassGen](https://github.com/smartlegionlab/clipassgen) |
| Android    | [Android Manager](https://github.com/smartlegionlab/smart-password-manager-android)                                       |
| Python     | [smartpasslib](https://github.com/smartlegionlab/smartpasslib)                                                            |
| Go         | [smartpasslib-go](https://github.com/smartlegionlab/smartpasslib-go)                                                      |
| Kotlin     | [smartpasslib-kotlin](https://github.com/smartlegionlab/smartpasslib-kotlin)                                              |

## Ecosystem

This web application is part of a comprehensive suite:

### Core Libraries
- **[smartpasslib](https://github.com/smartlegionlab/smartpasslib)** - Python implementation
- **[smartpasslib-js](https://github.com/smartlegionlab/smartpasslib-js)** - JavaScript implementation
- **[smartpasslib-kotlin](https://github.com/smartlegionlab/smartpasslib-kotlin)** - Kotlin implementation
- **[smartpasslib-go](https://github.com/smartlegionlab/smartpasslib-go)** - Go implementation

### Applications
- **[Desktop Manager](https://github.com/smartlegionlab/smart-password-manager-desktop)** - Cross-platform desktop application
- **[CLI PassGen](https://github.com/smartlegionlab/clipassgen/)** - Command-line password generator
- **[CLI PassMan](https://github.com/smartlegionlab/clipassman/)** - Console-based password manager
- **[Web Manager](https://github.com/smartlegionlab/smart-password-manager-web)** - Web interface (this project)
- **[Android Manager](https://github.com/smartlegionlab/smart-password-manager-android)** - Mobile Android app

## Version History

| Version          | Generation  | Status                   | Migration Required     |
|------------------|-------------|--------------------------|------------------------|
| v1.3.7 and below | Server-side | ❌ Deprecated/Unsupported | Must migrate to v2.0.3 |
| v2.0.3+          | Client-side | ✅ Current                | N/A                    |

## License

**BSD 3-Clause License**

Copyright (©) 2026, [Alexander Suvorov](https://github.com/smartlegionlab)

## Author

**Alexander Suvorov** - [GitHub](https://github.com/smartlegionlab)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-web/issues)
- **Documentation**: This README

---

