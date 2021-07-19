-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS account_role_id_seq CASCADE;

CREATE SEQUENCE account_role_id_seq START 1;

DROP TABLE IF EXISTS account_role CASCADE;

CREATE TABLE account_role(
    id BIGINT DEFAULT nextval('account_role_id_seq') PRIMARY KEY,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    edited_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    name VARCHAR(20) NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS account_main_id_seq CASCADE;

CREATE SEQUENCE account_main_id_seq START 1;

DROP TABLE IF EXISTS account_main CASCADE;

CREATE TABLE account_main(
    id INTEGER PRIMARY KEY DEFAULT nextval('account_main_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    email VARCHAR(100) NOT NULL CONSTRAINT unique_account_email UNIQUE,
    name VARCHAR(100) NOT NULL,
    hash_password VARCHAR(300),
    is_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    account_role_id INTEGER REFERENCES account_role(id)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS auth_code_seq CASCADE;

CREATE SEQUENCE auth_code_seq START 1;

DROP TABLE IF EXISTS auth_code CASCADE;

CREATE TABLE auth_code(
    id BIGINT DEFAULT nextval('auth_code_seq') PRIMARY KEY,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    edited_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER UNIQUE NOT NULL REFERENCES account_main(id) ON DELETE CASCADE,
    code VARCHAR(6) NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS account_session_id_seq CASCADE;

CREATE SEQUENCE account_session_id_seq START 1;

DROP TABLE IF EXISTS account_session CASCADE;

CREATE TABLE account_session(
    id BIGINT DEFAULT nextval('account_session_id_seq') PRIMARY KEY,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    edited_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER NOT NULL REFERENCES account_main(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS organisation_id_seq CASCADE;

CREATE SEQUENCE organisation_id_seq START 1;

DROP TABLE IF EXISTS organisation CASCADE;

CREATE TABLE organisation(
    id SMALLINT PRIMARY KEY DEFAULT nextval('organisation_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER REFERENCES account_main(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    login VARCHAR(50) CONSTRAINT unique_organisation_login UNIQUE,
    photo_link VARCHAR (500),
    description VARCHAR (2000),
    CONSTRAINT unique_organisation UNIQUE(name, login)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS parents_id_seq CASCADE;

CREATE SEQUENCE parents_id_seq START 1;

DROP TABLE IF EXISTS parents CASCADE;

CREATE TABLE parents(
    id SMALLINT PRIMARY KEY DEFAULT nextval('parents_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER REFERENCES account_main(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL,
    CONSTRAINT unique_parents UNIQUE(account_main_id, name, surname)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS children_id_seq CASCADE;

CREATE SEQUENCE children_id_seq START 1;

DROP TABLE IF EXISTS children CASCADE;

CREATE TABLE children(
    id SMALLINT PRIMARY KEY DEFAULT nextval('children_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    parents_id INTEGER REFERENCES parents(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL,
    date_born DATE NOT NULL,
    CONSTRAINT unique_children UNIQUE(parents_id, name, surname)
);


-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS events_id_seq CASCADE;

CREATE SEQUENCE events_id_seq START 1;

DROP TABLE IF EXISTS events CASCADE;

CREATE TABLE events(
    id SMALLINT PRIMARY KEY DEFAULT nextval('events_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    type VARCHAR(200) NOT NULL,
    name VARCHAR(200) NOT NULL,
    date_event DATE NOT NULL,
    hours INTEGER NOT NULL,
    skill VARCHAR(200) NOT NULL,
    organisation_id INTEGER REFERENCES organisation(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS achievements_id_seq CASCADE;

CREATE SEQUENCE achievements_id_seq START 1;

DROP TABLE IF EXISTS achievements CASCADE;

CREATE TABLE achievements(
    id SMALLINT PRIMARY KEY DEFAULT nextval('achievements_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    name VARCHAR(200),
    points INTEGER NOT NULL ARRAY,
    nomination VARCHAR(150)
);

-- -------------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS teacher_id_seq CASCADE;

CREATE SEQUENCE teacher_id_seq START 1;

DROP TABLE IF EXISTS teacher CASCADE;

CREATE TABLE teacher(
    id SMALLINT PRIMARY KEY DEFAULT nextval('teacher_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    login VARCHAR(150) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL,
    specialty VARCHAR(150) NOT NULL,
    organisation_id INTEGER REFERENCES organisation(id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS children_organisation_id_seq CASCADE;

CREATE SEQUENCE children_organisation_id_seq START 1;

DROP TABLE IF EXISTS children_organisation CASCADE;

CREATE TABLE children_organisation(
    id SMALLINT PRIMARY KEY DEFAULT nextval('children_organisation_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    organisation_id INTEGER REFERENCES organisation(id) ON DELETE CASCADE,
    children_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    CONSTRAINT unique_children UNIQUE(children_id, organisation_id)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS achievements_child_id_seq CASCADE;

CREATE SEQUENCE achievements_child_id_seq START 1;

DROP TABLE IF EXISTS achievements_child CASCADE;

CREATE TABLE achievements_child(
    id SMALLINT PRIMARY KEY DEFAULT nextval('achievements_child_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    children_organisation_id INTEGER REFERENCES children_organisation(id) ON DELETE CASCADE,
    achievements_id INTEGER REFERENCES achievements(id) ON DELETE CASCADE,
    point INTEGER NOT NULL,
    CONSTRAINT unique_point_achievement UNIQUE(achievements_id, point),
    CONSTRAINT unique_achievement_for_children UNIQUE(children_organisation_id, achievements_id)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS events_child_id_seq CASCADE;

CREATE SEQUENCE events_child_id_seq START 1;

DROP TABLE IF EXISTS events_child CASCADE;

CREATE TABLE events_child(
    id SMALLINT PRIMARY KEY DEFAULT nextval('events_child_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    children_organisation_id INTEGER REFERENCES children_organisation(id) ON DELETE CASCADE,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    status BOOLEAN NOT NULL DEFAULT FALSE,
    hours_event INTEGER,
    CONSTRAINT unique_children_events UNIQUE(children_organisation_id, events_id)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS teacher_skills_id_seq CASCADE;

CREATE SEQUENCE teacher_skills_id_seq START 1;

DROP TABLE IF EXISTS teacher_skills CASCADE;

CREATE TABLE teacher_skills(
    id SMALLINT PRIMARY KEY DEFAULT nextval('teacher_skills_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    skill_name VARCHAR(150),
    teacher_id INTEGER REFERENCES teacher(id) ON DELETE CASCADE,
    CONSTRAINT unique_teacher_skill UNIQUE(skill_name, teacher_id)
);


-- -------------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS teacher_session_id_seq CASCADE;

CREATE SEQUENCE teacher_session_id_seq START 1;

DROP TABLE IF EXISTS teacher_session CASCADE;

CREATE TABLE teacher_session(
    id BIGINT DEFAULT nextval('teacher_session_id_seq') PRIMARY KEY,
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    teacher_id INTEGER REFERENCES teacher(id) ON DELETE CASCADE
);


-- -------------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS request_to_organisation_id_seq CASCADE;

CREATE SEQUENCE request_to_organisation_id_seq START 1;

DROP TABLE IF EXISTS request_to_organisation CASCADE;

CREATE TABLE request_to_organisation(
    id SMALLINT PRIMARY KEY DEFAULT nextval('request_to_organisation_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    parents_id INTEGER REFERENCES parents(id) ON DELETE CASCADE,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    children_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    status BOOLEAN DEFAULT FALSE,
    CONSTRAINT unique_request UNIQUE(parents_id, children_id, events_id)
);

-- -------------------------------------------------------------------------------
