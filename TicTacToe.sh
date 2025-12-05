#!/bin/bash
bash server_starter.sh &
SERVER_PID=$!
sleep 2
firefox http://127.0.0.1:5000/ &
wait $SERVER_PID
