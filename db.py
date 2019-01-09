import pymysql
conn = pymysql.connect(host='localhost', user='root', passwd="root", db='douban')
cur = conn.cursor()
cur.execute("SELECT Host,User FROM user")
for r in cur:
  print(r)