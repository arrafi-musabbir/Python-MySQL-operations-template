from sshtunnel import SSHTunnelForwarder
import mysql.connector
from PasswordManager import PasswordManager
import sys

class UpdateTableEntries:

    def __init__(self, passphrase, key):
        
        self.server_connection = False
        self.serverINFO = PasswordManager(
            passphrase).retrieveServerCredentials()
        self.establishServerConnection()
        self.updateTables(key)

    def establishServerConnection(self):
        try:
            self.tunnel = SSHTunnelForwarder((self.serverINFO['SSH_HOST'], int(self.serverINFO['SSH_PORT'])),
                                             ssh_password=self.serverINFO['SSH_PSWD'],
                                             ssh_username=self.serverINFO['SSH_USER'],
                                             remote_bind_address=(self.serverINFO['DB_HOST'], int(self.serverINFO['DB_PORT'])))
            self.tunnel.start()
            self.myDB1 = mysql.connector.connect(
                host=self.serverINFO['DB_HOST'],
                port=self.tunnel.local_bind_port,
                user=self.serverINFO['DB_USER'],
                password=self.serverINFO['DB_PSWD'],
                database='arrafi_pg')
            self.mycursor1 = self.myDB1.cursor()

            self.myDB2 = mysql.connector.connect(
                host=self.serverINFO['DB_HOST'],
                port=self.tunnel.local_bind_port,
                user=self.serverINFO['DB_USER'],
                password=self.serverINFO['DB_PSWD'],
                database='wasa_amr')
            self.mycursor2 = self.myDB2.cursor()

            self.server_connection = True
            print("Remote server connection established successfully")
            return self.server_connection
        except mysql.connector.errors.InterfaceError:
            print("Server connection failed")
            return False

    def updateTables(self, search_key):
        self.mycursor2.execute(
            "SELECT device_sim,device_id from {}".format('amr_dashboard_device_info'))
        d = dict()
        print("searching for IDs starting with {}".format(search_key))
        for x in self.mycursor2:
            if x[1][:len(search_key)] == search_key:
                d[x[1]] = x[0]
        print('{} IDs found with {} predecessing'.format(len(d),search_key))
        for i in d:
            self.mycursor1.execute(
                "UPDATE init_devices SET Sim = %s WHERE ID = %s", (d[i], i))
        self.myDB1.commit()
        print("Sim number updated successfully")


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        a = UpdateTableEntries(sys.argv[1], sys.argv[2])
    else:
        a = UpdateTableEntries('passphrase', 'search_key')