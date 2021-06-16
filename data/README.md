# Data Descriptions

Following is a table of attributes between each type of exported grade file.
Some are common and shared between all, some are present in only one file.

See the individual `.md` files for further descriptions.

| Attribute            | Big Ideas | Teams | Illuminate |     Peardeck     |
|----------------------|:---------:|:-----:|:----------:|:----------------:|
| File type            |    csv    |  csv  |     xls    |  zip (jpg & csv) |
| Multiple Assignments |     ~     |   ~   |     no     |        no        |
| Identifying info     |     ID    | email |     ID     | Name + last 4 ID |
| Numeric score        |     ~     |  yes  |     yes    |   participation  |
| Total points present |     ~     |  yes  |     yes    |    implied 100   |


## Necessary config info
### Grade source
- Source name
- Common file type(s) (non-fatal if not matching, just provide a warning)
- Header row
- Column to match (username, name+4, etc)
    - If ID already present, then "database" not needed
    - Matching pattern?
- If there may be multiple assignments
    - First column of points earned (or how to process string to get points)
    - First column of total points, or known max (or how to process string to get max)
    - Repeat pattern
    
### Database
- Expected file type (non-fatal)
- Header row
- Student name column
    - Pattern for name (first & surname)
- Username column
- ID column
- Optional: class period column
- Optional: grade level column

