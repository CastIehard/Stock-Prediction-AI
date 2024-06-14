1. Create XXX.timer and XXX.service file in /etc/systemd/system
	Navigate to directory and make files with "sudo touch XXX.service" same for XXX.timer

2. Edit the files with following: sudo nano XXX.timer
	XXX.timer:
'''
		[Unit]
		Description=Run Your Python Script Daily

		[Timer]
		OnCalendar=*-*-* 11:11:00
		Persistent=false

		[Install]
		WantedBy=timers.target
'''
	XXX.service:
'''
		[Unit]
		Description=Your Python Script Service

		[Service]
		Type=simple
		ExecStart=/usr/bin/python3 /home/lucapi/Desktop/Program/my_main.py

		[Install]
		WantedBy=default.target
'''
3. After updating the XXX.service file enter: 	sudo restart XXX.service

3. Enable the timer: 	sudo systemctl enable XXX.service

4. Start the timer: 	sudo systemctl start XXX.timer

5. Reload timers: 	sudo systemctl daemon-reload

6. Show all timers: 	sudo systemctl list-timers

7. To check status and to run in manually: sudo systemctl status XXX.service/timer
