# Migration Guide: v1.x.x / v2.x.x to v4.0.0

> **📌 Version Note:** Smart Password Manager Web v4.0.0 uses smartpasslib-js v4.0.0, which introduces breaking changes from all previous versions. All smartpasslib implementations (Python, JS, C#, Go, Kotlin) now share the same algorithm.

## ⚠️ Breaking Change Notice

**Smart Password Manager Web v4.0.0 is NOT backward compatible with v1.x.x or v2.x.x**

| Version    | Generation      | Status       | Why                                                              |
|------------|-----------------|--------------|------------------------------------------------------------------|
| v1.x.x     | Server-side     | ❌ Deprecated | Passwords generated on server, limited security                  |
| v2.x.x     | Client-side     | ❌ Deprecated | Fixed iterations (30/60), limited character set                  |
| **v4.0.0** | **Client-side** | ✅ Current    | Dynamic iterations (15-30/45-60), expanded charset, max security |

Passwords generated with older versions cannot be regenerated using v4.0.0 due to fundamental changes in the deterministic generation algorithm.

---

## Why the change?

**v4.0.0 introduces fundamental improvements:**

- **Dynamic iteration counts** — deterministic steps vary per secret (15-30 for private, 45-60 for public)
- **Expanded character set** — Google-compatible symbols (26 special chars + A-Z + a-z + 0-9)
- **Enhanced key derivation** — salt separation for public/private keys ("private"/"public")
- **Unified length validation** — password length must be 12-100 characters (was 12-1000)
- **Input validation** — secret phrases must be at least 12 characters (enforced)
- **Maximum security** — no secret exposure in logs or iterations
- **Cross-platform consistency** — identical algorithm with all smartpasslib implementations

---

## What changed:

| Aspect                 | v1.x.x / v2.x.x  | v4.0.0                                |
|------------------------|------------------|---------------------------------------|
| Private key iterations | Fixed 30         | Dynamic 15-30                         |
| Public key iterations  | Fixed 60         | Dynamic 45-60                         |
| Key derivation salt    | None             | "private"/"public"                    |
| Character set          | `abc...!@#$&*-_` | `!@#$%^&*()_+-=[]{};:,.<>?/A-Za-z0-9` |
| Password max length    | 1000             | 100                                   |
| Secret validation      | Min 4 chars      | Min 12 chars (enforced)               |
| Secret in iterations   | Yes (exposed)    | No (secure)                           |

---

## Database Compatibility

**The existing database is NOT compatible with v4.0.0**

Public keys stored in v1.x.x/v2.x.x databases cannot be used with v4.0.0 because:
- Iteration counts changed from fixed 60 to dynamic 45-60
- Salt "public" was added to key derivation

**Result:** Old public keys will not verify secrets. Password regeneration will fail.

**No database migration is provided** — you need to recreate entries.

---

## Migration Steps

### Step 1: Retrieve existing passwords

Before upgrading, retrieve all actual passwords using the old version:

1. Login to the old version of the web application
2. For each password entry, click "Generate" and copy the password
3. Save all passwords in a safe place

### Step 2: Backup your database

```bash
pg_dump your_database_name > backup_v2.sql
```

### Step 3: Upgrade to v4.0.0

Pull the latest code. The smartpasslib-js v4.0.0 is included automatically.

### Step 4: Clear or migrate database

Since old public keys are not compatible, you have two options:

**Option A: Start fresh (recommended)**
```bash
python manage.py flush  # Clears all data
python manage.py migrate
```

**Option B: Keep old data but handle incompatibility**
- Old entries will remain but verification will fail
- You will need to delete old entries and recreate them

### Step 5: Recreate password entries

Using the **same secret phrases and lengths**, recreate all password entries:

1. Add new entry with description
2. Enter your secret phrase (minimum 12 characters)
3. Set the same length as before
4. New password will be generated (different from old one)

### Step 6: Update your services

Replace old passwords with newly generated ones on each website/service.

### Step 7: Verify

- Log in using new passwords
- Confirm regeneration works (same secret → same password)

---

## Important Notes

- **No automatic migration** — manual password regeneration required
- **No database migration** — old public keys are incompatible
- **Your secret phrases remain the same** — use them to recreate entries
- **Secret phrases shorter than 12 characters will now be rejected**
- **Password lengths between 101 and 1000 will now be rejected**
- **Old passwords still work** on services until you change them
- Test with non-essential accounts first

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-web/issues)
- **Core Library Issues**: [smartpasslib Issues](https://github.com/smartlegionlab/smartpasslib/issues)

---

