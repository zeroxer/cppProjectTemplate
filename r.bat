@echo off
REM Run Exe

set isDebug=%1

call activate.bat cppProjectTemplate

if "%isDebug%" == "" (
    python script/manage.py run x64 --debug=0
) else (
    python script/manage.py run x64 --debug=1
)

conda deactivate
