@echo off
cd /d "
C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections
"
"
C:\Users\suhas.bhandari\AppData\Local\Programs\Python\Python312\python.exe
" -m http.server 8000 --bind 127.0.0.1 > .server-8000.out.log 2> .server-8000.err.log
