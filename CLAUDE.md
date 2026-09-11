# CLAUDE.md — Backend

Flask API serving the nonprofit site frontend. Read this before making changes.

## Team

| Role | Person |
|---|---|
| Scrum Master / Developer | Aarav Nadar |
| Technologist / Developer #1 | Ryden Bercovitch |

## Goal

Provide the API behind a mimic of the San Diego Rescue Mission site. This repo holds data
models, endpoints, and the database. It serves no public pages — the frontend is a separate
Jekyll repo on GitHub Pages.

## Stack

Flask + SQLAlchemy + SQLite, running in Docker behind nginx on the shared class server,
reachable at our own subdomain. `main.py` registers blueprints. `__init__.py` configures the
app, port, and CORS.

## Before building anything

1. **Pick a unique port.** Default is `8587`; every team on the shared server needs its own
   or we collide. Set `FLASK_PORT` in `.env`, then update `docker-compose.yml`
   (`"PORT:PORT"`), the nginx conf filename, and its `proxy_pass`.
2. **Add our GitHub Pages URL to `allowed_origins` in `__init__.py`.** Missing this makes
   every frontend fetch fail CORS with a console error that looks like a broken endpoint.
   This is the most common wasted debugging hour on this template.
3. Confirm a test fetch from the deployed frontend returns a response before writing
   features.

## Conventions

Follow the existing template pattern rather than inventing one. `model/post.py` plus
`api/post.py` is the clearest pair to copy.

- **`model/<thing>.py`** — SQLAlchemy class, one per table. Include `__init__`, `create`,
  `read`, `update`, `delete`, and an `init<Thing>()` seeder for test data.
- **`api/<thing>.py`** — Flask blueprint with the endpoints. Register it in `main.py`.
- **Seeding** — add the seeder to the `generate_data` custom CLI command in `main.py` so a
  fresh clone can populate a working database in one step.

## What to build

| Model | Endpoints | Serves |
|---|---|---|
| Service | list, filter by need and location | Get Help Now page |
| Volunteer signup | create, list | Volunteer form |
| Contact message | create | Contact form |
| Newsletter subscriber | create | Footer signup |

Filter logic lives in the API, not the frontend. The frontend sends a query and renders
what comes back.

## Out of scope

Do not build.

- Real payment processing — donation UI stops at a confirmation state
- Donor account portal
- Any new auth system — the template already ships one, leave it alone
- Email sending — store submissions, do not deliver them

## Rules

**Validation server-side, always.** Client-side validation is for user experience; it is
not security. Every endpoint validates its own input.

**Status codes mean things.** Invalid input returns 400 with a message naming the field.
Missing resource returns 404. A 500 means we have a bug, not that the user typed something
wrong.

**No secrets in the repo.** `.env` is gitignored. The template ships shared test passwords
in `.env` — those are placeholders, not real credentials, and they do not go in any file we
commit.

**Do not edit template files we do not own.** `api/titanic.py`, `api/student.py`,
`api/section.py`, and the rest of the starter content stay as they are. Add our files
alongside them.

**Impact math.** One meal costs $2.83. If any endpoint returns an impact figure, it derives
from that number.

## Definition of done for any card

1. Endpoint returns correct JSON when called directly
2. Invalid input returns 400 with a useful message, not a 500
3. Seeder populates working test data from a fresh database
4. CORS passes from the deployed frontend, not just from localhost
5. Verified against the deployed backend URL, not just locally
