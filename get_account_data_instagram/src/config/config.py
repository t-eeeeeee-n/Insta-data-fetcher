import os
from dotenv import load_dotenv


def basic_info():
    load_dotenv()
    config = dict()
    config["access_token"] = os.getenv('ACCESS_TOKEN')
    config["app_id"] = os.getenv('APP_ID')
    config["app_secret"] = os.getenv('APP_SERCRET')
    config['instagram_account_id'] = os.getenv('INSTAGRAM_ACCOUNT_ID')
    config["version"] = os.getenv('VERSION')
    config["graph_domain"] = os.getenv('GRAPH_DOMAIN')
    config["endpoint_base"] = os.getenv('GRAPH_DOMAIN') + os.getenv('VERSION') + '/'
    config["user_name"] = os.getenv('USER_NAME')
    config["spread_id"] = os.getenv('SPREAD_ID')

    # 出力
    return config
