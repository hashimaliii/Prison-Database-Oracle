@echo off
echo ==========================================
echo Prison Database Oracle Setup Runner
echo ==========================================

set /p db_user="Enter Oracle Username (e.g., system or hr): "
set /p db_pass="Enter Oracle Password: "
set /p db_conn="Enter Connection String (e.g., localhost:1521/xe or ORCL): "

echo.
echo Connecting to Oracle and running scripts...
sqlplus %db_user%/%db_pass%@%db_conn% @run_setup.sql

echo.
echo Operation complete!
pause
