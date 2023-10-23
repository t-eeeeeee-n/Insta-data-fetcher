from datetime import datetime, timedelta

import pytz

from config import basic_info
from all.src.service.instagram.instagram_service import InstagramService
from all.src.service.spread.spread_service import SpreadService
import os


class Main:
    def exec(self):
        # リクエストパラメータ
        params = basic_info()  # リクエストパラメータ

        instagram_service = InstagramService()

        # フォロワー数、メディア数（投稿数）、メディアデータリスト
        user_usiness_discovery_data: dict = dict()
        response = instagram_service.get_user_business_discovery(params)["json_data"]["business_discovery"]
        for key, value in response.items():
            user_usiness_discovery_data[key] = value

        # メディア単体データ詳細
        media_data: dict = dict()
        response = instagram_service.get_media_data(params, "17991133829270797")["json_data"]
        for key, value in response.items():
            media_data[key] = value

        # メディア単体詳細インサイト
        media_insights_data: dict = dict()
        response = instagram_service.get_media_insights(params, "17978345465233162")["json_data"]["data"]
        for insight in response:
            media_insights_data[insight["name"]] = insight["values"][0]["value"]

        # ユーザーインサイト（日別）
        jst = pytz.timezone('Asia/Tokyo')
        # 現在の日付と時刻を取得（JSTで）
        current_datetime_jst = datetime.now(jst)
        # 今日の00:00の日付を作成（JSTで）
        today_midnight_jst = current_datetime_jst.replace(hour=0, minute=0, second=0, microsecond=0)
        # timedeltaを使用して1日を表すオブジェクトを作成
        one_day = timedelta(days=1)
        # 昨日の00:00の日付を計算（JSTで）
        yesterday_midnight_jst = today_midnight_jst - one_day
        # datetimeオブジェクトをUNIX時間に変換
        since = int(yesterday_midnight_jst.timestamp())
        util = int(today_midnight_jst.timestamp())

        user_insights_day_data: dict = dict()
        response = instagram_service.get_user_insights(params, since, util)["json_data"]["data"]
        for insight in response:
            user_insights_day_data[insight["name"]] = insight["values"][0]["value"]

        # ユーザーインサイト（累計？）
        user_insights_lifetime_data: dict = dict()
        response = instagram_service.get_user_insights_lifetime(params)["json_data"]["data"]
        for insight in response:
            user_insights_lifetime_data[insight["name"]] = insight["values"][0]["value"]

        # response = instagram_service.get_user_insights_lifetime(params)["json_data"]["data"]
        # # 結果出力
        # for insight in response:
        #     print(insight['title'] + "（" + insight['description'] + ")" + " (" + insight['period'] + ")")
        #     for value in insight['values']:  # loop over each value
        #         print("\t" + "value: " + str(value['value']))

        self.insert_spread_day_data(user_insights_day_data)

    # アカウント分析（日別）インサート
    def insert_spread_day_data(self, user_insights_day_data: dict):
        spread_service = SpreadService(os.getenv("SPREAD_ID"))

        spread_service.get_worksheet("アカウント分析（日別）")
        spread_data = spread_service.get_all_value()
        header = spread_data[0]

        date = (datetime.now()-timedelta(1)).strftime('%Y/%m/%d')
        user_insights_day_data["date"] = date
        user_insights_day_data["profile_views_rate"] = user_insights_day_data["profile_views"]/user_insights_day_data["reach"]

        target_cell = {
            "row_start": len(spread_data)+1,
            "col_start": 1,
            "row_end": len(spread_data)+1,
            "col_end": len(spread_data[0])
        }
        cell_list = spread_service.get_cell_list(target_cell)
        cell_list = self.input_cell_list_day_data(header, user_insights_day_data, cell_list)
        spread_service.worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    @classmethod
    def input_cell_list_day_data(cls, header, user_insights_day_data, cell_list) -> list:
        for idx, column in enumerate(header):
            if "<date>" in column:
                cell_list[idx].value = user_insights_day_data["date"]
            elif "<follower_count>" in column:
                cell_list[idx].value = user_insights_day_data["follower_count"]
            elif "<profile_views>" in column:
                cell_list[idx].value = user_insights_day_data["profile_views"]
            elif "<impressions>" in column:
                cell_list[idx].value = user_insights_day_data["impressions"]
            elif "<reach>" in column:
                cell_list[idx].value = user_insights_day_data["reach"]
            elif "<get_directions_clicks>" in column:
                cell_list[idx].value = user_insights_day_data["get_directions_clicks"]
            elif "<text_message_clicks>" in column:
                cell_list[idx].value = user_insights_day_data["text_message_clicks"]
            elif "<website_clicks>" in column:
                cell_list[idx].value = user_insights_day_data["website_clicks"]
            elif "<email_contacts>" in column:
                cell_list[idx].value = user_insights_day_data["email_contacts"]
            elif "<phone_call_clicks>" in column:
                cell_list[idx].value = user_insights_day_data["phone_call_clicks"]
            elif "<profile_views_rate>" in column:
                cell_list[idx].value = user_insights_day_data["profile_views_rate"]

        return cell_list


if __name__ == "__main__":
    Main().exec()
