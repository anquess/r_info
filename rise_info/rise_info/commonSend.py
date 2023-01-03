from django.core.mail import send_mail
from django.template.loader import render_to_string

from rise_info.settings import EMAIL_HOST_USER, DEBUG


def addCommentSendMail(comment, url, request):
    context = {
        'info': comment.info,
        'comment': comment,
        'url': url,
    }
    dest_list = []
    subject = '【' + str(comment.info.get_info_type_display) + '】' \
        + str(comment.info) + 'にコメントが追加されました'
    for adr in comment.info.addresses.all():
        dest_list.append(adr.mail)
    try:
        if not DEBUG:
            send_mail(
                subject,
                render_to_string('mail_comment_add.txt', context),
                EMAIL_HOST_USER, dest_list, fail_silently=False,)
        return None
    except Exception as e:
        return e
