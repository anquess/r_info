from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string


from addresses.models import Addresses
from eqs.models import DepartmentForEq
from rise_info.settings import EMAIL_HOST_USER, DEBUG

from functools import reduce
import operator


def add_addresses(request, info):
    add_addresses = request.POST.getlist('add_addresses[]')
    for address in info.addresses.all():
        if address.created_by == request.user \
                and not(address in add_addresses):
            info.addresses.remove(address)
    for address in add_addresses:
        info.addresses.add(address)
    info.save()


def addCommentSendMail(comment, url, request):
    context = {
        'info': comment.info,
        'comment': comment,
        'url': url,
    }
    dest_list = []
    subject = '【' + str(comment.info.get_info_type_display()) + '】' \
        + str(comment.info) + 'にコメントが追加されました'
    for adr in comment.info.addresses.all():
        dest_list.append(adr.mail)
    try:
        send_mail(
            subject,
            render_to_string('mail_comment_add.txt', context),
            EMAIL_HOST_USER,
            dest_list,
            fail_silently=False,)
        messages.add_message(request, messages.INFO, 'コメント受信者に配信しました')
    except Exception as e:
        messages.add_message(
            request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))
        return False
    return True


def notifyRegistration(info, request):
    departments = DepartmentForEq.objects.filter(
        Q(eq_class__eqtype__tech_supo=info)).distinct()
    q_departments = reduce(operator.or_, (
        Q(department__id__contains=i.id)for i in departments))
    q_is_receiver = Q(is_receive_info_from_offices=True)
    dests = Addresses.objects.filter(
        q_departments).filter(q_is_receiver).distinct()
    recipient_list = [dest.mail for dest in dests]
    subject = '【' + str(info.get_info_type_display()) + '】'\
        + str(info.title) + 'が登録されました'
    context = {
        'info': info,
    }
    message = render_to_string('mail_techSupo_add.txt', context)
    try:
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, '配信されました')
    except Exception as e:
        messages.add_message(
            request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))
        return e
    return 1
