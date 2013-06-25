from celery import task
from django.conf import settings
from models import *

import praw


@task(ignore_result=True)
def process_reddit_queue():
    r = praw.Reddit(settings.REDDIT_USER_AGENT)

    r.login(settings.REDDIT_USER, settings.REDDIT_PASSWORD)

    new_since_last = r.user.get_unread(limit=None)

    invalid_messages = []

    for message in new_since_last:
        if message is None:
            continue

        if not message.subject.lower() == settings.REDDIT_AUTH_SUBJECT.lower():
            message.mark_unread()
            continue

        split_body = message.body.splitlines()

        if split_body[0] != "":
            if len(split_body[0]) == 64:
                rc = RedditConfirmation.objects.get(key__exact=split_body[0])
                if rc:
                    rc.confirm()
                else:
                    invalid_messages.append(message)

                continue

            else:
                invalid_messages.append(message)

                continue

        else:
            invalid_messages.append(message)

            continue

    for message in invalid_messages:
        reply_string = 'Invalid Auth Code. Please make sure your code is the first and only line of your message. '
        reply_string += 'Your subject was correct, so please use the same subject. Do not reply to this message, '
        reply_string += 'it will not work.'
        message.reply(reply_string)
        message.mark_read()
