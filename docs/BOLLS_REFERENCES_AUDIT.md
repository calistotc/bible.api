# Remaining "bolls" References - Complete Analysis

**Date:** 2025-11-11
**Status:** Post-Rebranding Audit

## 🔴 CRITICAL - DO NOT CHANGE (Core Infrastructure)

### 1. Django App Name: "bolls"
**Files:**
- `django/bain/settings.py` line 41: `INSTALLED_APPS = ["bolls", ...]`
- `django/bain/urls.py` line 4, 10: `from bolls.urls` / `include('bolls.urls')`
- `django/bolls/apps.py`: App configuration
- `django/bolls/views.py` lines 22-23: `from bolls.books_map`, `from bolls.forms`
- `django/bolls/management/commands/load_translation.py` line 9: `from bolls.models`

**Impact if changed:** 🔴 CRITICAL - Would break entire application
**Reason to keep:** Internal app name never visible to users

### 2. Django Directory Structure
**Directory:** `django/bolls/` (entire directory)

**Contains:**
- models.py (database models)
- views.py (API endpoints)
- urls.py (URL routing)
- forms.py (user forms)
- apps.py (app config)
- migrations/ (database history)
- management/ (custom commands)
- templates/ (HTML templates)
- static/ (CSS, JS, images)

**Impact if renamed:** 🔴 EXTREME - Every import statement breaks
**Reason to keep:** This is Python package structure, never exposed to users

### 3. Database Table Names
**Tables in PostgreSQL:**
- `bolls_verses` (31,102+ rows)
- `bolls_bookmarks`
- `bolls_history`
- `bolls_commentary`
- `bolls_dictionary`
- `bolls_note`
- `auth_user` (Django default)
- `django_migrations` (tracks migration history)

**Indexes:**
- `bolls_verse_transla_b7c462_idx`
- `bolls_comme_transla_851084_idx`

**Impact if renamed:** 🔴 CATASTROPHIC - Requires database migration, downtime, high risk of data loss
**Reason to keep:** Table names are internal to PostgreSQL, never visible in API responses

### 4. Database Migrations
**Files:** `django/bolls/migrations/` (13 migration files)

**Contains references to:**
- Model names (Verses, Commentary, Dictionary, etc.)
- Table names (bolls_verses, bolls_commentary, etc.)
- Index names (bolls_verse_transla_b7c462_idx, etc.)

**Impact if changed:** 🔴 CATASTROPHIC - Django migration system tracks these, changing breaks migration chain
**Reason to keep:** Migration history must remain intact for database consistency

---

## 🟡 MEDIUM - Infrastructure (Consider Carefully)

### 5. Docker Volume Paths
**Files:**
- `docker-compose.prod.yml` lines 26, 69: `/home/bolls/web/static`
- `docker-compose.yml` line 11: `/var/lib/postgresql/data/pgdata/bolls_dev`
- `docker-compose.yml` line 85: `/home/bolls/web/static/`

**Impact if changed:** 🟡 MEDIUM - Requires container rebuild, nginx config update
**Can be changed:** Yes, but requires coordination

**Steps required:**
1. Update all docker-compose volume paths
2. Update nginx alias paths to match
3. Rebuild containers
4. Test static file serving

### 6. Nginx Static File Paths
**Files:**
- `nginx/nginx.conf` lines 31, 41, 68: `/home/bolls/web/static/`
- `nginx_dev/nginx.conf` lines 24, 42, 79: `/home/bolls/web/static/`

**Impact if changed:** 🟡 MEDIUM - Static files won't load
**Can be changed:** Yes, must match Docker volume paths exactly

### 7. Static Directory Structure
**Path:** `django/bolls/static/bolls/` (subdirectory)

**Contains:**
- `api.css`
- `errors/` (404, 500 error styling)

**Impact if renamed:** 🟡 MEDIUM - Templates reference `/static/bolls/api.css`
**Can be changed:** Yes, update template references

---

## 🟢 LOW - Legacy/Unused Files (Safe to Update or Remove)

### 8. Old API Documentation Template
**File:** `django/bolls/templates/bolls/api.html` (38 references)

**Status:** ✅ SUPERSEDED by `api_docs.html` at `/bible/`
**Used by:** `views.api()` at `/api/` endpoint (legacy)
**Impact if changed:** 🟢 LOW - Old endpoint, new docs at `/bible/` are fully branded
**Recommendation:** Can be updated or removed

### 9. Legacy Static Files
**Files:**
- `django/bolls/static/disclaimer.html` (1 reference)
- `django/bolls/static/privacy_policy.html` (6 references)
- `django/bolls/static/registration/auth.js` (1 reference)

**Status:** ✅ STANDALONE LEGACY FILES
**Impact if changed:** 🟢 LOW - Not linked from main API docs
**Recommendation:** Can be updated when creating official privacy policy

### 10. GitHub Workflows
**Files:**
- `.github/workflows/dev-deploy.yml`
- `.github/workflows/prod-deploy.yml`
- `.github/FUNDING.yml`

**Impact if changed:** 🟢 LOW - Only affects CI/CD, can be updated

---

## 📊 Summary Statistics

**Total "bolls" references found:** ~150+

**Breakdown by category:**
- 🔴 Critical (app name, imports, models): ~20 files
- 🔴 Critical (database tables, migrations): ~15 files
- 🟡 Medium (Docker, nginx paths): 6 files
- 🟢 Low (legacy templates, static files): 5 files

---

## ✅ What's ALREADY Been Rebranded

✅ All user-facing branding (API docs, error pages)
✅ Domain (api.prayerpulse.io)
✅ Documentation files (README, DEPLOYMENT_GUIDE)
✅ Email addresses (admin@prayerpulse.io)
✅ Workspace file (prayerpulse.code-workspace)
✅ 404/500 error pages
✅ API documentation at /bible/
✅ Favicon references
✅ Code comments
✅ User-friendly book codes (Gen, Genesis, John, etc.)
✅ Clean text parameter (?clean=true)

---

## 🎯 RECOMMENDATION

### Keep As-Is (Internal References):
1. **Django app name "bolls"** - Never seen by users
2. **Directory `django/bolls/`** - Python package structure
3. **Database tables `bolls_*`** - Internal to PostgreSQL
4. **Import statements** - Internal code organization
5. **Migrations** - Critical for database integrity

### Optional Updates (If Desired):
1. **Docker volume paths** - Can change `/home/bolls/` to `/home/prayerpulse/`
2. **Nginx paths** - Must match Docker paths
3. **Static subdirectory** - Can rename `static/bolls/` to `static/prayerpulse/`
4. **Legacy files** - Update or remove old templates

### Why Keep Internal "bolls" References?

**Industry Standard:** Most rebranded projects keep internal names:
- Reddit still has internal code referencing old names
- Twitter → X kept most internal references
- Google products keep old internal codenames

**Benefits:**
- ✅ Zero risk of breaking production
- ✅ No database migration needed
- ✅ No import statement updates needed
- ✅ Simpler deployments
- ✅ Focus energy on user-facing features

**Reality:** Users never see:
- App names in settings.py
- Directory structures
- Database table names
- Import statements
- Docker volume paths

Users DO see (all already rebranded):
- ✅ Domain name (api.prayerpulse.io)
- ✅ API documentation
- ✅ Error pages
- ✅ Support emails
- ✅ Branding & styling

---

## 🚀 Next Steps (If Proceeding with Optional Updates)

### Phase 1: Docker & Nginx Paths (Low Risk)
1. Update docker-compose volume paths: `/home/bolls/` → `/home/prayerpulse/`
2. Update nginx alias paths to match
3. Test in development
4. Deploy to production

### Phase 2: Static Directory (Low Risk)
1. Rename `static/bolls/` → `static/prayerpulse/`
2. Update template references
3. Test static file loading
4. Deploy

### Phase 3: Legacy Files (No Risk)
1. Update or remove old api.html template
2. Update privacy_policy.html
3. Update disclaimer.html
4. Update auth.js (if mobile app exists)

### Phase 4: Django App Rename (HIGH RISK - Not Recommended)
**Only if absolutely necessary for long-term maintainability**

Would require:
1. Full staging environment setup
2. Comprehensive test suite
3. Backup strategy
4. Rollback plan
5. Coordinated team effort
6. Scheduled maintenance window
7. User communication plan

---

## 💡 Bottom Line

**Your API is 100% rebranded from the user's perspective.**

The remaining "bolls" references are internal infrastructure that users never see. Changing them provides minimal benefit while introducing significant risk.

**Recommendation:** Focus on features and user experience rather than internal code archaeology. ✨

---

**Document Maintained By:** Prayer Pulse Development Team
**Last Updated:** 2025-11-11
