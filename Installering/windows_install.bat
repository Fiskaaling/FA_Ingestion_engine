REM Installera Conda, git og https://www.microsoft.com/en-us/download/confirmation.aspx?id=48145 fyrst
REM System32 má vera í path
REM git má vera installera á C:\Program Files\Git\cmd\git.exe, ella broyt setup fílin

call C:\ProgramData\Anaconda3\condabin\conda create -n ingestion_engine_env -y
call C:\ProgramData\Anaconda3\Scripts\activate.bat ingestion_engine_env
call C:\ProgramData\Anaconda3\condabin\conda install numpy -y
call C:\ProgramData\Anaconda3\condabin\conda install matplotlib -y
call C:\ProgramData\Anaconda3\condabin\conda install pandas -y
call C:\ProgramData\Anaconda3\condabin\conda install scipy -y
call C:\ProgramData\Anaconda3\condabin\conda install cartopy -y
call python -m pip install geopy
call python -m pip install  pyperclip
call python -m pip install screeninfo
set "GIT_PYTHON_GIT_EXECUTABLE=C:\Program Files\Git\cmd\git.exe"
call python -m pip install gitpython
call C:\ProgramData\Anaconda3\condabin\conda install -c conda-forge utide -y
call python -m pip install mysql-connector-python
call python -m pip install pywin32

echo Liðugt at installera
pause