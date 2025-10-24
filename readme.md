# Rostering App — CLI (Flask MVC)

A command-line rostering system built from the **uwidcit/flaskmvc** template for staff scheduling and attendance management.

## Features
- **Admin**: Create/assign/publish shifts, approve/reject requests, generate weekly reports  
- **Staff**: View roster, clock in/out  
- **Auth**: Hashed passwords (Werkzeug) + JWT login (Flask-JWT-Extended)  
- **MVC architecture**: Models in `App/models`, controllers in `App/controllers`, CLI in `wsgi.py`

## Prerequisites 
- **Python 3.9+** (tested with Python 3.12+)
- **Virtual environment** (required for flask commands)
- **Dependencies** from requirements.txt (includes Flask, SQLAlchemy, etc.)
---

## Quick Start
### 1. Create Virtual Environment (needed to run the code)
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux  
python3 -m venv .venv
source .venv/bin/activate

# Verify activation - you should see (.venv) in your prompt
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
# Empty database
flask init
# With demo users (recommended for testing)
flask initialize
```


**Demo Users Created:**
- Admin: `admin1` / `adminpass`
- Staff: `staff1` / `staffpass`, `staff2` / `staffpass`

---
## Database Management
| Command | Purpose | Result |
|---------|---------|---------|
| `flask initialize` | Reset with demo users | Fresh database + 3 demo users |
| `flask init` | Create empty database | Fresh empty database |
| `del temp-database.db && flask init` | Complete reset | Deletes file + creates empty database |
> **Note**: Demo users are `admin1/adminpass`, `staff1/staffpass`, `staff2/staffpass`
---

## CLI Commands Reference
> **Note**: All commands require an active virtual environment. Look for `(.venv)` in your prompt.
### User Management
```bash
# View all users in database
flask user list

# Create new users (use unique usernames/emails)
flask user create ADMIN "Alice Smith" alice.smith@email.com alice_smith adminpass123
flask user create STAFF "Sam Wilson" sam.wilson@email.com sam_wilson staffpass123
flask auth login staff1 staffpass
```

### Shift Management
```bash
flask shift create 1 2025-09-29T09:00 2025-09-29T17:00 "FrontDesk" 2025-09-29
flask shift assign 1 2
flask shift all
flask shift publish 2025-09-29
```

### Attendance Tracking
```bash
flask att in 1 2 2025-09-29T09:04
flask att out 1 2 2025-09-29T17:02
```

### Request Management
```bash
flask req make 2 1 SWAP "Need to switch" --shift 2
flask req decide 1 APPROVED
```

### Reporting
```bash
flask report gen 2025-09-29
```

---

## Complete Demo Workflow
```bash
# 1. Setup with demo data
flask initialize

# 2. Create and assign shifts
flask shift create 1 2025-09-29T09:00 2025-09-29T17:00 "FrontDesk" 2025-09-29
flask shift assign 1 2

# 3. Record attendance
flask att in 1 2 2025-09-29T09:04
flask att out 1 2 2025-09-29T17:02

# 4. Generate weekly report
flask report gen 2025-09-29
```

---
## Testing
```bash
pytest                    # Run all tests
coverage run -m pytest   # Run with coverage
coverage report          # View coverage report
```

### Run unit vs. integration separately
tag tests using pytest markers configured in `pytest.ini`:

```ini
[pytest]
testpaths = App/tests
markers =
	unit: unit tests that validate small, isolated logic
	integration: integration tests that exercise DB, controllers, or API flows
```

Run only unit tests:
```bash
pytest -q -m unit
```

Run only integration tests:
```bash
pytest -q -m integration
```
```

---
## Troubleshooting

### Common Issues
| Issue | Solution |
|-------|-----------|
| `TypeError: unsupported operand type(s) for \|` | Python 3.9 compatible - already fixed with Union types |
| `'flask' is not recognized` | Activate virtual environment first: `source .venv/bin/activate` |
| `ModuleNotFoundError` | Virtual environment not activated or corrupted - recreate it |
| `UNIQUE constraint failed` | Username/email already exists - use different values |
| Database errors | Try: `flask initialize` (reset) or `rm temp-database.db && flask init` |
| Import errors | Ensure virtual environment is activated and dependencies installed |
| `pkg_resources` warnings | Safe to ignore - Flask-Admin uses deprecated package (functionality works fine) |

### Virtual Environment Management
```bash
# Create virtual environment
python3 -m venv .venv  # Linux/macOS
python -m venv .venv   # Windows

# Activate virtual environment
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\Activate.ps1     # Windows PowerShell
.venv\Scripts\activate.bat     # Windows CMD

# Deactivate virtual environment
deactivate

# Check if active - look for (.venv) in your prompt
```

### If Virtual Environment is Corrupted
```bash
# Linux/macOS
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Recent Improvements ✨
- **Python 3.9 Compatibility**: Fixed type annotations to use `Union[Type, None]` instead of `Type | None` for Python 3.9 compatibility
- **Enhanced Error Handling**: Improved error messages for common setup issues
- **Streamlined Setup**: Simplified virtual environment creation and dependency installation process

---

## Technical Details

### Key Features
- **Python 3.9+ Compatible**: Uses proper type annotations compatible with Python 3.9
- **MVC Architecture**: Clean separation of models, views, and controllers
- **CLI Interface**: Complete command-line interface for all operations
- **SQLAlchemy ORM**: Database operations with SQLAlchemy
- **JWT Authentication**: Secure authentication with Flask-JWT-Extended
- **Demo Data**: Pre-configured demo users for testing

### Configuration (`App/default_config.py`)
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

### Project Structure
```
App/
├── models/          # User, Admin, Staff, Shift, Attendance, Request, Report
├── controllers/     # Business logic functions  
├── views/           # Web routes (if needed)
├── __init__.py      # App factory + DB + JWT setup
├── database.py      # SQLAlchemy instance
└── default_config.py # Development configuration
wsgi.py              # CLI commands (Click) + app entry point
requirements.txt     # Dependencies
```

### Database Models
- **User** (base) → **Admin** and **Staff** (inheritance)
- **Shift** → Scheduling with status tracking
- **Attendance** → Clock in/out records  
- **Request** → Swap/time-off with approval workflow
- **Report** → Weekly summary statistics

---

**License:** Academic use for assignment 1.
