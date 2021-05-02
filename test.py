from sshtunnel import SSHTunnelForwarder
import mysql.connector
from passwordmanager import PasswordManager

class UpdateTableEntries:

	def __init__(self, passphrase):
		self.server_connection = False
		self.serverINFO = PasswordManager(passphrase).retrieveServerCredentials()

	def establishServerConnection(self):
		try:
			self.tunnel = SSHTunnelForwarder((self.serverINFO['SSH_HOST'], int(self.serverINFO['SSH_PORT'])), 
										ssh_password=self.serverINFO['SSH_PSWD'], 
										ssh_username=self.serverINFO['SSH_UNAME'], 
										remote_bind_address=(self.serverINFO['DB_HOST'], int(self.serverINFO['DB_PORT']))) 
			self.tunnel.start()
			self.myDB = mysql.connector.connect(
				host=self.serverINFO['DB_HOST'],
				port=self.tunnel.local_bind_port,
				user=self.serverINFO['DB_UNAME'],
				password=self.serverINFO['DB_PSWD'])
			self.table_name = self.serverINFO['DB_TABLE']
			self.mycursor = self.myDB.cursor()
			self.server_connection = True
			print("Remote server connection established successfully")
			return self.db_connection
		except mysql.connector.errors.InterfaceError:
			print("Server connection failed")
			return False

	def 


conn1 = mysql.connector.connect(host=DB_HOST, user=DB_USER , passwd = SSH_PSWD, port=tunnel.local_bind_port, database=DB_NAME1)
cur1 = conn1.cursor()

conn2 = mysql.connector.connect(host=DB_HOST, user=DB_USER , passwd = SSH_PSWD, port=tunnel.local_bind_port, database=DB_NAME2)
cur2 = conn2.cursor()

cur2.execute("SELECT device_sim,device_id from {}".format(TABLE_NAME2))
d = dict()
for x in cur2:
	if len(x[1]) == 16:
		d[x[1]] = x[0]

# for i in d:
# 	cur1.execute("UPDATE {} SET Sim = {} WHERE ID = {}".format(TABLE_NAME1, '0'+d[i] , i))
# conn1.commit()

for i in d:
	cur1.execute("UPDATE init_devices SET Sim = %s WHERE ID = %s",(d[i],i))
conn1.commit()
