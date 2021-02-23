#!/bin/bash

sudo python setup.py install

cp smartbms_monitor.service /etc/systemd/system/smartbms_monitor.service
chmod +x /etc/systemd/system/smartbms_monitor.service
systemctl daemon-reload

systemctl start smartbms_monitor.service
systemctl enable smartbms_monitor.service

systemctl status smartbms_monitor.service
