import hashlib

from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Count

from .models import *
from .exceptions import CustomException


day = timezone.now() - timezone.timedelta(days=1)
week = timezone.now() - timezone.timedelta(days=7)
month = timezone.now() - timezone.timedelta(days=30)

def create_client_api_key(client):
    client_id = client.id
    client_name = client.client_name
    hash_string = "%s:%s" % (str(client_id), client_name)
    api_key = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    client.api_key = api_key
    client.save()
    return api_key

def create_client(client_name, email):
    """"""
    try:
        client = Client.objects.create(client_name=client_name, email=email)
    except IntegrityError:
        raise CustomException('Client Already Exist', 5001)

    return create_client_api_key(client)

def get_client(client_name, api_key):
    try:
        return Client.objects.get(api_key=api_key, client_name=client_name)
    except Client.DoesNotExist:
        raise CustomException('Invalid api_key. No client exist with this api key.', 5002)

def create_client_data(page_name, timestamp,
                location, user_info, session_info, client):
    """
    :return:
    """
    try:
        username = user_info['username']
        useremail = user_info['email']
    except KeyError:
        raise CustomException('userinfo does not have valid pair of data.', 5003)
    name = user_info.get('name')

    try:
        sessionkey = session_info['sessionkey']
        login_at = session_info['login_at']
    except KeyError:
        raise CustomException('sessioninfo does not have valid pair of data.')
    logout_at = session_info.get('logout_at', None)

    try:
        country = location['country']
        city = location['city']
    except KeyError:
        raise CustomException('location does not have valid pair of data.')
    try:
        user = UserInfo.objects.get(username=username, client=client)
    except UserInfo.DoesNotExist:
        user = UserInfo.objects.create(username=username, client=client,
                                       name=name, email=useremail)

    session = SessionInfo.objects.create(sessionkey=sessionkey,
                                         login_at=login_at, logout_at=logout_at)
    try:
        location = Location.objects.get(country=country, city=city)
    except Location.DoesNotExist:
        location = Location.objects.create(country=country, city=city)

    ClientData.objects.create(page_name=page_name, timestamp=timestamp,
                              user=user, session=session, client=client,
                              location=location)

    return

def get_client_data(client, page_name):
    average_time = get_average_time_on_page(client, page_name)
    number_of_users = get_number_users(client, page_name)
    number_of_page_views = get_number_of_page_view(client, page_name)

    result = {'page_name': page_name,
              'client_name': client.client_name,
              'client_id': client.id,
              'number_of_unique_user': number_of_users}
    result.update(average_time)
    result.update({'views': number_of_page_views})
    return result


def get_average_time_on_page(client, page_name):
    """
    """
    total_seconds = 0
    client_data = ClientData.objects.filter(client=client, page_name=page_name)
    no_of_sessions = client_data.count()
    for obj in client_data:
        session = obj.session
        if session.logout_at:
            time_diff = obj.session.logout_at - session.login_at

        else:
            time_diff = timezone.now() - session.login_at

        total_seconds += time_diff.total_seconds()

    average_duration = total_seconds/no_of_sessions
    return {'average_session_duration': average_duration}

def get_number_users(client, page_name):
    """
    :return:
    """



    number_of_user_last_day =  ClientData.objects.filter(client=client, page_name=page_name,
                                                         session__login_at__gt=day
                                                         ).order_by().values('user').distinct().count()
    number_of_user_last_week = ClientData.objects.filter(client=client, page_name=page_name,
                                                         session__login_at__gt=week
                                                         ).order_by().values('user').distinct().count()
    number_of_user_last_month = ClientData.objects.filter(client=client, page_name=page_name,
                                                         session__login_at__gt=month
                                                         ).order_by().values('user').distinct().count()

    number_of_vistors = {'last_day': number_of_user_last_day,
                         'last_week': number_of_user_last_week,
                         'last_month': number_of_user_last_month}

    return number_of_vistors


def get_number_of_page_view(client, page_name):
    """
    :param client:
    :param page_name:
    :return:
    """
    number_of_visitors_last_day = ClientData.objects.filter(client=client, page_name=page_name,
                                                        session__login_at__gt=day
                                                        ).values('location__city', 'location__country'
                                                                 ).annotate(page_views=Count('location__city'))
    number_of_visitors_last_month = ClientData.objects.filter(client=client, page_name=page_name,
                                                            session__login_at__gt=month
                                                            ).values('location__city', 'location__country'
                                                                     ).annotate(page_views=Count('location__city'))


    day_views = change_visitor_data(number_of_visitors_last_day)
    monthly_views = change_visitor_data(number_of_visitors_last_month)

    return {'day_views': day_views, 'monthly_views': monthly_views}

def get_client_current_users(client, page_name):
    """
    :param client:
    :param page_name:
    :return:
    """
    online_users = ClientData.objects.filter(client=client, page_name=page_name,
                              session__logout_at__exact=None
                              ).annotate(online_users=Count('user')).values('online_users').distinct()

    return online_users[0]
def change_visitor_data(visitor_list):
    """
    :param visitor_list:
    :return:
    """
    return [{'views': obj['page_views'],
             'country': obj['location__country'],
             'city': obj['location__city']
            }
            for obj in list(visitor_list)]