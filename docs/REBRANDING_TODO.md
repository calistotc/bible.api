# Prayer Pulse API - Rebranding & Cleanup Documentation

**Date Created:** 2025-11-11
**Purpose:** Track all references to the original "bolls.life" repository and document what needs to be updated to complete the Prayer Pulse rebranding.

---

## ✅ COMPLETED - Safe Changes (Already Done)

These items have been updated and pose no risk to API functionality:

### Documentation & Branding
- ✅ `django/bolls/templates/api_docs.html` - Complete redesign with Prayer Pulse branding
- ✅ Montserrat font integrated across documentation
- ✅ Black theme with green accents (#00d084)
- ✅ API documentation expanded with comprehensive endpoints

---

## 🟢 SAFE TO UPDATE NOW - Non-Breaking Changes

These can be updated immediately without affecting API functionality. They are cosmetic or user-facing only.

### 1. Favicons & Logo Files
**Impact:** LOW - Only affects browser tab icons and app icons
**Location:** `django/bolls/static/`

```
- favicon.ico
- favicon-16x16.png
- favicon-32x32.png
- apple-touch-icon.png
- android-chrome-192x192.png
- android-chrome-512x512.png
- bolls.png (main logo file - replace with Prayer Pulse logo)
- logoshield.png
```

**Action Required:**
1. Design/obtain Prayer Pulse favicons and logos
2. Replace all files above with new branding
3. Keep same filenames to avoid breaking links

---

### 2. Error Page Templates
**Impact:** LOW - Only affects error pages users rarely see
**Files:**
- `django/bolls/templates/404.html`
- `django/bolls/templates/500.html`

**Current Issues:**
- 404.html references `/static/bolls/errors/app.css` and `/static/bolls/errors/app.js`
- 500.html has old email: `bpavlisinec@gmail.com` (should be `admin@prayerpulse.io`)

**Action Required:**
1. Update support email in 500.html
2. Update branding/styling in both templates
3. Verify CSS/JS paths still work

---

### 3. PWA Manifest File
**Impact:** LOW - Only affects Progressive Web App metadata
**File:** `imba/public/site.webmanifest`

**Current Content:**
```json
{
    "name": "Bolls Bible",
    "short_name": "Bolls",
    ...
}
```

**Action Required:**
1. Change `"name"` to `"Prayer Pulse Bible API"`
2. Change `"short_name"` to `"Prayer Pulse"`

---

### 4. Workspace Configuration
**Impact:** NONE - Developer tool only
**File:** `bolls.code-workspace`

**Action Required:**
1. Rename file to `prayerpulse.code-workspace`
2. Update any internal references

---

### 5. Static Asset Directory Structure
**Impact:** LOW - May require nginx config update
**Directories:**
- `django/bolls/static/bolls/` (contains api.css and errors/)

**Action Required:**
1. Can rename `static/bolls/` to `static/prayerpulse/`
2. Update template references from `/static/bolls/` to `/static/prayerpulse/`
3. Update nginx config paths if changed

---

### 6. Documentation Files
**Impact:** NONE - Reference materials only
**Files:**
```
- README.md
- DEPLOYMENT_GUIDE.md
- CHANGES_SUMMARY.md
- docs/HOW_TO_ADD_A_NEW_TRANSLATION.md
- docs/HOW_TO_ADD_A_NEW_DICTIONARY.md
- docs/LOCAL_DEV_WITH_DOCKER_COMPOSER.md
```

**Action Required:**
1. Replace all references to "bolls.life" with "api.prayerpulse.io"
2. Update repository owner information
3. Update email addresses to Prayer Pulse contacts

---

### 7. Comments in Code
**Impact:** NONE - Comments only
**File:** `django/bain/settings.py` line 30

```python
# Something like: localhost 127.0.0.1 [::1] dev.bolls.life
```

**Action Required:**
1. Update to reference `dev.prayerpulse.io` or similar

---

### 8. Docker Compose Email References
**Impact:** LOW - Only affects Let's Encrypt notifications
**File:** `docker-compose.yml` line 133, `docker-compose.prod.yml` line 115

```yaml
- "--certificatesresolvers.myresolver.acme.email=bpavlisinec@gmail.com"
```

**Action Required:**
1. Change to `admin@prayerpulse.io` or appropriate Prayer Pulse email

---

### 9. Imba Frontend (Scheduled for Removal)
**Impact:** NONE for production (not used in production docker-compose.api.yml)
**Directory:** `/imba/` (entire directory)

**Found References:**
- Contains full Bolls.life branding throughout
- Multiple references in `imba/public/site.webmanifest`, `imba/index.html`, etc.
- Referenced in development docker-compose files

**Action Required:**
1. ✅ **REMOVE ENTIRE DIRECTORY** - Not needed, React frontend used instead
2. Clean up docker-compose.yml and docker-compose.prod.yml
3. Update nginx configs to remove Imba proxy references

---

## 🔴 CRITICAL - Breaking Changes (Requires Careful Planning)

**⚠️ DO NOT CHANGE THESE WITHOUT THOROUGH TESTING AND PLANNING ⚠️**

These changes affect core Django functionality and database structure. Changing them requires coordinated updates across multiple files and may require database migrations.

---

### 1. Django App Name: "bolls"
**Impact:** 🔴 CRITICAL - Affects entire application
**Risk Level:** HIGH - Breaking changes

**Files Affected:**
```
django/bain/settings.py:41
    INSTALLED_APPS = ["bolls", ...]

django/bain/urls.py:8
    path('', include('bolls.urls'))

django/bolls/apps.py
    class BollsConfig(AppConfig):
        name = 'bolls'
```

**Why Critical:**
- Django uses the app name for:
  - Database table prefixes (`bolls_verses`, `bolls_bookmarks`, etc.)
  - Migration tracking in `django_migrations` table
  - Template namespace lookups
  - Static file collection
  - Import statements throughout codebase

**Renaming Would Require:**
1. Rename `django/bolls/` directory to `django/prayerpulse/`
2. Update all import statements: `from bolls.models import ...` → `from prayerpulse.models import ...`
3. Update `INSTALLED_APPS` in settings.py
4. Update `urls.py` include statements
5. Update app config in `apps.py`
6. Update all template namespaces
7. Run `makemigrations` and `migrate` to update migration tracking
8. **Database tables will KEEP old names** unless you create custom SQL migrations
9. Test extensively before deploying

**Recommendation:**
- **Keep internal "bolls" app name** - Users never see this
- Focus on user-facing branding (templates, static files, documentation)
- Only rename if absolutely necessary for long-term maintainability
- If renaming, do it in a dedicated sprint with full testing

---

### 2. Database Table Names & Indexes
**Impact:** 🔴 CRITICAL - Affects database structure
**Risk Level:** EXTREME - Could break live API

**Current Database Objects:**
```
Tables (auto-generated by Django):
- bolls_verses
- bolls_bookmarks
- bolls_history
- bolls_commentary
- bolls_dictionary
- bolls_translation
- bolls_book
... (and more)

Indexes (from migrations):
- bolls_verse_transla_b7c462_idx
- bolls_comme_transla_851084_idx
```

**Files Containing Table References:**
```
django/bolls/migrations/0012_verses_bolls_verse_transla_b7c462_idx_and_more.py
django/bolls/migrations/0013_commentary_bolls_comme_transla_851084_idx_and_more.py
```

**Why Critical:**
- These are actual database objects in production
- Renaming requires downtime and complex migrations
- Risk of data loss if done incorrectly
- All queries reference these table names

**Recommendation:**
- **DO NOT RENAME** - Table names are internal, never visible to API users
- Changing would require:
  1. Creating Django migrations to rename tables
  2. Updating all raw SQL queries (if any)
  3. Testing with full database backup
  4. Coordinating with database administrators
  5. Planning for rollback strategy

---

### 3. Django Project Structure
**Impact:** 🔴 CRITICAL - Affects imports and references
**Risk Level:** HIGH

**Directory:** `django/bolls/`

**Contains:**
```
django/bolls/
├── __init__.py
├── admin.py
├── apps.py
├── books_map.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── views.py
├── migrations/
├── management/
├── static/
└── templates/
```

**Import Examples Throughout Codebase:**
```python
from bolls.models import Verses, Bookmarks, History
from bolls.views import get_text, search_verses
from bolls.books_map import BOOKS
import bolls.forms
```

**Renaming Would Require:**
- Update every single import statement
- Update Django app configuration
- Update template loading paths
- Update static file paths
- Careful testing of every endpoint

**Recommendation:**
- **Keep directory name as "bolls"** for internal consistency
- The directory name is never exposed to end users
- Focus energy on user-facing rebranding instead

---

### 4. Volume Paths in Docker
**Impact:** 🟡 MEDIUM - Affects deployments
**Risk Level:** MEDIUM

**Files:**
```
docker-compose.yml:110
    - ./django/bolls/static/:/home/bolls/web/static/:delegated

docker-compose.prod.yml:26, 92
    - STATIC_VOLUME_NAME:/home/bolls/web/static
    - IMBA_VOLUME_NAME:/imba
```

**Why Important:**
- Changing paths requires rebuilding containers
- Must update nginx alias paths to match
- Could cause static files to not load if mismatched

**Action Required (If Changing):**
1. Update all volume mount paths
2. Update corresponding nginx `alias` directives
3. Update Dockerfile WORKDIR paths
4. Rebuild and test all containers
5. Update production deployment scripts

---

### 5. Nginx Static File Paths
**Impact:** 🟡 MEDIUM - Affects static file serving
**Risk Level:** MEDIUM

**Files:**
```
nginx/nginx.conf:41
    alias /home/bolls/web/static/;

nginx_dev/nginx.conf
    Similar references
```

**Why Important:**
- Static files (CSS, JS, images, translations) won't load if paths are wrong
- Must match Docker volume mounts exactly
- Production nginx config already uses `/var/www/api/bible/static/` (no "bolls" reference)

**Recommendation:**
- Production is already correct (no "bolls" in path)
- Development configs can be updated for consistency
- Ensure Docker volume mounts match nginx aliases

---

### 6. Environment Variables & Configuration
**Impact:** 🟡 MEDIUM - Affects configuration
**Files:**
```
docker-compose.yml:40
    - DJANGO_ALLOWED_HOSTS=bolls.local 127.0.0.1 localhost

docker-compose.yml:11
    - PGDATA=/var/lib/postgresql/data/pgdata/bolls_dev
```

**Action Required:**
1. Update `DJANGO_ALLOWED_HOSTS` to use `prayerpulse.local` or similar
2. Update `PGDATA` path (cosmetic, doesn't affect functionality)
3. Update any `.env` file examples

---

## 🔄 FUTURE ENHANCEMENT - User-Friendly API Endpoints

**Priority:** MEDIUM - Quality of Life Improvement
**Impact:** Would require maintaining backward compatibility

### Current Endpoint Structure

The current API uses numeric book IDs which can be confusing:

```
Current Format:
/get-text/YLT/1/1/1/          → Genesis 1:1
/get-chapter/KJV/1/1/         → Genesis chapter 1
/get-verses/NIV/1/1/1-5/      → Genesis 1:1-5
```

**Problems with Current Approach:**
- Users need to memorize or look up book numbers (Genesis = 1, Exodus = 2, etc.)
- Not intuitive or self-documenting
- Harder for beginners to use without consulting documentation
- Doesn't follow REST best practices for readable URLs

---

### Proposed User-Friendly Structure

**Option 1: Short Book Codes (Recommended)**
```
New Format:
/get-text/YLT/Gen/1/1/        → Genesis 1:1
/get-chapter/KJV/Exo/1/       → Exodus chapter 1
/get-verses/NIV/Gen/1/1-5/    → Genesis 1:1-5
/get-verses/ESV/Matt/5/3-10/  → Matthew 5:3-10
/search/KJV/Psa/             → Search in Psalms
```

**Benefits:**
- ✅ Immediately readable (Gen = Genesis, Exo = Exodus, Matt = Matthew)
- ✅ Self-documenting endpoints
- ✅ Easier to remember and type
- ✅ Follows industry standards (Bible Gateway, YouVersion use similar formats)
- ✅ Beginner-friendly

**Standard Bible Book Abbreviations:**

Old Testament:
```
Gen, Exo, Lev, Num, Deu, Jos, Jdg, Rut, 1Sa, 2Sa, 1Ki, 2Ki, 1Ch, 2Ch,
Ezr, Neh, Est, Job, Psa, Pro, Ecc, Sng, Isa, Jer, Lam, Ezk, Dan,
Hos, Joe, Amo, Oba, Jon, Mic, Nah, Hab, Zep, Hag, Zec, Mal
```

New Testament:
```
Matt, Mark, Luke, John, Acts, Rom, 1Co, 2Co, Gal, Eph, Phi, Col,
1Th, 2Th, 1Ti, 2Ti, Tit, Phm, Heb, Jas, 1Pe, 2Pe, 1Jn, 2Jn, 3Jn,
Jude, Rev
```

---

**Option 2: Full Book Names**
```
Alternative Format:
/get-text/YLT/Genesis/1/1/
/get-chapter/KJV/Exodus/1/
/get-verses/NIV/Matthew/5/3-10/
```

**Benefits:**
- ✅ Most intuitive for beginners
- ✅ No abbreviation memorization needed

**Drawbacks:**
- ❌ Longer URLs
- ❌ Requires URL encoding for books with spaces (e.g., "1 Samuel" → "1%20Samuel" or "1-Samuel")
- ❌ Inconsistent naming across translations (some use "Song of Solomon" vs "Song of Songs")

---

**Option 3: Hybrid Approach (Most Flexible)**
```
Support Both Formats:
/get-text/YLT/Gen/1/1/        ✅ Works (short code)
/get-text/YLT/Genesis/1/1/    ✅ Works (full name)
/get-text/YLT/1/1/1/          ✅ Works (legacy numeric)
```

**Benefits:**
- ✅ Backward compatible (existing integrations don't break)
- ✅ User-friendly for new users
- ✅ Flexible for different use cases

**Implementation Notes:**
- Create book name/abbreviation mapping in Django
- Update URL patterns to accept book codes: `<str:book>` instead of `<int:book>`
- Keep numeric endpoints active for backward compatibility
- Update documentation with examples of both formats
- Add endpoint to list all book codes: `/books/codes/` or `/book-abbreviations/`

---

### Implementation Plan

**Phase 1: Research & Design**
1. ✅ Review industry standards (Bible Gateway, YouVersion, ESV API)
2. ✅ Decide on abbreviation format (recommendation: Option 3 - Hybrid)
3. ☐ Create comprehensive book code mapping
4. ☐ Design URL structure

**Phase 2: Backend Development**
1. ☐ Create book code mapping in `django/bolls/books_map.py`
2. ☐ Update URL patterns in `django/bolls/urls.py` to accept strings
3. ☐ Update views to handle both numeric IDs and book codes
4. ☐ Add book code validation
5. ☐ Create `/book-codes/` endpoint to list all abbreviations

**Phase 3: Testing**
1. ☐ Test all endpoints with numeric IDs (verify backward compatibility)
2. ☐ Test all endpoints with short codes (Gen, Exo, Matt, etc.)
3. ☐ Test edge cases (case sensitivity, invalid codes)
4. ☐ Performance testing (ensure lookups are fast)

**Phase 4: Documentation**
1. ☐ Update API documentation with new endpoint formats
2. ☐ Add book code reference table
3. ☐ Add migration guide for existing users
4. ☐ Highlight backward compatibility

**Phase 5: Deployment**
1. ☐ Deploy to staging environment
2. ☐ Test with real clients
3. ☐ Gather feedback
4. ☐ Deploy to production

---

### Example Book Code Mapping

```python
# django/bolls/books_map.py (add to existing file)

BOOK_CODES = {
    # Numeric ID: (Full Name, Short Code, Alt Codes)
    1: ("Genesis", "Gen", ["Ge", "Gn"]),
    2: ("Exodus", "Exo", ["Ex", "Exod"]),
    3: ("Leviticus", "Lev", ["Le", "Lv"]),
    # ... continue for all 66 books
    40: ("Matthew", "Matt", ["Mt", "Mat"]),
    41: ("Mark", "Mark", ["Mk", "Mrk"]),
    42: ("Luke", "Luke", ["Lk", "Luk"]),
    43: ("John", "John", ["Jn", "Jhn"]),
    # ... etc.
}

# Reverse lookup: book code → numeric ID
CODE_TO_ID = {}
for book_id, (full_name, short_code, alt_codes) in BOOK_CODES.items():
    # Add full name (case-insensitive)
    CODE_TO_ID[full_name.lower()] = book_id
    # Add short code (case-insensitive)
    CODE_TO_ID[short_code.lower()] = book_id
    # Add alternative codes
    for alt in alt_codes:
        CODE_TO_ID[alt.lower()] = book_id

def get_book_id(book_identifier):
    """
    Convert book identifier to numeric ID.
    Accepts: numeric ID (int/str), full name, or abbreviation
    Returns: numeric ID (int) or None if invalid
    """
    # If it's already a number, return it
    if isinstance(book_identifier, int):
        return book_identifier if 1 <= book_identifier <= 66 else None

    # Try to convert string to int
    try:
        book_id = int(book_identifier)
        return book_id if 1 <= book_id <= 66 else None
    except ValueError:
        pass

    # Look up by name/code (case-insensitive)
    return CODE_TO_ID.get(book_identifier.lower())
```

---

### API Examples with New Format

**Get Single Verse:**
```bash
# New user-friendly format
curl https://api.prayerpulse.io/get-text/KJV/Gen/1/1/
curl https://api.prayerpulse.io/get-text/KJV/John/3/16/

# Legacy numeric format (still works)
curl https://api.prayerpulse.io/get-text/KJV/1/1/1/
```

**Get Chapter:**
```bash
# New format
curl https://api.prayerpulse.io/get-chapter/ESV/Matt/5/

# Legacy format
curl https://api.prayerpulse.io/get-chapter/ESV/40/5/
```

**Get Multiple Verses:**
```bash
# New format
curl https://api.prayerpulse.io/get-verses/NIV/Psa/23/1-6/

# Legacy format
curl https://api.prayerpulse.io/get-verses/NIV/19/23/1-6/
```

**Search within Book:**
```bash
# New format
curl https://api.prayerpulse.io/v2/find/KJV?search=faith&book=Rom

# Could also support: /v2/find/KJV/Rom?search=faith
```

---

### Documentation Additions Needed

**New Endpoint: List Book Codes**
```
GET /book-codes/
GET /books/abbreviations/

Response:
{
  "books": [
    {
      "id": 1,
      "name": "Genesis",
      "short_code": "Gen",
      "alt_codes": ["Ge", "Gn"],
      "testament": "OT",
      "chapters": 50
    },
    {
      "id": 40,
      "name": "Matthew",
      "short_code": "Matt",
      "alt_codes": ["Mt", "Mat"],
      "testament": "NT",
      "chapters": 28
    }
    // ... all 66 books
  ]
}
```

---

### Recommendations

**✅ Recommended Approach: Option 3 (Hybrid)**
- Implement support for book codes AND keep numeric IDs working
- This ensures backward compatibility while improving user experience
- Industry standard (most Bible APIs offer this flexibility)
- Lowest risk of breaking existing integrations

**Priority Level: MEDIUM**
- Not urgent, but significantly improves developer experience
- Can be implemented after critical rebranding work is done
- Should be done before major marketing push to new developers

**Estimated Effort:**
- Backend: 2-3 days (mapping creation, view updates, testing)
- Documentation: 1 day (updating all examples, adding reference tables)
- Testing: 1-2 days (comprehensive endpoint testing)
- **Total: ~5-6 days of development work**

---

## 📋 Recommended Action Plan

### Phase 1: Immediate Safe Changes (This PR)
1. ✅ Remove entire `/imba/` directory
2. ✅ Update favicons with Prayer Pulse branding
3. ✅ Update 404.html and 500.html templates
4. ✅ Update site.webmanifest (if keeping it)
5. ✅ Update email addresses in configs (bpavlisinec → admin@prayerpulse.io)
6. ✅ Update documentation files (README, etc.)
7. ✅ Update docker-compose email references
8. ✅ Rename workspace file
9. ✅ Update code comments

### Phase 2: Medium Priority (Future PR)
1. Consider renaming `static/bolls/` to `static/prayerpulse/`
2. Update template references to new static paths
3. Update development nginx configs
4. Test thoroughly in development environment

### Phase 3: Low Priority (Future Consideration)
1. Review whether Django app rename is worth the effort
2. If proceeding with app rename:
   - Create detailed migration plan
   - Set up staging environment
   - Create comprehensive test suite
   - Plan rollback strategy
   - Schedule maintenance window
   - Execute with full team coordination

---

## 🔍 Quick Reference: Bolls References by File Type

### Templates (Safe to update branding)
- `django/bolls/templates/404.html`
- `django/bolls/templates/500.html`
- `django/bolls/templates/admin/base_site.html`
- `django/bolls/templates/bolls/api.html`
- `django/bolls/templates/registration/*.html`

### Static Assets (Safe to replace)
- `django/bolls/static/bolls.png`
- `django/bolls/static/favicon*`
- `django/bolls/static/android-chrome-*.png`
- `django/bolls/static/apple-touch-icon.png`

### Configuration Files (Review carefully before changes)
- `django/bain/settings.py`
- `django/bain/urls.py`
- `django/bolls/apps.py`
- `docker-compose.yml`
- `docker-compose.prod.yml`
- `nginx/nginx.conf`

### Python Code (Critical - affects imports)
- `django/bolls/*.py` (all Python files)
- `django/bolls/management/commands/*.py`
- Any file with `from bolls import ...`

### Database (Do not modify)
- Migration files in `django/bolls/migrations/`
- Database tables with `bolls_` prefix
- Database indexes with `bolls_` in name

---

## 📝 Notes for Future Maintainers

1. **Production is already rebranded externally** - api.prayerpulse.io domain, Prayer Pulse branding in docs
2. **Internal "bolls" references are okay** - Users never see directory names or app names
3. **Database table names cannot be easily changed** - Leave them as-is unless there's a compelling reason
4. **Focus on user-facing elements** - Templates, static assets, documentation, error pages
5. **Test before deploying** - Always verify API endpoints work after any changes

---

## ✅ Sign-off Checklist (Before Deploying Changes)

When making changes, verify:

- [ ] API endpoints still respond correctly
- [ ] Static files load properly (CSS, JS, images)
- [ ] Error pages display with correct branding
- [ ] Documentation is accessible
- [ ] Favicon displays correctly in browser
- [ ] No broken links in templates
- [ ] Docker containers build successfully
- [ ] Database migrations apply cleanly (if any)
- [ ] No import errors in Python code
- [ ] Nginx serves files from correct paths

---

**Last Updated:** 2025-11-11
**Maintained By:** Prayer Pulse Development Team
