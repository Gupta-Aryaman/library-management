from .workers import celery
from datetime import datetime, timedelta
from celery.schedules import crontab
from jinja2 import Template
from flask import render_template
import os
import csv

from .models import *
from .extensions import db_session
from .helpers import send_email


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='1', hour='0'),
        send_daily_reminder.s(),
        name='sending daily reminder'
    )

    sender.add_periodic_task(
        crontab(minute='1', hour='00', day_of_month='*'),
        send_monthly_report.s(),
        name='sending monthly report'
    )

    sender.add_periodic_task(
        crontab(minute='01', hour='00'),
        auto_revoke_book.s(),
        name='revoking books post 7 days'
    )



@celery.task
def send_daily_reminder():
    template = """
    <p>
        Dear M/s. {{ name }},
    </p>
    <br />
    <p>
        We really miss you on our eLibrary.
    </p>
    <p>
        Check out our latest books. They are is always something new to learn everyday.
    </p>
    <p>
        Excited to see you soon.
    </p>
    <br />
    <p>
        Best Regards,
    </p>
    <p>
        Aryaman's eLibrary
    </p>
        <small>The story is truly finished not when the author adds the last period, but when the reader enters!</small>
        """
    all_users = db_session.query(User).all()
    template = Template(template)

    for user in all_users:
        is_active_today = db_session.query(LoginLogs).filter(LoginLogs.user_id==user.id).filter(LoginLogs.login_date == datetime.date.today() - timedelta(days=1)).count()
        
        if is_active_today == 0:
            address = user.email
            subject = "We miss you " + user.username.capitalize() + "!"
            rendered_template = template.render(name=user.username)
            send_email(address, subject, rendered_template)

    return 200

    


@celery.task()
def send_monthly_report():
    all_users = db_session.query(User).all()

    for user in all_users:

        borrowed_books = db_session.query(BorrowedBooks, Books, Sections).\
            join(Books, BorrowedBooks.book_id == Books.id).\
            join(Sections, Books.section == Sections.id).\
            filter(
                BorrowedBooks.user_id == user.id,
                BorrowedBooks.is_approved == True,
                BorrowedBooks.borrow_date > datetime.date.today() - timedelta(days=30)
            ).all()

        books = []
        pending_return_count = 0
        total_issued_books = len(borrowed_books)
        serial_number = 1

        for book in borrowed_books:
            books.append({
                "serial_number": serial_number,
                "title": book.Books.title,
                "author": book.Books.author,
                "section": book.Sections.section,
                "borrow_date": book.BorrowedBooks.borrow_date.strftime("%d/%m/%Y"),
                "return_pending_bool": book.BorrowedBooks.is_returned,
                "return_date": book.BorrowedBooks.scheduled_return_date.strftime("%d/%m/%Y"),
            })
            pending_return_count += 0 if book.BorrowedBooks.is_returned else 1
            serial_number += 1


        rendered_template = render_template("user_report.html", user=user.username, books=books, pending_return_count=pending_return_count)


        send_email(user.email, "[eLibrary]User Monthly Report", rendered_template)

    return 200


@celery.task
def auto_revoke_book():
    all_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.is_returned == False, BorrowedBooks.is_approved == True).all()

    for book in all_books:
        if book.scheduled_return_date < datetime.date.today():
            book.is_returned = True
            book.is_revoked = True
            book.actual_return_date = datetime.date.today()

            actual_book = db_session.query(Books).filter(Books.id == book.book_id).first()
            actual_book.available_copies += 1

            db_session.commit()

    return 200