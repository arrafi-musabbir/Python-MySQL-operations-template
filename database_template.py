import mysql.connector
import time
from datetime import datetime
import socket
from sshtunnel import SSHTunnelForwarder
import yaml

class database:

    def __init__(self, server):
        self.internetConnectivity = self.checkInternetSocket()
        self.db_connection = False
        self.mycursor = None
        self.totalIDs = None
        self.server = server
        self.connectDB()

    # establish connection to database

    def connectDB(self):
        self.retrieveCreds()
        if self.server == 'remote':
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
                    password=self.serverINFO['DB_PSWD'],
                    database=self.serverINFO['DB_NAME'])
                self.table_name = self.serverINFO['DB_TABLE']
                self.db_state = 1
                self.mycursor = self.myDB.cursor()
                print("Server connection established successfully")
            except mysql.connector.errors.InterfaceError:
                self.db_state = 0
                print("Server connection failed")
            return self.db_state
        elif self.server == 'local':
            try:
                self.myDB = mysql.connector.connect(
                        host=self.serverINFO['DB_HOST'],
                        port=self.serverINFO['DB_PORT'],
                        user=self.serverINFO['DB_UNAME'],
                        password=self.serverINFO['DB_PSWD'],
                        database=self.serverINFO['DB_NAME'])
                self.table_name = 'deviceid'
                self.db_state = 1
                self.mycursor = self.myDB.cursor()
                print("Server connection established successfully")
            except mysql.connector.errors.InterfaceError:
                self.db_state = 0
                print("Server connection failed")
            return self.db_state
        else:
            print("Invalid server")

    def retrieveCreds(self):
        self.serverINFO = dict()
        if self.server == 'local':
            with open('local_creds.yaml', 'r') as file:
                    serverINFO = yaml.safe_load(file)
                    for i in serverINFO:
                        self.serverINFO[i] = serverINFO[i]
        elif self.server == 'remote' :
            with open('remote_creds.yaml', 'r') as file:
                    serverINFO = yaml.safe_load(file)
                    for i in serverINFO:
                        self.serverINFO[i] = serverINFO[i]
                        
    # add new entries
    def addNew(self, Sim, ID, Password, CreatedOn):
        try:
            self.mycursor.execute(
                "INSERT INTO {}(Sim, ID, Password, CreatedOn) VALUES(%s, %s, %s, %s)".format(self.table_name), (Sim, ID, Password, CreatedOn))
            self.myDB.commit()
            time.sleep(1)
            print("added to database successfully")
            return True
        except mysql.connector.errors.IntegrityError:
            print("Unique value violated")
            return False

    # describe the table

    def describeTable(self, tableName):
        self.mycursor.execute("DESCRIBE {}".format(tableName))
        for x in self.mycursor:
            print(x)

    # terminate connection with database

    def disconnect(self):
        if self.db_connection:
            self.myDB.disconnect()

    # clear said table

    def clearTable(self, tableName):
        self.mycursor.execute("TRUNCATE TABLE {}".format(tableName))
        self.myDB.commit()
        print("The table has been cleared")

    # clear n number of entries from said table

    def clearEntries(self, n):
        if self.myDB:
            try:
                for i in range(n):
                    self.mycursor.execute(
                        "DELETE FROM deviceid ORDER BY CreatedOn DESC LIMIT 1")
                self.myDB.commit()
                print(n, "number of entries deletation succcessfull")
            except AttributeError:
                print("Not connected to Database")
                pass
        else:
            print("database didn't respond")

    # get total number of entries/ID
    def getTotalID(self):
        try:
            # self.mycursor.execute(
            #     "SELECT Serial FROM deviceid ORDER BY CreatedOn DESC LIMIT 1")
            self.mycursor.execute("SELECT * FROM deviceid")
            num_rows = self.mycursor.fetchall()
            return len(num_rows)
        except:
            print("database connection failed")
            return False

    # check if a stable internet connection is available
    def checkInternetSocket(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port))
            print("stable internet connection")
            return True
        except socket.error:
            print("unstable internet connection restored")
            return False


if __name__ == "__main__":
    # initiate class instance bt providing either local / remote
    a = database('local')
    # a.describeTable(tableName="deviceid")
    # a.addNew("CHECK_IN_OUT_records", randint(1, 100), randint(101, 200), randint(201, 300),)
    a.disconnect()
    # just some commmit