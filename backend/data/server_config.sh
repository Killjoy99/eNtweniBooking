cat config.json | curl -X PUT -d@- localhost:9000/config
# cat config.json | sudo curl -X PUT -d@- --unix-socket /var/run/control.unit.sock http://localhost:9000/config