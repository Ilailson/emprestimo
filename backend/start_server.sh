#!/bin/bash
cd /home/IEC/ilailsonrocha/Imagens/EmprestimofuncionalTela/emprestimo/backend
pkill -f "app.py" 2>/dev/null
sleep 1
nohup venv/bin/python app.py > server.log 2>&1 &
sleep 2
echo "Server started. Check server.log for details."
tail -5 server.log
