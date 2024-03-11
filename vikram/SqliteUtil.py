import sqlite3

class SqliteUtil:
    assitantTableCreateSchema = """
        CREATE TABLE IF NOT EXISTS assistant_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_id INTEGER ,
        org_name TEXT NOT NULL,
        assistant_id TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""

    def __init__(self) -> None:
        self.conn = None
        self.curr = None

    def connectTodb(self):
        if self.conn == None:
            self.conn =  sqlite3.connect('magic_beans.db')

    def createCurr(self):
        if self.curr == None:
            self.curr = self.conn.cursor()

    def closeConn(self):
        self.curr.close()
        self.conn.close()
        self.curr = None
        self.conn= None

    def createAssitantTable(self):
        self.connectTodb()
        self.createCurr()
        self.curr.execute(self.assitantTableCreateSchema)
        self.conn.commit()
        self.closeConn()


    def addNewAssistantToDb(self, orgId,orgName,assitant_id):
        insetQuery = """ INSERT INTO assistant_info (org_id,org_name,assistant_id) VALUES (?,?,?)"""
        self.connectTodb()
        self.createCurr()
        data = self.curr.execute(insetQuery,(orgId,orgName,assitant_id)).fetchall()
        self.conn.commit()
        self.closeConn()
        return data

    def getAssistantIdForOrg(self,orgName):
        getQuery = """ select assistant_id from assistant_info where org_name like '{0}' """.format(orgName)
        self.connectTodb()
        self.createCurr()
        data = self.curr.execute(getQuery).fetchone()
        self.conn.commit()
        self.closeConn()
        return data



        