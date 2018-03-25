import paramiko
import time

myconn = paramiko.SSHClient()
myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
myconn.connect('10.1.0.2', port=22, username='cloud',
                password='Sendate2017', look_for_keys=False,
                allow_agent=False)
myshell = myconn.invoke_shell()
myshell.send(' iperf3  -c  10.6.3.101 -u -b 0 -l 1500 -n 1000000000 -V -J  \n')
time.sleep(10)
output = myshell.recv(65535)
myconn.close()
print(output)
mystr = output.decode(encoding='UTF-8')
print(mystr)
