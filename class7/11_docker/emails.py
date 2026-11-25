from typing import Annotated

from fastapi import Depends

from storage import SENT_EMAILS


class EmailSender:
    def send(self, to: str, subject: str) -> None:
        SENT_EMAILS.append({"to": to, "subject": subject})
        print(f"[email] '{subject}' sent to {to}")


def get_email_sender() -> EmailSender:
    return EmailSender()


EmailSenderDep = Annotated[EmailSender, Depends(get_email_sender)]
