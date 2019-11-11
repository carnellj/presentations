import uuid
import psycopg2

class RfidDB:
    ##Need to put this in a secret
    def __init__(self, _user, _password, _dbname, _host):
         self.user = _user
         self.password = _password
         self.dbname = _dbname
         self.host=_host


    def getConn(self):
        return psycopg2.connect(user=self.user, password=self.password,dbname=self.dbname, host=self.host)

         
    def createContactTable(self):
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS contacts;")
        cursor.execute("CREATE TABLE contacts (contact_id VARCHAR(100) PRIMARY KEY NOT NULL, " +
                 "first_name TEXT NOT NULL, "     +
                 "last_name  TEXT NOT NULL, "     +
                 "phone      TEXT NOT NULL, "     +
                 "group_id   TEXT NOT NULL  ); ")
          
        conn.commit()
        conn.close()


    def createRfidUsersTable(self):
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS RfidUsers;")
        cursor.execute("CREATE TABLE RfidUsers (user_id VARCHAR(100) PRIMARY KEY NOT NULL, " +
                       "rfId TEXT NOT NULL, " +
                       "musicOption_id  TEXT NOT NULL); ")

        conn.commit()
        conn.close()


    def createMusicOptionsTable(self):
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS MusicOptions;")
        cursor.execute("CREATE TABLE MusicOptions (musicOption_id VARCHAR(100) PRIMARY KEY NOT NULL, " +
                       "musicTitle TEXT NOT NULL, " +
                       "fileName  TEXT NOT NULL); ")

        conn.commit()
        conn.close()


    def create(self, first_name, last_name, phone,groupId):
        contactId = str(uuid.uuid4())

        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (contact_id, first_name, last_name, phone, group_id) VALUES ((%s),(%s),(%s),(%s),(%s))",
            (contactId,first_name,last_name,phone,groupId))
        conn.commit()
        conn.close()
        return contactId


    def createRfidUser(self, rfid, musicOption_id):
        user_id = str(uuid.uuid4())

        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO RfidUsers (user_id, rfid, musicOption_id) VALUES ((%s),(%s),(%s),(%s),(%s))",
            (user_id,rfid,musicOption_id))
        conn.commit()
        conn.close()
        return user_id


    def get(self,contactId):
        conn = self.getConn()
        cursor = conn.cursor()
         
        cursor.execute("SELECT * FROM contacts WHERE contact_id = %(contactId)s",    {'contactId': contactId})
        dbresult = cursor.fetchone()
        result = {}
        result["contactId"] = contactId
        result["firstName"] = dbresult[1]
        result["lastName"]  = dbresult[2]
        result["phoneNumber"]     = dbresult[3]
        conn.close()
        return result 

    def getAllByGroupId(self,groupId):
        conn = self.getConn()
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM contacts WHERE group_id = %(groupId)s",    {'groupId': groupId})
        results = []

        for record in cursor:
          result = {}
          result["contactId"] = record[0]
          result["firstName"] = record[1]
          result["lastName"]  = record[2]
          result["phoneNumber"]     = record[3]
          result["groupId"]   = record[4]
          results.append(result)
        conn.close() 
        return results 

    def getAll(self):
        conn = self.getConn()
        cursor = conn.cursor()
        results = []
        cursor.execute("SELECT * FROM contacts")

        for record in cursor:
          result = {}
          result["contactId"] = record[0]
          result["firstName"] = record[1]
          result["lastName"]  = record[2]
          result["phoneNumber"]     = record[3]
          result["groupId"]   = record[4]
          results.append(result)
        conn.close()  
        return results


    def getAllMusicOptions(self):
        conn = self.getConn()
        cursor = conn.cursor()
        results = []
        cursor.execute("SELECT * FROM MusicOptions")

        for record in cursor:
          result = {}
          result["musicOption_id"] = record[0]
          result["musicTitle"] = record[1]
          results.append(result)
        conn.close()
        return results

    def delete(self):
        print("Delete Contact.")


class GroupDB:
    def __init__(self, _user, _password, _dbname, _host):
         self.user = _user
         self.password = _password
         self.dbname = _dbname
         self.host=_host

    def getConn(self):
        return  psycopg2.connect(user=self.user, password=self.password,dbname=self.dbname, host=self.host)
         
    def createGroupTable(self):
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS groups;")
        cursor.execute("CREATE TABLE groups (group_id VARCHAR(100) PRIMARY KEY NOT NULL, " +
                 "group_name         TEXT NOT NULL, "     +
                 "group_description  TEXT NOT NULL); ")

        conn.commit()
        conn.close()         


    def create(self, group_name, group_description):
        groupId = str(uuid.uuid4())
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO groups (group_id, group_name, group_description) VALUES ((%s),(%s),(%s))",
            (groupId,group_name,group_description))
        conn.commit()

        conn.close()
        return groupId

    def get(self,groupId):
        conn = self.getConn()
        cursor = conn.cursor()
         
        cursor.execute("SELECT * FROM groups WHERE group_id = %(groupId)s",    {'groupId': groupId})
        dbresult = cursor.fetchone()
        result = {}
        result["groupId"]   = groupId
        result["groupName"] = dbresult[1]
        result["groupDescription"]  = dbresult[2]
        result["groupId"] =dbresult[3]
        conn.close()
        return result 

    def getAll(self):
        conn = self.getConn()
        cursor = conn.cursor()
        results = []
        cursor.execute("SELECT * FROM groups")

        for record in cursor:
              result = {}
              result["groupId"] = record[0]
              result["groupName"] = record[1]
              result["groupDescription"] = record[2]
              results.append(result)
        conn.close()
        return results                   

    def delete(self):
        print("Delete Group.")