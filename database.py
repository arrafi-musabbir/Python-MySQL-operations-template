import mysql.connector
import time
from datetime import datetime 
import socket 
import pymysql
from random import randint

class database:

    def __init__(self, host, port, user, password, schema):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = schema
        self.db_state = 0
        self.mycursor = None
        self.totalIDs = None
        self.internetConnectivity = self.checkInternetSocket()

        
    # establish connection to database
    def connectDB(self):
        try:
            self.myDB = mysql.connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database)
            self.db_state = 1
            self.mycursor = self.myDB.cursor()
            print("Server connection established successfully")
        except mysql.connector.Error:
            self.db_state = 0
            print("Server connection failed")
        return self.db_state

    
    # add new entries
    def addNew(self, tableName, MAC_Address, check_IN, check_OUT):
        try:
            self.mycursor.execute(
                "INSERT INTO {}(MAC_Address, check_IN, check_OUT) VALUES(%s, %s, %s)".format(tableName), (MAC_Address, check_IN, check_OUT))
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
                print(n,"number of entries deletation succcessfull")
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
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            print("stable internet connection")
            return True
        except socket.error:
            # print(ex)
            print("unstable internet connection restored")
            return False
    
if __name__ == "__main__":
    a = database(host ="bqgm0itmhmekra8ftfqb-mysql.services.clever-cloud.com",
                port = "3306",
                user ="ui3kv2obppaytcrg",
                password ="1G4NcaXyBPpAWuGrx5Mg",
                schema ="bqgm0itmhmekra8ftfqb" )
    a.connectDB()
    a.describeTable("CHECK_IN_OUT_records")
    a.addNew("CHECK_IN_OUT_records", randint(1, 100), randint(101, 200), randint(201, 300),)
    a.disconnect()
    ## just some commmit
