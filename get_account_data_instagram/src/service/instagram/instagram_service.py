import json

import requests


class InstagramService:

    # Instagram基本表示API..................................................................

    # ユーザー https://developers.facebook.com/docs/instagram-basic-display-api/reference/user
    # IGユーザービジネスディスカバリー https://developers.facebook.com/docs/instagram-api/reference/ig-user/business_discovery?locale=ja_JP
    def get_user_data(self, params):
        """
        ***********************************************************************************
        【APIのエンドポイント】
        "https://graph.instagram.com/{api-version}/{user-id}?fields={fields}&access_token={access-token}"
        ***********************************************************************************
        """

        # エンドポイントに送付するパラメータ
        Params = dict()
        Params['user_id'] = params['instagram_account_id']
        Params['access_token'] = params['access_token']
        # エンドポイントURL
        url = params['endpoint_base'] + Params['user_id']
        # 出力
        return self.api_call(url, Params, 'GET')

    # メディア https://developers.facebook.com/docs/instagram-basic-display-api/reference/media
    def get_media_data(self, params, media_id):
        """
        ***********************************************************************************
        【APIのエンドポイント】
        "https://graph.instagram.com/{media-id}?fields={fields}&access_token={access-token}"
        ***********************************************************************************
        """
        Params = dict()
        Params['media_id'] = media_id
        Params['access_token'] = params['access_token']
        Params['fields'] = "id,caption,media_type,media_url"
        # エンドポイントURL
        url = params['endpoint_base'] + Params['media_id']
        # 出力
        return self.api_call(url, Params, 'GET')

    # InstagramグラフAPI..................................................................

    # IGメディアインサイト 写真と動画の指標 https://developers.facebook.com/docs/instagram-api/reference/ig-media/insights
    def get_media_insights(self, params, media_id):
        """
        ***********************************************************************************
        【APIのエンドポイント】
        "https://graph.facebook.com/{api-version}/{ig-media-id}/insights?metric={metric}&access_token={access-token}"
        ***********************************************************************************
        """
        Params = dict()
        Params['media_id'] = media_id
        Params['access_token'] = params['access_token']
        Params['metric'] = "engagement, impressions, reach, saved, video_views"
        # エンドポイントURL
        url = params['endpoint_base'] + Params['media_id'] + "/insights"
        # 出力
        return self.api_call(url, Params, 'GET')

    # Instagramユーザーインサイト https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
    def get_user_insights(self, params, since=None, util=None, period='day'):
        """
        ***********************************************************************************
        【APIエンドポイント】
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}&access_token={access-token}
        ***********************************************************************************
        """
        # エンドポイントに渡すパラメータ
        Params = dict()
        Params[
            'metric'] = 'follower_count,impressions,profile_views,reach, get_directions_clicks, text_message_clicks, website_clicks, email_contacts, phone_call_clicks'
        Params['period'] = period  # 集計期間
        if since is not None:
            Params['since'] = since
            Params['util'] = util
        Params['access_token'] = params['access_token']  # アクセストークン

        # エンドポイントURL
        url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'  # endpoint url

        # 出力
        return self.api_call(url, Params, 'GET')

    # Instagramユーザーインサイト https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
    def get_user_insights_lifetime(self, params, period='lifetime'):
        """
        ***********************************************************************************
        【APIエンドポイント】
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}&access_token={access-token}
        ***********************************************************************************
        """
        # エンドポイントに渡すパラメータ
        Params = dict()
        Params[
            'metric'] = 'audience_city, audience_country, audience_gender_age, audience_locale, online_followers'
        Params['period'] = period  # 集計期間
        Params['access_token'] = params['access_token']  # アクセストークン

        # エンドポイントURL
        url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'  # endpoint url

        # 出力
        return self.api_call(url, Params, 'GET')

    # IGユーザービジネスディスカバリー https://developers.facebook.com/docs/instagram-api/reference/ig-user/business_discovery?locale=ja_JP
    def get_user_business_discovery(self, params):
        """
        ***********************************************************************************
        【APIのエンドポイント】
        "https://graph.instagram.com/{api-version}/{user-id}?fields=business_discovery.username({user_name}){followers_count,media_count}&access_token={access-token}"
        ***********************************************************************************
        """

        # エンドポイントに送付するパラメータ
        Params = dict()
        Params['user_id'] = params['instagram_account_id']
        Params['access_token'] = params['access_token']
        Params[
            'fields'] = 'business_discovery.username(' + params[
            'user_name'] + '){followers_count,media_count,media{comments_count,like_count}}'
        # エンドポイントURL
        url = params['endpoint_base'] + Params['user_id']
        # 出力
        return self.api_call(url, Params, 'GET')

    # APIリクエスト用の関数
    @classmethod
    def api_call(cls, url, params, request_type):
        # リクエスト
        if request_type == 'POST':
            # POST
            req = requests.post(url, params)
        else:
            # GET
            req = requests.get(url, params)

        # レスポンス
        res = dict()
        res["url"] = url
        res["endpoint_params"] = params
        res["endpoint_params_pretty"] = json.dumps(params, indent=4)
        res["json_data"] = json.loads(req.content)
        res["json_data_pretty"] = json.dumps(res["json_data"], indent=4)

        # 出力
        return res
