import uuid
import psycopg2

class ContactDB:
    def __init__(self):
         self.conn =  psycopg2.connect(user="postgres", password="p0stgr@s",dbname="contact_db", host="contactdb")
         
    def createContactTable(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS contacts;")
        cursor.execute("CREATE TABLE contacts (contact_id VARCHAR(100) PRIMARY KEY NOT NULL, " +
                 "first_name TEXT NOT NULL, "     +
                 "last_name  TEXT NOT NULL, "     +
                 "phone      TEXT NOT NULL); ")
          
        self.conn.commit()

    def create(self, first_name, last_name, phone):
        contactId = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (contact_id, first_name, last_name, phone) VALUES ((%s),(%s),(%s),(%s))",
            (contactId,first_name,last_name,phone))
        self.conn.commit()
        return contactId

    def get(self,contactId):
        cursor = self.conn.cursor()
         
        cursor.execute("SELECT * FROM contacts WHERE contact_id = %(contactId)s",    {'contactId': contactId})
        dbresult = cursor.fetchone()
        result = {}
        result["contactId"] = contactId
        result["firstName"] = dbresult[1]
        result["lastName"]  = dbresult[2]
        result["phone"]     = dbresult[3]
        return result 

    def delete(self):
        print("Delete Conctact.")
