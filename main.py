from flask import Flask, render_template,Response, make_response, request
import random
from datetime import date
import mysql.connector

app = Flask(__name__)

zaehler = 1


def dateileser():
        #for dateinr in range(1,25):
        global zaehler
        with open('./tuereninhalt/%s.txt' % zaehler , encoding='utf8') as fd:
                        zaehler += 1 
                        for line in fd:
                                line.strip()
                                #print(zaehler)
                                return line
                          



def init():
        mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="8naYsFQd",
        )

        cur = mydb.cursor()

        cur.execute("CREATE DATABASE if not exists adventskalender")

        mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="8naYsFQd",
          database="adventskalender"
        )

        cur = mydb.cursor(buffered=True)

        cur.execute("SHOW DATABASES")
        cur.execute("CREATE TABLE if not exists tuer (id INT, content TEXT(65535) )")


        cur = mydb.cursor(buffered=True)

        
        rowcheck = """ SELECT * FROM adventskalender.tuer; """
        
        cur.execute(rowcheck)

        gibt_es = cur.rowcount 
        print(gibt_es)
        if gibt_es == 0:

                #cur.execute(""" truncate tuer """)
                for zahl in range(1, 25):
                        #aw= dateileser()
                        valu = ("INSERT INTO  tuer (id, content) VALUES (%s, %s)")
                        valu1 = (zahl, dateileser())
                        cur.execute(valu, valu1)

                mydb.commit()

                cur.execute("SHOW TABLES")

                see = ("SELECT * FROM adventskalender.tuer;")

                cur.execute(see)

                print(cur.rowcount, "drinne")
                for x in cur:
                 print(x)
                print("hinzugefügt, war vorher nix")
                print(cur.rowcount)

                cur.close()


                
        else:
                #cur.execute(""" truncate tuer """)
                
                cur.execute("SHOW TABLES")

                see = """ SELECT * FROM adventskalender.tuer; """

                cur.execute(see)

                print(cur.rowcount, "drinne")
                for x in cur:
                 print(x)
                print("ist was drinne")

                cur.close()


        cur = mydb.cursor(buffered=True)
        aufg_finder = cur.execute(" SELECT * FROM adventskalender.tuer WHERE id = %d; ")
        return(aufg_finder)
              


def numberinstring(nr: int, cookie: str):
     
      visited = ""
      if cookie:
          visited = cookie.split(":")

      for door in visited:
                if nr == int(door):
                 return True
     
      return False
       
def handlecookie(resp: Response, nr: int):

        cookie = request.cookies.get("Besucht")

        if cookie == None:
                resp.set_cookie("Besucht", str(nr))
                return resp

        if numberinstring(nr, cookie):
                return resp


        resp.set_cookie("Besucht",cookie + ":" + str(nr))
        return resp



@app.route("/")
def start():


        title = "ORDIX 2022 Adventskalender"
        tuerliste  = []
        heute = date.today()
        bild = random.randint(1,3)

        cookie = request.cookies.get("Besucht")

        for i in range(1, 25):

                if numberinstring(i, cookie):
                        thisdict= {
                        "nr": i,
                        "tuerclass": "tuer open",
                        "ypos": random.randint(-10,11),
                        "xpos": random.randint(-4,94),
                        "farbe": "black",
                        }
                else:
                        thisdict= {
                        "nr": i,
                        "tuerclass": "tuer closed",
                        "ypos": random.randint(-10,11),
                        "xpos": random.randint(-4,94)
                        }
                random.shuffle(tuerliste)
                tuerliste.append(thisdict)

        d1 = int(heute.strftime("%d"))
        m1 = int(heute.strftime("%m"))

        


        return render_template("start.html", title=title, tuerliste=tuerliste, heute=heute, d1=d1, m1=m1, bild=bild)


        


@app.route("/tuer/<int:nr>")
def tuer(nr):


        aufg1 = "aw1"
        aufg2 = "aw2"
        aufg3 = "aw3"
        aufg4 = "aw4"
        aufg5 = "aw5"
        aufg6 = "aw6"
        aufg7 = "aw7"
        aufg8 = "aw8"
        aufg9 = "aw9"
        aufg10 = "aw10"
        aufg11 = "aw11" 
        aufg12 = "aw12"
        aufg13 = "aw13"
        aufg14 = "aw14"
        aufg15 = "aw15"
        aufg16 = "aw16"
        aufg17 = "aw17"
        aufg18 = "aw18"
        aufg19 = "aw19"
        aufg20 = "aw20"
        aufg21 = "aw21"
        aufg22 = "aw22"
        aufg23 = "aw23"
        aufg24 = "aw24"

        
        aufgnr = """  SELECT * FROM adventskalender.tuer WHERE id = %d;""" % (nr)                  #[aufg1,aufg2,aufg3,aufg4,aufg5,aufg6,aufg7,aufg8,aufg9,aufg10,aufg11,aufg12, aufg13,aufg14,aufg15,aufg16,aufg17,aufg18,aufg19,aufg20,aufg21,aufg22,aufg23,aufg24]



        heute = date.today()
        d1 = int(heute.strftime("%d"))
        m1 = int(heute.strftime("%m"))

        if nr <= d1:
                resp = make_response(render_template("tueren.html", nr=nr, aufgnr=aufgnr))
                resp = handlecookie(resp, nr)
                return resp 

        return "Schummler"
        



if __name__ =="__main__":
        init()
        # dateileser()
        app.run(debug=True)