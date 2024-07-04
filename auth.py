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
        'submit': 'ログイン'
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

print(f"logged in as: {res_session.json()['session_collection'][0]['userEid']}")