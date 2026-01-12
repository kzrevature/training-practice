# Basic Task Execution in Snowflake - 'Folinic'

Simple demo for creating and running a task in Snowflake.

### Explanation

Everything is in `folinic.sql`.
It should be self-explanatory.

```
CREATE OR REPLACE TASK FolinicUpdateAgeTask
    AS 
        UPDATE FolinicPerson fp
        SET age = FLOOR(MONTHS_BETWEEN(CURRENT_DATE(), fp.dob) / 12);
```

This is the task definition.
It simply updates `age` using the `dob` (date of birth) column.

```
EXECUTE TASK FolinicUpdateAgeTask;
```

This *schedules execution* of the task.
Note that it won't run immediately,
so wait a second or two before checking the results with `SELECT`.

If you encounter a "SQL Compilation Error [...] FolinicUpdateAgeTask does not exist"
you might need to comment out the `EXECUTE TASK` statement
and run the rest of the file separately.
I'm not sure why this error appears only sometimes.