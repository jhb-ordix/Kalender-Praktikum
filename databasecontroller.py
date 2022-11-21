import mysql.connector
import markdown


def fileReader(counter):
    """
    reads .txt file
    @return all lines in a .txt file
    """

    lines = []

    with open('./doorContent/%s.txt' % counter, encoding='utf8') as f:
        for line in f:
            lines.append(line.strip())
        return markdown.markdown(str('\n'.join(lines)))

def connectToDB(init = False):
    host="127.0.0.1"
    user="root"
    password="8naYsFQd"
    database="adventskalender"

    if init:
        db = mysql.connector.connect(
            host= host,
            user= user,
            password= password
        )
        db.cursor().execute("CREATE DATABASE if not exists " + database)

    db = mysql.connector.connect(
        host= host,
        user= user,
        password= password,
        database= database
    )
    return db, db.cursor(buffered=True)



def addDataToDB():

        mydb, cur = connectToDB()

        for i in range(1, 25):
            statement = ("INSERT INTO  tuer (id, content) VALUES (%s, %s)")
            valu1 = (i, fileReader(i))
            cur.execute(statement, valu1)

        mydb.commit()

        # cur.execute("SHOW TABLES")

        # see = ("SELECT * FROM adventskalender.tuer;")

        # cur.execute(see)

        # print(cur.rowcount, "drinne")
        # for x in cur:
        #     print(x)
        print("hinzugefügt, war vorher nix")
        # print(cur.rowcount)

        # cur.close()

def deleteDataFromDB():

    mydb, cur = connectToDB()
    cur.execute(" DELETE FROM tuer;")
    #cur.execute("SELECT * FROM tuer ")
    #print(cur.rowcount)
    mydb.commit()



def init(dbupdate: bool):
    """
    initialises the database and creates databases/tables if not existant

    """
    _, cur = connectToDB(init = True)


    cur.execute("CREATE TABLE if not exists tuer (id INT, content TEXT(65535) )")
    cur.execute("SELECT * FROM adventskalender.tuer;")
    if cur.rowcount == 0:

        addDataToDB()

    elif dbupdate:
        
        deleteDataFromDB()
        print("DB Gelöscht")
        addDataToDB()

    else:
        cur.execute("SHOW TABLES")

        cur.execute("SELECT * FROM adventskalender.tuer;")

        print(cur.rowcount, "drinne")
        for x in cur:
            print(x)
        print("ist was drinne")

        # cur.close(


def getTask(nr):
    """
    gets task from databas
    @param nr id to looks for in table tuer
    @return fetches all in database 
    """

    mydb, cur = connectToDB()

    cur.execute("SHOW TABLES")

    aufgnr = (f"SELECT content FROM tuer WHERE id = {nr};")
    cur.execute(aufgnr)
    return cur.fetchall()[0]
