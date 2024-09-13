from celery import shared_task   
from celery.utils.log import get_task_logger
from .email import send_otp,send_welcome_mail, update_status_mail

logger = get_task_logger(__name__)


@shared_task(name="send_otp_task", bind=True)
def send_otp_task(self, email, otp, name, template_name):
    logger.info("Sent OTP to your registered Email")
    return send_otp( email=email, otp = otp, name = name, template_name = template_name)

@shared_task(name="send_welcome_mail_task", bind=True)
def send_welcome_mail_task(self, email, firstname, lastname):
    logger.info("Sent Welcome email to your registered Email")
    return send_welcome_mail( email=email, firstname = firstname,  lastname = lastname)

@shared_task(name="update_status_mail_task", bind=True)
def update_status_mail_task(self, email,firstname,lastname,username,status):
    logger.info("Sent Status Update to the Registered mail")
    return update_status_mail( email=email, firstname = firstname,  lastname = lastname,username = username, status = status)


