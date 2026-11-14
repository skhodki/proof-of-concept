# Natural language text-to-SQL proof of concept #

This project uses Python and PostgreSQL to create a fake LLM to convert three pre-defined natural language questions into valid SQL, and to return a natural language response.

NOTE: No LLM is used. The AI part of the process is faked with hard-coded scripts.

## Prerequisites

This project assumes that you already have Python and PostgreSQL installed on your development computer.

## Setup

```
git clone git@github.com:skhodki/proof-of-concept.git
cd proof-of-concept
```

## .env
Create a hidden `.env` file with the following entries:

DB_NAME=events_db
DB_USER=__YOUR_USERNAME__
DB_PASSWORD=__YOUR_PASSWORD__
DB_HOST=localhost
DB_PORT=5432

On Windows, __YOUR_USERNAME__ should be `postgres`, and __YOUR_PASSWORD__ should be the password you used when installing PostgreSQL

On MacOS, __YOUR_USERNAME__ should be your Mac user name. The password will be ignored, so you can remove the entry for it.

## Windows: installing dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

This installs FastAPI, the PostgreSQL driver, and the dotenv package in one step.

## MacOS: installing dependencies

```zsh
python3 -m venv .venv
source .venv/lib/activate
pip install -r requirements.txt
```

This installs FastAPI, the PostgreSQL driver, and the dotenv package in one step.

## Checking that Python can connect to PostgreSQL

1. Run:
```python
python connect_db.py
```

If all is well, the output should be:

```
(1,)
```
## Creating some dummy data in the database

2. Run
```
python add_data.py
```

If all goes well, the output should be:

```
Table 'meetings' is ready.
Inserted meetings with ids=[1, 2, 3].

All meetings:
(1, 'Python for AI', 'Maker Lab', datetime.datetime(2026, 11, 20, 19, 0))
(2, 'LLM and SQL', 'City Library', datetime.datetime(2026, 11, 21, 18, 30))
(3, 'Database design', 'Café Olé', datetime.datetime(2026, 11, 22, 17, 0))
```

## Starting the server

3. Run
```
fastapi dev main.py
```

If all goes well, the output should be something like:
```
 ⚡️ Starting FastAPI in development mode

 🐍 Using import string: main:app

 🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
 ```

4. Ctrl-click or Cmd-click on the [http://127.0.0.1:8000](http://127.0.0.1:8000) link.
5. A web page should open in your browser. Check what happens if you click on the different buttons.

If all goes well, you might see something like:

```tex
Natural language question = "find meetings on friday"
{
  "question": "find meetings on friday",
  "sql": "SELECT id, title, location, start_time FROM meetings WHERE EXTRACT(ISODOW FROM start_time) = 5",
  "rows": [
    {
      "id": 1,
      "title": "Python for AI",
      "location": "Maker Lab",
      "start_time": "2026-11-20T19:00:00"
    }
  ],
  "answer": "The meeting \"Python for AI\" will take place at Maker Lab this coming Friday at 7 p.m."
}

The meeting "Python for AI" will take place at Maker Lab this coming Friday at 7 p.m.
```

## Understanding the pipeline

1. A click on a button sends a request to the server with a natural language question, such as "find meetings on friday".
2. The `main.py` server sends a request to `fake_llm_in.py` to convert this question to SQL.
3. `main.py` uses `psycopg2` to run this SQL against the database.
4. `main.py` sends a request to `fake_llm_out.py` to convert the row data from the database into a natural language answer.
5. `main.py` returns a dict with the question, sql, rows and answer to the client.
6. The client displays the raw data that it receives, for debugging purposes, and then displays the answer.

## Security issues

NOTE that `main.py` executes an SQL query from an external source without checking whether it is safe to do so. In the context of this simple proof-of-concept demo, this does not cause any problems. In a deployed project, it could cause disaster.

A production version would not accept SQL from the client at all. It would accept parameters and build the query server-side, or validate the SQL against an allowlist before executing it.