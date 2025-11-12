# Prayer Pulse Bible API 📖

A powerful, multilingual RESTful API providing access to 150+ Bible translations in 27 languages, with commentaries, cross-references, dictionaries, and advanced search capabilities.

**🌐 Live API:** [https://api.prayerpulse.io](https://api.prayerpulse.io)
**📚 Full Documentation:** [https://api.prayerpulse.io/docs/bible/](https://api.prayerpulse.io/docs/bible/)

---

## ✨ Key Features

### 🌍 Multilingual Support
- **27 languages** including English, Spanish, Portuguese, Ukrainian, Russian, Chinese, Korean, Japanese, German, French, Hebrew, Greek, Arabic, and more
- **150+ Bible translations** organized by language
- **RTL support** for Hebrew, Arabic, and Farsi
- **Language discovery endpoint** for building internationalized apps

### 📖 User-Friendly API Design
- **Readable book names** - Use `Genesis`, `John`, or `Psalms` instead of numeric IDs
- **Clean text parameter** - Toggle Strong's numbers and footnotes on/off
- **Section titles** - Access editorial headings for Bible study apps
- **Flexible formats** - Support for both modern and legacy URL structures

### 📚 Advanced Bible Study Tools
- **Cross-references** - 3,780+ commentary entries with links to related passages
- **Parallel comparisons** - Compare multiple translations side-by-side
- **Advanced search** - Full-text search with verse-level precision
- **Hebrew/Greek dictionaries** - Strong's Concordance lookups
- **Commentaries** - Scholarly notes and translation variants

### ⚡ Developer-Friendly
- **RESTful design** - Intuitive, predictable endpoints
- **CORS enabled** - Use from any web application
- **No authentication required** - Open access to Bible content
- **JSON responses** - Easy to integrate with any framework
- **Comprehensive docs** - Interactive examples and code snippets

---

## 🚀 Quick Start

### Fetch a Verse
```bash
curl https://api.prayerpulse.io/bible/get-verse/KJV/John/3/16/
```

### Get All Available Languages
```bash
curl https://api.prayerpulse.io/bible/get-languages/
```

### Search for Text
```bash
curl https://api.prayerpulse.io/bible/search/NIV/love%20your%20neighbor/
```

### Compare Translations
```bash
curl https://api.prayerpulse.io/bible/get-parallel-verses/ \
  -H "Content-Type: application/json" \
  -d '{
    "translations": ["KJV", "NIV", "ESV"],
    "verses": [{"book": 43, "chapter": 3, "verse": 16}]
  }'
```

---

## 📊 Supported Languages & Translations

| Language | Translations | Examples |
|----------|--------------|----------|
| 🇺🇸 English | 40+ | KJV, NIV, ESV, NASB, NLT, NKJV, MSG, AMP, BSB, CSB, CEB, WEB, YLT |
| 🇪🇸 Spanish | 7+ | Reina-Valera 1960, NVI, NTV, LBLA, BTX3, PDT, RV2004 |
| 🇵🇹 Portuguese | 14+ | Almeida (ARA, ARC, ACF), NVI, NTLH, NAA, NVT, KJA, CNBB |
| 🇺🇦 Ukrainian | 12+ | UBIO, UKRK, HOM, UTT, UMT, PHIL, CUV23, TUB, GYZ |
| 🇷🇺 Russian | 7+ | Synodal, NRT, JNT, RBS2, BTI, TNHR, DESN |
| 🇨🇳 Chinese | 5+ | CUV (Traditional), CUNP, CUNPS (Simplified), PCB, PCBS |
| 🇰🇷 Korean | 2 | KRV (개역한글), RNKSV (새번역) |
| 🇯🇵 Japanese | 3 | Shinkai-yaku, Shinkyodo-yaku, Kougo-yaku |
| 🇩🇪 German | 6 | Luther, Schlachter, Elberfelder, Menge, HFA |
| 🇫🇷 French | 5 | Segond, Darby, NBS, Parole de Vie, BDS |
| 🇮🇱 Hebrew | 5 | WLC (with vowels/accents), Aleppo Codex, DHNT |
| 🇬🇷 Greek | 4 | Septuagint (LXX), Textus Receptus, Tischendorf, LXXE |
| 🇸🇦 Arabic | 1 | Smith and Van Dyke (RTL support) |
| 🇮🇷 Farsi | 2 | POV, FACB (RTL support) |

**Plus:** Dutch, Czech, Hindi, Malayalam, Nepali, Indonesian, Tamil, Polish, Romanian, Norwegian, Swahili, Swedish, Vietnamese, Afrikaans, Hungarian, Latin/Italian

---

## 🛠️ Self-Hosting Setup

### Prerequisites
- Docker & Docker Compose (or Podman with podman-compose)
- PostgreSQL database
- 2GB+ RAM recommended
- 10GB+ disk space for translations

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/calistotc/bible.api.git
   cd bible.api
   ```

2. **Configure environment**
   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your database credentials
   ```

3. **Start services**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Load Bible data**
   ```bash
   # Load a translation (e.g., King James Version)
   docker-compose exec web python3 manage.py load_translation KJV

   # Load commentaries and cross-references
   docker-compose exec web python3 manage.py load_commentaries
   ```

5. **Access your API**
   - API endpoints: `http://localhost/bible/`
   - Documentation: `http://localhost/docs/bible/`

### Detailed Setup Guides
- [Local Development with Docker](./docs/LOCAL_DEV_WITH_DOCKER_COMPOSER.md)
- [VPS Instance Setup](./docs/VPS_INSTANCE_SETUP.md)
- [How to Add a New Translation](./docs/HOW_TO_ADD_A_NEW_TRANSLATION.md)
- [How to Add Commentaries](./docs/HOW_TO_ADD_COMMENTARIES.md)
- [How to Add a Dictionary](./docs/HOW_TO_ADD_A_NEW_DICTIONARY.md)

---

## 📖 API Endpoints Overview

### Core Endpoints
- `GET /bible/get-languages/` - List all languages and translations
- `GET /bible/get-translations/` - List all available translations
- `GET /bible/get-verse/{translation}/{book}/{chapter}/{verse}/` - Get a single verse
- `GET /bible/get-chapter/{translation}/{book}/{chapter}/` - Get entire chapter with commentaries
- `GET /bible/get-text/{translation}/{book}/{chapter}/` - Get chapter text only
- `GET /bible/search/{translation}/{query}/` - Search Bible text
- `POST /bible/get-parallel-verses/` - Compare translations side-by-side

### Advanced Features
- `GET /bible/get-books/{translation}/` - Get book list with metadata
- `GET /bible/get-random-verse/{translation}/` - Get random verse
- `GET /bible/dictionary-definition/{dict}/{query}/` - Hebrew/Greek dictionary lookup
- `GET /bible/get-translation/{translation}/` - Download entire translation

### Query Parameters
- `?clean=true` - Remove Strong's numbers, footnotes, and section titles
- Context parameters available on search endpoints

**See full documentation at:** [https://api.prayerpulse.io/docs/bible/](https://api.prayerpulse.io/docs/bible/)

---

## 💡 Use Cases

### Bible Reading Apps
```javascript
// Fetch John 3:16 in multiple translations
const translations = ['KJV', 'NIV', 'ESV'];
const verse = { book: 43, chapter: 3, verse: 16 };

const response = await fetch('https://api.prayerpulse.io/bible/get-parallel-verses/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ translations, verses: [verse] })
});

const data = await response.json();
console.log(data); // Compare translations side-by-side
```

### Multilingual Bible Study Tools
```python
import requests

# Get all available languages
languages = requests.get('https://api.prayerpulse.io/bible/get-languages/').json()

# Display language selector
for lang in languages:
    print(f"{lang['language']}: {len(lang['translations'])} translations")
    for translation in lang['translations']:
        print(f"  - {translation['short_name']}: {translation['full_name']}")
```

### Cross-Reference Study
```javascript
// Fetch verse with cross-references
const response = await fetch('https://api.prayerpulse.io/bible/get-verse/RNKSV/Genesis/3/24/');
const verse = await response.json();

if (verse.comment) {
  // Parse HTML links to get related verses
  const parser = new DOMParser();
  const doc = parser.parseFromString(verse.comment, 'text/html');
  const links = doc.querySelectorAll('a');

  links.forEach(link => {
    console.log(`Related: ${link.textContent} - ${link.href}`);
  });
}
```

---

## 🏗️ Architecture

### Tech Stack
- **Backend:** Django 4.x (Python)
- **Database:** PostgreSQL 14+
- **Web Server:** Nginx
- **Containerization:** Docker / Podman
- **Reverse Proxy:** Traefik (optional)

### Project Structure
```
bible.api/
├── django/                 # Django application
│   ├── bolls/             # Main app (Bible API)
│   │   ├── data/          # Languages and metadata
│   │   ├── management/    # Django commands
│   │   ├── models.py      # Database models
│   │   ├── views.py       # API endpoints
│   │   ├── urls.py        # URL routing
│   │   └── templates/     # API documentation
│   └── bain/              # Project settings
├── commentaries/          # Commentary data (CSV)
├── sql/                   # Bible translation data
├── nginx_prod/            # Nginx configuration
├── docs/                  # Setup documentation
└── docker-compose*.yml    # Docker configurations
```

---

## 🎯 What's New in Prayer Pulse API

### Recent Improvements
- ✅ **Multilingual Support** - Added `/get-languages/` endpoint with 27 languages
- ✅ **Cross-References** - 3,780+ commentary entries with interconnected passages
- ✅ **User-Friendly URLs** - Use book names instead of numeric IDs
- ✅ **Clean Text Parameter** - Toggle annotations on/off
- ✅ **Section Titles** - Extract editorial headings for better organization
- ✅ **URL Restructure** - Documentation at `/docs/bible/`, API at `/bible/`
- ✅ **Comprehensive Docs** - Interactive API documentation with examples
- ✅ **Modern UI** - Beautiful landing page and documentation design

### Roadmap
- 🔜 Additional translations (community contributions welcome)
- 🔜 More commentaries and study resources
- 🔜 Audio Bible integration
- 🔜 Verse memorization features
- 🔜 Prayer API endpoints
- 🔜 User management API

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Add a New Translation
1. Prepare translation data in JSON format
2. Follow the guide: [How to Add a New Translation](./docs/HOW_TO_ADD_A_NEW_TRANSLATION.md)
3. Submit a pull request

### Add Commentaries
1. Prepare commentary data in CSV format
2. Follow the guide: [How to Add Commentaries](./docs/HOW_TO_ADD_COMMENTARIES.md)
3. Submit a pull request

### Report Issues
Found a bug or have a feature request? [Open an issue](https://github.com/calistotc/bible.api/issues)

---

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

This project is a fork of [bolls.life](https://github.com/batmanwgd/bible) with significant enhancements for multilingual support, improved API design, and modern documentation.

We're grateful to the original contributors and the many Bible translation projects that make their work freely available.

---

## 📞 Support

For questions, issues, or support:

- **Email:** [admin@prayerpulse.io](mailto:admin@prayerpulse.io)
- **Documentation:** [https://api.prayerpulse.io/docs/bible/](https://api.prayerpulse.io/docs/bible/)
- **Issues:** [GitHub Issues](https://github.com/calistotc/bible.api/issues)

---

**Built with ❤️ for the global Church | Prayer Pulse Bible API**
