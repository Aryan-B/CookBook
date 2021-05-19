@ECHO OFF
cd ./download
forfiles /S /M *.* /C "cmd /c rename @file @fname.jpg"
ECHO All extensions changed...