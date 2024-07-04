import requests
from bs4 import BeautifulSoup
import argparse

# ログイン用のURL（ログイン画面にアクセスする）
login_url = 'https://panda.ecs.kyoto-u.ac.jp/cas/login?service=https%3A%2F%2Fpanda.ecs.kyoto-u.ac.jp%2Fsakai-login-tool%2Fcontainer'
base_url = 'https://panda.ecs.kyoto-u.ac.jp/direct'

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
    return session.post(login_url, data=login_data)

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

# params_site = {
#     '_limit': 50,
# }
# res_site = session.get(base_url + '/site' + '.json', params=params_site)
# for site in res_site.json()['site_collection']:
#     print(site['title'], site['id'])

# test: 配布資料を示すID
id = 'ae7eb08f-5eab-41d2-a8d8-229aac826b97'

# サイトのすべてのディレクトリ/ファイルを取得
# res_content = session.get(base_url + '/content' + '/site' + '/' + id + '.json')
# for site in res_content.json()['content_collection']:
#     print(site['title'])

res_content = session.get(base_url + '/content' + '/resources' + '/' + id + '.json')

# カレントディレクトリの項目
for site in res_content.json()['content_collection']:
    print(f"|--{site['name']}")
    for child in site['resourceChildren']:
        # 各childが項目を持つなら，それを取得

        if (child['type'] == 'org.sakaiproject.content.types.folder'):
            resource_id = child['resourceId']
            res_content_child = session.get(base_url + '/content' + '/resources' + resource_id + '.json')
            # print(res_content_child.text)
            for site_child in res_content_child.json()['content_collection']:
                # if (site_child['type'] == 'org.sakaiproject.content.types.folder'):
                #     for site_grand_child in site_child['resourceChildren']:
                #         print("  ", end='')
                #         print(f"|--{site_grand_child['name']}")
                #     else:
                #         print("  ", end='')
                #         print(f"|--{site_child['name']}")
                    print("  ", end='')
                    print(f"|--{site_child['name']}")
        else:
            print(f"|--{site['name']}")