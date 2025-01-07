from celery import shared_task
from datetime import datetime, timedelta
from .models import Borrow , Book , Member
import logging


logger = logging.getLogger(__name__)

@shared_task
def notify_overdue_books():
    
    overdue_borrows = Borrow.objects.filter(return_date__lt=datetime.now() , returned=False)
    for borrow in overdue_borrows:
        # Replace with actual notification logic (e.g., email or SMS)
        logger.info(f'Overdue book: {borrow.book.title}, Borrower: {borrow.member.name}')
    
