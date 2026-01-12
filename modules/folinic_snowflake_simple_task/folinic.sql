USE WAREHOUSE COMPUTE_WH;

USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE DATABASE FolinicDB;
USE FolinicDB;

CREATE OR REPLACE SCHEMA FolinicSCH;
USE FolinicDB.FolinicSCH;

CREATE OR REPLACE TABLE FolinicPerson (
    first_name      VARCHAR(50),
    last_name       VARCHAR(50),
    dob             DATE,
    age             INT
);

INSERT INTO FolinicPerson (first_name, last_name, dob, age)
VALUES
    ('Bob', 'Jones', '01/01/2001', 0),
    ('Brie', 'Jess', '02/02/2002', 100),
    ('Bill', 'Joel', '03/03/2003', -2);

-- DATEDIFF(YEAR, ...) is bad, literally just subtracts the raw year
-- without considering the rest of the date
CREATE OR REPLACE TASK FolinicUpdateAgeTask
    AS 
        UPDATE FolinicPerson fp
        SET age = FLOOR(MONTHS_BETWEEN(CURRENT_DATE(), fp.dob) / 12);
        
-- May need to run this separately
EXECUTE TASK FolinicUpdateAgeTask;

-- Run this after the task finishes execution
SELECT * FROM FolinicPerson;