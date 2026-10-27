-- Class dataset schema (Class 8 redo). Entities: students, tools, availability slots.
-- students 1 : N nothing; students M : N tools and M : N availability slots → two bridge tables.
-- Created parents first, bridges last.

CREATE TABLE IF NOT EXISTS students (
    student_id            SERIAL PRIMARY KEY,           -- generated: names are not unique
    netid                 TEXT NOT NULL UNIQUE,         -- stored lowercase
    name                  TEXT NOT NULL,
    school_year           TEXT CHECK (school_year IN ('Freshman','Sophomore','Junior','Senior')),
    intro_programming     TEXT CHECK (intro_programming IN ('took_it','equivalent','neither')),
    skill_programming     SMALLINT CHECK (skill_programming BETWEEN 1 AND 5),
    skill_data_stats      SMALLINT CHECK (skill_data_stats BETWEEN 1 AND 5),
    skill_frontend_design SMALLINT CHECK (skill_frontend_design BETWEEN 1 AND 5),
    skill_business_pitch  SMALLINT CHECK (skill_business_pitch BETWEEN 1 AND 5),
    working_style         TEXT,
    interests             TEXT,
    semester_goal         TEXT,
    submitted_at          TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS tools (
    tool_id SERIAL PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS availability_slots (
    slot_id SERIAL PRIMARY KEY,
    label   TEXT NOT NULL UNIQUE                        -- e.g. 'Weekday evenings'
);

CREATE TABLE IF NOT EXISTS student_tools (
    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
    tool_id    INT REFERENCES tools(tool_id) ON DELETE CASCADE,
    PRIMARY KEY (student_id, tool_id)
);

CREATE TABLE IF NOT EXISTS student_availability (
    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
    slot_id    INT REFERENCES availability_slots(slot_id) ON DELETE CASCADE,
    PRIMARY KEY (student_id, slot_id)
);
