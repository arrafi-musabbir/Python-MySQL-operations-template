from sshtunnel import SSHTunnelForwarder
import mysql.connector
print(len("2021-04-28 12:46:19.520502"))

SSH_HOST = '103.123.8.52'
SSH_PSWD = 'Dhaka!027'
SSH_UNAME = 'papel'
SSH_PORT = 22
DB_USER = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME1 = 'arrafi_pg'
TABLE_NAME1 = 'init_devices'
DB_NAME2 = 'wasa_amr'
TABLE_NAME2 = 'amr_dashboard_device_info'


tunnel=SSHTunnelForwarder((SSH_HOST, SSH_PORT), ssh_password = SSH_PSWD, ssh_username = SSH_UNAME, remote_bind_address = (DB_HOST, DB_PORT))
tunnel.start()
conn1 = mysql.connector.connect(host=DB_HOST, user=DB_USER , passwd = SSH_PSWD, port=tunnel.local_bind_port, database=DB_NAME1)
cur1 = conn1.cursor()
conn2 = mysql.connector.connect(host=DB_HOST, user=DB_USER , passwd = SSH_PSWD, port=tunnel.local_bind_port, database=DB_NAME2)
cur2 = conn2.cursor()
cur1.execute("DESCRIBE {}".format(TABLE_NAME1))
cur2.execute("SELECT device_sim,device_id from {}".format(TABLE_NAME2))
for x in cur1:
            print(x)
d = dict()
for x in cur2:
	if len(x[1]) == 16:
		d[x[1]] = x[0]
# for i in sorted(d.keys()):
# 	print(i,'>>',d[i],'\n')

# for i in d:
# 	cur1.execute("UPDATE {} SET Sim = {} WHERE ID = {}".format(TABLE_NAME1, '0'+d[i] , i))
# conn1.commit()

for i in d:
	cur1.execute("UPDATE init_devices SET Sim = %s WHERE ID = %s",(d[i],i))
conn1.commit()
