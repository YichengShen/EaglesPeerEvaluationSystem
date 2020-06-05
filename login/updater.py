from datetime import datetime, date
from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler

from assessment.models import Assessment, Question, Answer, Result_set
from account.models import User

import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'theEaglesInstructor@gmail.com'
EMAIL_PASSWORD = 'jiujiu1016'


def check_for_new_assesments():
    print("scheduler working")
    d = datetime.now(timezone('US/Eastern'))
    fmt = '%Y-%m-%d'
    d = d.strftime(fmt)
    assessment_list = Assessment.objects.all()
    recipients =  []

    for i in assessment_list:
        if str(i.start_date) == d:
            recipients = i.course.students.all()
            #When ready to implement with real emails change this variable to r.email so that it sends it to the specific email
            """
            for r in recipients:
                print(r.email)
                msg = EmailMessage()
                msg['Subject'] = 'New Assessment'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = r.email
                msg.set_content('Peer Assessment ' + i.name + "is pending and opened today. Please go to your dashboard and complete it")

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    #smtp.send_message(msg)
            """
            msg = EmailMessage()
            msg['Subject'] = 'New Assessment'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = 'shenvw@bc.edu'
            msg.set_content('Peer Assessment ' + i.name + "is pending and opened today. Please go to your dashboard and complete it")
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            print("Email sent")

        else:
            print("no assignment")



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_new_assesments, 'interval', days=1)
    scheduler.start()
