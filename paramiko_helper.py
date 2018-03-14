import paramiko as pko
import sys

nbytes = 4096
hostname = '192.168.0.1'
port = 22
username = 'root'
password = 'root'
#command = 'pgrep gpio_ctrl_daemon'
command = 'ps -ef | grep [g]pio_ctrl_daemon'

client = pko.Transport((hostname, port))
client.connect(username=username,password=password)

stdout_data = []
stderr_data = []
session = client.open_channel(kind='session')
session.exec_command(command)
while True:
    if session.recv_ready():
        stdout_data.append(session.recv(nbytes))
    if session.recv_stderr_ready():
        stderr_data.append(session.recv_stderr(nbytes))
    if session.exit_status_ready():
        break

print('exit status: ',session.recv_exit_status())
print(str(stdout_data))
print(str(stderr_data))

session.close()
client.close()

