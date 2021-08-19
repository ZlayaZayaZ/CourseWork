import time
from tqdm import tqdm
import requests
from pprint import pprint


class YaUploader:
    def __init__(self, token_yd: str, token_vk: str):
        self.token_yd = token_yd
        self.token_vk = token_vk

    def uploader_ava_vk(self, name_folder, id_user: str, count=5):
        """
        Функция сохраняет на yandex.disc фотографии аватарок пользователя vk.com,
        чей id указан при вызове функции. Количество фотографий задается параметром
        count(по умолчанию = 5). Фотографии идут в антихронологическом порядке.
        """
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {
            'owner_id': id_user,
            'album_id': 'profile',
            'rev': '1',
            'extended': '1',
            'photo_sizes': '1',
            'count': count,
            'access_token': token_vk,
            'v': '5.131'
        }
        req = requests.get(url_vk, params_vk).json()
        wild_json = req['response']['items']
        photos = {}
        for photo in wild_json:
            type_max = photo['sizes'][-1]['type']
            url_max = photo['sizes'][-1]['url']
            photos[photo['id']] = {'likes': photo['likes']['count'], 'type': type_max, 'url': url_max,
                                   'date': photo['date']}
        self.upload_ya(name_folder, photos)
        return 'Фотографии профиля загружены на yandex.disk'

    def uploader_wall_vk(self, name_folder, id_user: str, count=5):
        """
        Функция сохраняет на yandex.disc фотографии со стены пользователя vk.com,
        чей id указан при вызове функции. Количество фотографий задается параметром
        count(по умолчанию = 5). Фотографии идут в антихронологическом порядке.
        """
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {
            'owner_id': id_user,
            'album_id': 'wall',
            'rev': '1',
            'extended': '1',
            'photo_sizes': '1',
            'count': count,
            'access_token': token_vk,
            'v': '5.131'
        }
        req = requests.get(url_vk, params_vk).json()
        wild_json = req['response']['items']
        photos = {}
        for photo in wild_json:
            type_max = photo['sizes'][-1]['type']
            url_max = photo['sizes'][-1]['url']
            photos[photo['id']] = {'likes': photo['likes']['count'], 'type': type_max, 'url': url_max,
                                   'date': photo['date']}
        self.upload_ya(name_folder, photos)
        return 'Фотографии со стены загружены на yandex.disk'

    def upload_ya(self, save_folder, photos):
        """
        Сохраняет файлы на yandex.disk по ссылкам расположенным в словаре photos, передаваемым извне.
        """
        api_base_url = 'https://cloud-api.yandex.net/'
        headers = {
            'accept': 'application/json',
            'authorization': f'OAuth {self.token_yd}'
        }
        requests.put(api_base_url + 'v1/disk/resources', params={'path': save_folder}, headers=headers)
        home_json = []
        list_photo = []
        upload_url = api_base_url + 'v1/disk/resources/upload'
        for i in tqdm(photos):
            photo_url = photos[i]['url']
            if str(photos[i]['likes']) in list_photo:
                photo_name = str(photos[i]['likes']) + '_' + str(photos[i]['date'])
                r = requests.post(upload_url,
                                  headers=headers,
                                  params={
                                      'path': save_folder + '/' + photo_name,
                                      'url': photo_url
                                  })
            else:
                photo_name = str(photos[i]['likes'])
                r = requests.post(upload_url,
                                  headers=headers,
                                  params={
                                      'path': save_folder + '/' + photo_name,
                                      'url': photo_url
                                  })
            list_photo.append(photo_name)
            home_json.append({'file_name': photo_name, 'size': photos[i]['type']})
            time.sleep(1)
        pprint(home_json)


if __name__ == '__main__':
    """
    Получить от пользователя токен yandex.disk, токен vk,
    id интересующего пользователя и имя папки для сохранения файлов.
    """
    token_yd = ...
    token_vk = ...
    name_folder_wall = ...
    name_folder_ava = ...
    id_user = ...
    uploader = YaUploader(token_yd, token_vk)
    result1 = uploader.uploader_wall_vk(name_folder_wall, id_user, 10)
    result2 = uploader.uploader_ava_vk(name_folder_ava, id_user, 10)
    print(result1)
    print(result2)
