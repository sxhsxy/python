import cx_Oracle
import uuid
con = cx_Oracle.connect('RHISC', 'RHISC', '192.168.201.63:1521/ORCL', encoding='utf8')
c = con.cursor()
c.execute('select fuwujgbh,fuwujgmc,yiyuanbh,zuzhijgdm from gy_fuwujg')
rows = c.fetchall()
rows2 = list()
for row in rows:
    row2 = list(row)
    row2.insert(0, row[1])
    row2.insert(0, uuid.uuid4().hex)
    rows2.append(row2)
#    print(row2)
c.close()
con.close()
print(rows2)

con2 = cx_Oracle.connect('xiaohu', '82626296', '192.168.201.77/pdborcl', encoding='gbk')
c2 = con2.cursor()
c2.prepare('insert into organization1 (uuid,name,FUWUJGBH,FUWUJGMC,yiyuanbh,zuzhijgdm) values (:1, :2, :3, :4, :5, :6)')
c2.executemany(None, rows2)
con2.commit()
c2.close()
con2.close()
