# Migration Guide: v1.x.x to v2.x.x

## ⚠️ Breaking Change Notice

**Smart Password Manager Web v2.x.x is NOT backward compatible with v1.x.x**

Passwords generated with older versions cannot be regenerated using v2.x.x due to fundamental changes in the deterministic generation algorithm.

---

## Why the change?

**v2.x.x introduces fundamental improvements:**

- **Client-side generation** — secret never leaves your browser
- **Cross-platform determinism** — same passwords as Python, Go, Kotlin, JS, C#
- **Decentralized by design** — no central servers, no cloud dependency
- **Stronger cryptographic algorithm** — based on SHA-256
- **Better cross-platform consistency** — identical results across all platforms

---

## What changed:

- Password generation moved from server to **browser (client-side)**
- Core algorithm now uses **SHA-256**
- Secret phrase **never leaves your device**
- Server stores only metadata (description, length, public key)
- Old passwords **cannot be regenerated** with new version

---

## Migration Steps

### Step 1: Retrieve existing passwords

For each password entry, generate the actual password using your secret phrase with the old version of the application.

### Step 2: Upgrade to v2.x.x

Pull the latest code and apply migrations:

```bash
git pull origin master
python manage.py migrate
```

### Step 3: Generate new passwords

Using the **same secret phrases and lengths**, generate new passwords with the new version.

### Step 4: Update your services

Replace old passwords with newly generated ones on each website/service.

### Step 5: Verify

- Log in using new passwords
- Confirm regeneration works

---

## Important Notes

- **No automatic migration** — manual regeneration required for each password
- **Your secret phrases remain the same** — only generated passwords change
- Old passwords are not compatible with new version
- Test with non-essential accounts first

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-web/issues)

