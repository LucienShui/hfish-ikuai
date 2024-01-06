from requests import post, Session
from geoip2.database import Reader
from json import load
from typing import List, Tuple
import os


class IKuai:
    def __init__(self, username: str, md5_password: str, url: str):
        self.url = url
        self.session = Session()

        login_response = self.session.post(
            self.url + '/Action/login', json={'username': username, 'passwd': md5_password}).json()

        assert login_response['Result'] == 10000 and login_response['ErrMsg'] == 'Success', 'login failed'

    def post(self, json: dict) -> dict:
        return self.session.post(self.url + '/Action/call', json=json).json()


def get_attack_ip_list(hfish_api: str) -> List[str]:
    honeypot_response = post(hfish_api, json={'start_time': 0, 'end_time': 0, 'source': 1}).json()
    attack_ip_list = honeypot_response['data']['attack_ip']
    return attack_ip_list


def main():
    hfish_api = os.environ['HFISH_API']
    username: str = os.environ['IKUAI_USERNAME']
    md5_password: str = os.environ['IKUAI_MD5PASSWORD']
    ikuai_api = os.environ['IKUAI_API']

    attack_ip_list = get_attack_ip_list(hfish_api)

    print(f'total attack ip {len(attack_ip_list)}')

    ip_list: List[Tuple[str, str]] = []

    with Reader('Country.mmdb') as reader:
        for ip in attack_ip_list:
            response = reader.country(ip)
            iso_code = response.country.iso_code
            if iso_code not in ['CN', 'PRIVATE']:
                ip_list.append((ip, iso_code))

    print(f'set {len(ip_list)} black ip to ikuai')

    ikuai = IKuai(username, md5_password, ikuai_api)
    with open('ikuai_request.json') as f:
        ikuai_request = load(f)
    ikuai_request["param"]['addr_pool'] = ",".join([ip for ip, _ in ip_list])
    ikuai_request["param"]["comment"] = ",".join([code for _, code in ip_list])
    ipgroup_response = ikuai.post(ikuai_request)

    assert ipgroup_response['Result'] == 30000 and ipgroup_response['ErrMsg'] == 'Success'

    print('done')


if __name__ == '__main__':
    main()
