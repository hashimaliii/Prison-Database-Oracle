SET ECHO ON;

PROMPT Executing 01_create_tables.sql
@01_create_tables.sql

PROMPT Executing 02_constraints.sql
@02_constraints.sql

PROMPT Executing 03_sequences.sql
@03_sequences.sql

PROMPT Executing 04_indexes.sql
@04_indexes.sql

PROMPT Executing 05_insert_data.sql
@05_insert_data.sql

PROMPT Executing 07_views.sql
@07_views.sql

PROMPT Executing 08_dcl.sql
@08_dcl.sql

PROMPT Executing 09_plsql.sql
@09_plsql.sql

COMMIT;
PROMPT Setup Complete!
EXIT;
