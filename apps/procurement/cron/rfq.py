from django_cron import CronJobBase, Schedule
from django.utils import timezone

from APP_COMPANY import APP_COMPANY
from ..models.rfq import RFQ


class RFQClosingCron(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "rfq_closing"
    file_path = "cron-demo.txt"

    def do(self):
        # rfq_closing_cron()
        message = f"Code: {self.code}    Current date: {timezone.now()}\n"
        with open(self.file_path, "a") as myfile:
            myfile.write(message)


def rfq_closing_cron():
    """
    RFQ Closing Cron Job
    """

    today = timezone.now()
    rfq_s = (
        RFQ.objects.select_related()
        .filter(required_date__gte=today)
        .values("id", "level", "open_status")
    )

    import os, json
    from django.core.mail import send_mail

    try:
        send_mail(
            "RFQ Closing Cron Job",
            f"This is the RFQ Closing Cron Job functionality testing mail. \n {json.dumps(rfq_s, indent=4)}",
            from_email=f"{APP_COMPANY['name']} <{os.getenv('EMAIL_HOST_USER')}>",
            fail_silently=False,
            recipient_list=["toure925@outlook.com"],
        )
    except:
        pass
