@echo off
REM Build Exe

call activate.bat cppProjectTemplate

set isDebug=%1

where cl >nul 2>nul || (
    REM generate initvc.bat file
    python script/manage.py init x64
    if exist ./.Build/initvc.bat (
        call ./.Build/initvc.bat
        del .Build\initvc.bat
    ) else (
        goto scriptEnd
    )
)

if "%isDebug%" == "" (
    python script/manage.py build x64 --debug=0
) else (
    python script/manage.py build x64 --debug=1
)

conda deactivate

:scriptEnd