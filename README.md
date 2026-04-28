# Smart Password Manager Web <sup>v2.1.1</sup>

---

**Web-based smart password manager with deterministic password generation. Generate, manage, and retrieve passwords without storing them. Your secret phrase never leaves your browser.**

**Decentralized by Design**: Unlike traditional password managers that store encrypted vaults on central servers, 
smartpasslib stores nothing. Your secrets never leave your device. Passwords are regenerated on-demand — 
**no cloud, no database, no trust required**. The server stores only metadata (description, length, public key) 
for verification — never your secret phrase or actual password. Internet connection is only needed to load the 
page and sync metadata; all cryptographic operations happen locally in your browser.

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

## 🔄 Breaking Change (v2.x.x)

> **⚠️ This version is NOT backward compatible with v1.x.x**

Passwords generated with older versions **cannot be regenerated** with v2.x.x.

📖 **Full migration instructions** → see [MIGRATION.md](https://github.com/smartlegionlab/smart-password-manager-web/blob/master/MIGRATION.md)

---

## Core Principles

- **Zero-Storage Security**: No passwords or secret phrases are ever stored or transmitted
- **Decentralized Architecture**: No central servers, no cloud dependency, no third-party trust required
- **Deterministic Regeneration**: Passwords are recreated identically from your secret phrase
- **Metadata Only**: Store only descriptions and verification keys
- **Client-Side Generation**: All cryptographic operations happen in your browser
- **On-Demand Discovery**: Passwords exist only when you generate them

## Key Features

- **Decentralized & Serverless**: No central database, no cloud lock-in, complete user sovereignty
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
- **Decentralized Trust**: No third party needed — you control your secrets completely
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

**Key derivation (same as Python/Go/Kotlin/C# versions):**

| Key Type    | Iterations | Purpose                                               |
|-------------|------------|-------------------------------------------------------|
| Private Key | 30         | Password generation (never stored, never transmitted) |
| Public Key  | 60         | Verification (stored on server)                       |

**Character Set:** `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&*-_`

**Decentralized Architecture**:
- No central authority required
- Metadata can be synced via any channel
- Your security depends only on your secret phrase

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

## Security Requirements

### Secret Phrase
- **Minimum 12 characters** (enforced)
- Case-sensitive
- Use mix of: uppercase, lowercase, numbers, symbols, emoji, or Cyrillic
- Never store digitally
- **NEVER use your password description as secret phrase**

### Strong Secret Examples
```
✅ "MyStrongSecretPhrase2026!"   — mixed case + numbers + symbols
✅ "P@ssw0rd!LongSecret"         — special chars + numbers + length
✅ "КотБегемот2026НаДиете"       — Cyrillic + numbers
```

### Weak Secret Examples (avoid)
```
❌ "GitHub Account"              — using description as secret (weak!)
❌ "password"                    — dictionary word, too short
❌ "1234567890"                  — only digits, too short
❌ "qwerty123"                   — keyboard pattern
❌ Same as description           — never use the same value as password description
```

### Decentralized Nature

**There is no "forgot password" button.** This is by design:

- No central server can reset your passwords
- No support team can recover your access
- Your secret phrase is the ONLY key

**This is the price of true decentralization** — you are completely in control.

## Interface Preview

![Web Interface](https://github.com/smartlegionlab/smart-password-manager-web/raw/master/data/images/smart_password_manager.png)

## Architecture

### Technology Stack
- **Backend**: Django 5.2+ (only for auth, metadata storage, and session management)
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Client Crypto**: smartpasslib-js (Web Crypto API)

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
| C#         | [smartpasslib-csharp](https://github.com/smartlegionlab/smartpasslib-csharp)                                              |

## Ecosystem

**Core Libraries:**
- **[smartpasslib](https://github.com/smartlegionlab/smartpasslib)** - Python
- **[smartpasslib-js](https://github.com/smartlegionlab/smartpasslib-js)** - JavaScript
- **[smartpasslib-kotlin](https://github.com/smartlegionlab/smartpasslib-kotlin)** - Kotlin
- **[smartpasslib-go](https://github.com/smartlegionlab/smartpasslib-go)** - Go
- **[smartpasslib-csharp](https://github.com/smartlegionlab/smartpasslib-csharp)** - C#

**CLI Applications:**
- **[CLI Smart Password Manager (Python)](https://github.com/smartlegionlab/clipassman)**
- **[CLI Smart Password Generator (Python)](https://github.com/smartlegionlab/clipassgen)**
- **[CLI Smart Password Manager (C#)](https://github.com/smartlegionlab/SmartPasswordManagerCsharpCli)**
- **[CLI Smart Password Generator (C#)](https://github.com/smartlegionlab/SmartPasswordGeneratorCsharpCli)** 

**Desktop Applications:**
- **[Desktop Smart Password Manager (Python)](https://github.com/smartlegionlab/smart-password-manager-desktop)**
- **[Desktop Smart Password Manager (C#)](https://github.com/smartlegionlab/SmartPasswordManagerCsharpDesktop)**

**Other:**
- **[Web Smart Password Manager](https://github.com/smartlegionlab/smart-password-manager-web)** (this)
- **[Android Smart Password Manager](https://github.com/smartlegionlab/smart-password-manager-android)**

## Version History

| Version          | Generation  | Status                   | Migration Required     |
|------------------|-------------|--------------------------|------------------------|
| v1.3.7 and below | Server-side | ❌ Deprecated/Unsupported | Must migrate to v2.x.x |
| v2.x.x+          | Client-side | ✅ Current                | N/A                    |

## License

**BSD 3-Clause License**

Copyright (©) 2026, [Alexander Suvorov](https://github.com/smartlegionlab)

## Author

**Alexander Suvorov** - [GitHub](https://github.com/smartlegionlab)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-web/issues)
- **Documentation**: This [README](https://github.com/smartlegionlab/smart-password-manager-web/blob/master/README.md)

