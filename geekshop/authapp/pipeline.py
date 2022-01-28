from datetime import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    base_url = 'https://api.vk.com/method/users.get/'

    fields_for_requests = ['bdate', 'sex', 'about', 'photo_max_orig', 'uid']

    params = {
        'fields': ','.join(fields_for_requests),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)

    if api_response.status_code != 200:
        return

    api_data = api_response.json()['response'][0]

    if 'sex' in api_data:
        if api_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif api_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.UNKNOWN

    if 'about' in api_data:
        user.shopuserprofile.about_me = api_data['about']

    if 'bdate' in api_data:
        bdate = datetime.strptime(api_data['bdate'], "%d.%m.%Y").date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'photo_max_orig' in api_data:
        avatar_url = api_data['photo_max_orig']
        new_img = requests.get(avatar_url).content
        with open(f"{settings.BASE_DIR}/media/users/{api_data['first_name']}_avatar.jpg", 'wb') as handler:
            handler.write(new_img)
        user.avatar = f"users/{api_data['first_name']}_avatar.jpg "

    user.save()

