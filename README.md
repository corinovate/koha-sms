# koha-sms
Script to send SMS in Koha to patrons; whose books are going to get due.
## Requirements
Python3.x <br>
requests <br>
pymysql <br>

## Installation
```
pip install requests
pip install pymysql
```
## Code
Use your Database details on the user, password & db field.
```
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             db='kohadatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
 ```
 This is the SQL query to take details of patrons whose books are going to be due in 1 day.
 
 ```
  sql = '''SELECT p.cardnumber, p.surname, p.branchcode, p.firstname, p.mobile, p.phone,
 co.date_due, i.barcode, b.title, b.author
FROM borrowers p 
LEFT JOIN issues co ON (co.borrowernumber=p.borrowernumber) 
LEFT JOIN items i ON(co.itemnumber=i.itemnumber)
LEFT JOIN biblio b ON (b.biblionumber=i.biblionumber)
WHERE DATE(co.date_due) = DATE_ADD(curdate(), INTERVAL 1 DAY)
 AND i.homebranch = "VCL" 
 '''
 ```
 You can change the due day from 1 to 3 by changing `INTERVAL 1 DAY` to `INTERVAL 3 DAY`. `INTERVAL -1 DAY` wil show the details of patrons whose books are already due, a day before. Also change the branchname to the appropriate ` i.homebranch = "VCL"`.
 
 ## Scheduling
 ```
 $ crontab -e
 $ 5 9 * * * python3 /home/villauser/scripts/koha_sms_v2.py # Every day 9:05 AM, script will be executed.
```

 ## Files
 There are two files `koha_sms_v1.py` and `koha_sms_v2.py`. v1 will use the number in `phone` field. v2 is specifically for my organization. It will check both `phone` and `mobile` field and will send message to one number. 
 
 ## Credits
 Nicole C. Baratta, ByWater Solutions, Koha List <br>
 Made the SQL Query  <br>
 A huge thanks to them :) <br>
 https://wiki.koha-community.org/wiki/SQL_Reports_Circulation#Patrons_w.2F_Books_Due_Tomorrow
