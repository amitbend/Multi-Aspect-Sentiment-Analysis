import MySQLdb
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
def GetReviews(Pid): 
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                         user="joomla", # your username,
                          passwd="C9nG5xHQXyV95pUe", # your password
                          db="sentiment") # name of the data base
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor() 
    if Pid=='*':
        cur.execute("SELECT * FROM reviews")
    else:
        cur.execute("SELECT * FROM reviews where P_id="+ Pid)
    All_reviews=[]
    # print all the first cell of all the rows
    for row in cur.fetchall() :
        All_reviews.append(strip_tags(unicode(row[3])) +strip_tags(unicode(row[4]))+" ")
    return All_reviews


def UpdDB(Data):
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                         user="joomla", # your username,
                          passwd="C9nG5xHQXyV95pUe", # your password
                          db="sentiment")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    for row in Data:# Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO attributes(p_id, \
           attr_name, Pos, Pos_Review_ID, Neg,Neg_Review_ID) \
           VALUES ('%d', '%s', '%d', '%s', '%d','%s' )" % \
           (row[0],row[2],row[3])    
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            print "Error while submitting Querry:" + sql
    # disconnect from server
    db.close()
    
def QuerryDB(sql):
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                         user="joomla", # your username,
                          passwd="C9nG5xHQXyV95pUe", # your password
                          db="sentiment")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except:
        print "Error while submitting Querry:" + sql
    db.close()
    return cursor.fetchall()
    
def FetchReviewsByPid(Pid):
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                         user="joomla", # your username,
                          passwd="C9nG5xHQXyV95pUe", # your password
                          db="sentiment")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql="SELECT title, text from reviews where review_id="+str(Pid)
    try:
        cursor.execute(sql)
    except:
        print "Error while submitting Querry:" + sql
        db.close()
        return 
    db.close()
    return cursor.fetchall()
    
