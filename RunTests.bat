setlocal
set PYTHONPATH=%cd%\robot\shared\lib;%cd%\Submodules;%PYTHONPATH%
cd robot\shared\testmanager
python TestManager.py
cd ..\..\..\
endlocal