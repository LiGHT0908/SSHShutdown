import subprocess
import re
import sys
import paramiko

def get_ips():
    commands=["nmap","10.10.22.1/24","-p","22","--open"]
    run=subprocess.Popen(commands,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out=run.communicate()
    stuff=list(out)
    fin=stuff[0].decode("utf-8")
    ips=re.findall( r'[0-9]+(?:\.[0-9]+){3}' , fin)
    print(ips)
    return ips

def ssh_kill(hosts):
    for i in range(0,len(hosts)):
        try:
            pc = paramiko.SSHClient()
            pc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pc.connect(hostname=hosts[i],port=22,username="mu",password="1")
            stdin,stdout,stderr=pc.exec_command("sudo shutdown now",get_pty=True)
            stdin.write("1\n")
            stdin.flush()
            stderr=stderr.readlines()
            stdout=stdout.readlines()
            print("Shutting Down " + hosts[i])
        except Exception as e:
            print(str(e))


ip_list=get_ips()
ssh_kill(ip_list)
