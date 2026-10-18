# CampusShare

CampusShare is a web application where Beihang University students lend and borrow equipment (cameras, lab tools, sports gear, books, and more). Owners list items, borrowers request them for a date range, and the system tracks approval, payment status, deposits, returns, damage, ratings, and messages.

**Course:** Software Engineering, Beihang University, Autumn 2026
**Team:** 26F

> **Status:** working prototype. See [Known limitations](#known-limitations) before using it with real people.

## Features

- Registration and login (Beihang email addresses only)
- Equipment listings: create, edit, delete
- Browse, keyword search, category and status filters
- Borrowing requests with automatic price calculation
- Owner approval or rejection, return, late fee, damage record, deposit tracking
- Ratings and reviews
- Direct messages between students and a notification list

## Tech stack

| Part | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite (`campusshare.db`, created on first run) |
| Frontend | HTML templates (`templates/`), static files (`static/`) |
| Security libraries | Werkzeug (password hashing), itsdangerous (reset tokens) |

## Quick start (macOS or Linux)

```bash
git clone https://github.com/bhsei/26F.git
cd 26F
python3 -m venv venv
source venv/bin/activate
pip install flask
python3 app.py
```

Open <http://127.0.0.1:5000> in your browser.

**Test accounts:** registration only accepts emails ending in `@buaa.edu.cn`. For testing, use made-up addresses such as `test1@buaa.edu.cn`. Use two browsers (or a private window) to act as an owner and a borrower at the same time.

**Important:** the prototype currently listens on all network addresses, so other devices on the same Wi-Fi can reach it. Stop it with `Ctrl + C` when you finish testing, and do not run it on shared networks.

## Project structure

Current layout:

```
26F/
|-- app.py            # Flask application: database setup and all routes
|-- templates/        # HTML pages
|-- static/           # CSS, images, scripts
|-- docs/             # Project documentation (see below)
`-- .gitignore
```

The course guide recommends this wider layout, which the team is adopting step by step:

```
26F/
|-- README.md
|-- src/              # Source code
|-- tests/            # Automated and manual test assets
|-- docs/
|   |-- requirements/ # SRS and requirement-related artifacts
|   |-- design/       # Architecture and detailed design documents
|   |-- testing/      # Test plan, test cases, and test report
|   `-- release/      # Release notes and final pitch materials
|-- plans/            # Project plan, iteration plans, schedules
|-- worklogs/         # Team and individual work logs
|-- weekly-reports/   # Weekly progress-report slides (W01, W02, ...)
|-- assets/           # Images, diagrams, demo media
`-- .gitignore
```

## Documentation

| Document | Location | Status |
|---|---|---|
| Software Requirements Specification | [`docs/requirements/SRS.md`](docs/requirements/SRS.md) | Draft v0.1 |
| User roles and permissions | [`docs/requirements/user-roles-and-permissions.md`](docs/requirements/user-roles-and-permissions.md) | Draft v0.1 |
| Architecture and design | `docs/design/` | Planned (Week 11) |
| Security and trust design | `docs/design/` | Planned (Week 11) |
| Test plan and report | `docs/testing/` | Planned |
| Release notes and pitch | `docs/release/` | Planned (Week 16) |

## Progress

- [x] Project kickoff
- [x] Prototype built
- [x] Prototype reviewed and tested; gaps recorded
- [x] SRS first draft
- [ ] SRS reviewed by the team
- [ ] SRS submitted (Week 7)
- [ ] Software design and architecture (Week 11)
- [ ] Implementation of agreed fixes and features
- [ ] Testing
- [ ] Release and investment pitch (Week 16)

## Known limitations

The full list is in [Appendix A of the SRS](docs/requirements/SRS.md#appendix-a-current-state-gaps). The most important ones:

- Email addresses and student IDs are not verified, so anyone can register as a student.
- The secret key is stored in the source code, and forms have no CSRF protection.
- Payments and deposits are status labels only. No money moves.
- Notifications are only created for new messages.
- Damage reporting and deposit refunds need fixing.
- There is no administrator role.

## Contributing

1. Pull the latest changes before you start: `git pull --rebase`
2. Change one document or one coherent piece of code at a time.
3. Stage only the files that belong to that change: `git add <file>`
4. Commit with the course format: `W<week> - <summary>; <description>`
   Example: `W7 - SRS v0.1; first draft with requirements and process flows`
5. Push: `git push origin main`

Never put passwords, tokens, or keys in files, commit messages, issues, or screenshots.

## Team

| Name | Responsibility |
|---|---|
| Turay Edward Joe | Backend and database development, Flask routes and business logic, rental workflow, payment and deposit logic, late fees, damage handling, testing and debugging, presentation support |
| Amanda Nancy Skaikay | Requirements and system analysis, UI and usability review, borrowing and rental workflow testing, documentation and presentation support, functionality evaluation |
| Sandra Masiwa | System design, project documentation, architecture and workflow design, functional and security requirements, user roles and process flows, security and trust design |
