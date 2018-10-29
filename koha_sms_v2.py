"""

Koha-SMS
Script by mK
muneeb.k@outlook.com

A Script to Send SMS to patrons whose books are going to due or already due.
Add a crontab entry to execute this script.

"""

import pymysql.cursors
import requests

# API key for the SMS Application
headers = {
    'Authorization': 'AccessKey 1234567890',
}
# Connecting MySQL DB
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             db='kohadatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    # Create a new record
    sql = '''SELECT p.cardnumber, p.surname, p.branchcode, p.firstname, p.mobile, p.phone,
 co.date_due, i.barcode, b.title, b.author
FROM borrowers p 
LEFT JOIN issues co ON (co.borrowernumber=p.borrowernumber) 
LEFT JOIN items i ON(co.itemnumber=i.itemnumber)
LEFT JOIN biblio b ON (b.biblionumber=i.biblionumber)
WHERE DATE(co.date_due) = DATE_ADD(curdate(), INTERVAL 1 DAY)
 AND i.homebranch = "VCL" 
ORDER BY p.surname ASC
'''
    cursor.execute(sql)
    result = list(cursor.fetchall())
    print(result)

    # This will iterate with each result we got from the DB
    for i in range(len(result)):
        d = result[i].get("date_due").strftime('%m/%d/%y')
        message = "Dear " + result[i].get("firstname") + " " + result[i].get("surname") + "\n" "Your book : " + result[
            i].get(
            "title") + " is due on " + d + "\n" + "Please return or renew them ASAP. Overdue items will accrue fines at the rate of MVR 5.00 per day per item." + "\n\n" + "Now you can renew through OPAC : \nlibrary.villacollege.edu.mv \n\n" + "Villa College Library\n" + "Email: xxxxx@villacollege.edu.mv\n" + "Ph: xxxxxxx"
        # This Condition is specifically for my work environment, Villa College - Maldives
        # Check whether there is a number in the field or not. Maldives  phone no has only 7 digits. 960 is the international code.

        if (len(result[i].get("phone"))) >= 7:

            if result[i].get("phone")[:3] == "960":
                mob_no = result[i].get("phone")[:10]

            else:
                mob_no = result[i].get("phone")[:7]

        elif (len(result[i].get("mobile"))) >= 7:

            if result[i].get("mobile")[:3] == "960":

                mob_no = result[i].get("mobile")[:10]

            else:
                mob_no = result[i].get("mobile")[:7]

        else:
            mob_no = 0
            print("No Number, Card No: " + result[i].get("cardnumber"))

        data = dict(body=message, recipients=mob_no, sender_id='vc-library')
        
        if mob_no != "0":
            response = requests.post('https://rest.msgowl.com/messages', headers=headers, data=data)

    connection.close()
