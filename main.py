import urllib.request
import requests
from bs4 import BeautifulSoup
import argparse
import urllib
import os
import time

# ログイン用のURL（ログイン画面にアクセスする）
login_url = 'https://panda.ecs.kyoto-u.ac.jp/cas/login?service=https%3A%2F%2Fpanda.ecs.kyoto-u.ac.jp%2Fsakai-login-tool%2Fcontainer'
base_url = 'https://panda.ecs.kyoto-u.ac.jp/direct'
# test: 配布資料を示すID
id = 'ae7eb08f-5eab-41d2-a8d8-229aac826b97'

# ログインページからlogin tokenを取得
def get_lt_value():
    # ログインページを取得
    res_page = session.get(login_url)
    soup = BeautifulSoup(res_page.text, 'html.parser')
    lt_value = soup.find('input', {'name': 'lt'})['value']
    return lt_value

# ログイン
def login(username, password, lt):
    login_data = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'submit': 'ログイン',
    }
    print(f'Logging in as: {username}...')
    return session.post(login_url, data=login_data)

def site():
    params_site = {
        '_limit': 50,
    }
    res_site = session.get(base_url + '/site' + '.json', params=params_site)
    for site in res_site.json()['site_collection']:
        print(f"{site['title']} ({site['id']})")

    return res_site


def ls(resource_id):
    res_content = session.get(base_url + '/content' + '/resources' + '/' + resource_id + '.json')
    # カレントディレクトリの項目
    for site in res_content.json()['content_collection']:
        if (site['type'] == 'org.sakaiproject.content.types.folder'):
            print('📁', end='')
        else:
            print('📄', end='')
        print(f"{site['name']}")

def download(site_id):
    # サイトのすべてのディレクトリ/ファイルを取得
    print('Fetching Files...')
    res_site = session.get(base_url + '/content' + '/site' + '/' + site_id + '.json')
    print('Downloading...')
    for content in res_site.json()['content_collection']:
        if (content['type'] != 'collection'):
            # data = urllib.request.urlopen(content['url']).read()
            os.makedirs('save' + content['container'], exist_ok=True)
            try:
                with open('save' + content['container'] + content['title'], mode='xb') as f:
                    res_file = session.get(content['url'])
                    f.write(res_file.content)
                    print(f'Download: {content['title']}')
            except FileExistsError:
                # print(f'Pass: {content['title']}')
                pass
    print('Done!')



# # カレントディレクトリの項目
# for site in res_content.json()['content_collection']:
#     # print(f"|--{site['name']}")
#     for child in site['resourceChildren']:
#         # 各childが項目を持つなら，それを取得
#         if (child['type'] == 'org.sakaiproject.content.types.folder'):
#             resource_id = child['resourceId']
#             res_content_child = session.get(base_url + '/content' + '/resources' + resource_id + '.json')
#             with open('a.json', 'w') as f:
#                 f.write(res_content_child.text)
#             for site_child in res_content_child.json()['content_collection']:
#                 if (site_child['type'] == 'org.sakaiproject.content.types.folder'):
#                     for site_grand_child in site_child['resourceChildren']:
#                         print("  ", end='')
#                         print(f"|--{site_grand_child['name']}")
#                     else:
#                         print(f"|--{site_child['name']}")
#                 else:
#                     print(f"|--{site_child['name']}")
#         else:
#             print(f"|--{site['name']}")



# # サイトのすべてのディレクトリ/ファイルを取得
# res_site = session.get(base_url + '/content' + '/site' + '/' + id + '.json')
# for content in res_site.json()['content_collection']:
#     print(content['container'])

# セッションを開始
session = requests.Session()

# print(get_lt_value())

# コマンドラインを受け付ける
parser = argparse.ArgumentParser(
    prog='PandA CLI'
)
parser.add_argument('ID')
parser.add_argument('password')
args = parser.parse_args()

res_login = login(args.ID, args.password, get_lt_value())

# セッション情報を取得してみる
res_session = session.get(base_url + '/session' + '.json')

# ログイン状態を確認
print(f"logged in as: {res_session.json()['session_collection'][0]['userEid']}")
# 現在のディレクトリ
# ls(id)
# res_site = site()

# download('2024-110-6115-000')

# 研究室のファイルをダウンロード
download(id)
