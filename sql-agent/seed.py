import sqlite3

conn = sqlite3.connect("company.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS project_assignments;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    budget  INTEGER NOT NULL
);

CREATE TABLE employees (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    title         TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    salary        INTEGER NOT NULL,
    hire_date     TEXT NOT NULL
);

CREATE TABLE projects (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    start_date    TEXT NOT NULL,
    end_date      TEXT,
    status        TEXT NOT NULL CHECK(status IN ('active', 'completed', 'on_hold'))
);

CREATE TABLE project_assignments (
    employee_id INTEGER REFERENCES employees(id),
    project_id  INTEGER REFERENCES projects(id),
    role        TEXT NOT NULL,
    PRIMARY KEY (employee_id, project_id)
);
""")

cur.executemany("INSERT INTO departments VALUES (?,?,?)", [
    (1, "Engineering",  1_200_000),
    (2, "Marketing",      400_000),
    (3, "Sales",          600_000),
    (4, "HR",             250_000),
])

cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?)", [
    (1,  "Alice Nguyen",     "Senior Engineer",    1, 135_000, "2019-03-15"),
    (2,  "Bob Patel",        "Engineer",           1, 105_000, "2021-07-01"),
    (3,  "Carol Kim",        "Lead Engineer",      1, 150_000, "2017-11-20"),
    (4,  "David Osei",       "Engineer",           1,  98_000, "2022-04-10"),
    (5,  "Eva Rossi",        "Marketing Manager",  2, 115_000, "2018-06-05"),
    (6,  "Frank Li",         "Marketing Analyst",  2,  80_000, "2023-01-17"),
    (7,  "Grace Müller",     "Sales Director",     3, 140_000, "2016-09-30"),
    (8,  "Henry Brooks",     "Account Executive",  3,  90_000, "2020-02-28"),
    (9,  "Isabel Torres",    "Account Executive",  3,  88_000, "2021-11-03"),
    (10, "James Wright",     "HR Manager",         4, 110_000, "2018-04-22"),
    (11, "Karen Okafor",     "HR Specialist",      4,  75_000, "2022-08-14"),
])

cur.executemany("INSERT INTO projects VALUES (?,?,?,?,?,?)", [
    (1, "API Redesign",        1, "2025-01-10", None,         "active"),
    (2, "Data Pipeline v2",    1, "2024-09-01", "2025-03-31", "completed"),
    (3, "Brand Refresh",       2, "2025-02-01", None,         "active"),
    (4, "Q3 Campaign",         2, "2024-07-01", "2024-09-30", "completed"),
    (5, "Enterprise Outreach", 3, "2025-03-01", None,         "active"),
    (6, "Onboarding Revamp",   4, "2025-01-20", None,         "on_hold"),
])

cur.executemany("INSERT INTO project_assignments VALUES (?,?,?)", [
    (1, 1, "Backend Lead"),
    (2, 1, "Developer"),
    (3, 1, "Architect"),
    (4, 2, "Developer"),
    (3, 2, "Lead"),
    (1, 2, "Developer"),
    (5, 3, "Owner"),
    (6, 3, "Analyst"),
    (5, 4, "Owner"),
    (7, 5, "Sponsor"),
    (8, 5, "AE"),
    (9, 5, "AE"),
    (10, 6, "Owner"),
    (11, 6, "Contributor"),
])

conn.commit()
conn.close()
print("company.db created with 4 tables and sample data.")
