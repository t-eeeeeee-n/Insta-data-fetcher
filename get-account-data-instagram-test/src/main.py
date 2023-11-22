from datetime import datetime, timedelta

from config.config import basic_info
from service.instagram.instagram_service import InstagramService
from service.spread.spread_service import SpreadService


class Main:
    SPREAD_ID = "1yDqCXJs2ezFPMAP3iPFKxPcn8c2jOw0odrrau9YMUfE"

    def exec(self):
        # リクエストパラメータ
        params = basic_info()  # リクエストパラメータ

        instagram_service = InstagramService()

        # フォロワー数、メディア数（投稿数）、メディアデータリスト
        user_discovery_data: dict = dict()
        response = instagram_service.get_user_business_discovery(params)["json_data"]["business_discovery"]
        for key, value in response.items():
            user_discovery_data[key] = value

        # ユーザーインサイト（日別）
        user_insights_day_data: dict = dict()
        response = instagram_service.get_user_insights(params)["json_data"]["data"]
        for insight in response:
            user_insights_day_data[insight["name"]] = insight["values"][0]["value"]

        self.insert_spread_total_data(user_discovery_data)
        self.insert_spread_day_data(user_insights_day_data)

    # アカウント分析（累計）インサート
    def insert_spread_total_data(self, user_discovery_data: dict):
        spread_service = SpreadService(self.SPREAD_ID)

        spread_service.get_worksheet("アカウント分析（累計）")
        spread_data = spread_service.get_all_value()
        header = spread_data[0]

        date = datetime.now().strftime('%Y/%m/%d')
        user_discovery_data["date"] = date

        target_cell = {
            "row_start": len(spread_data) + 1,
            "col_start": 1,
            "row_end": len(spread_data) + 1,
            "col_end": len(spread_data[0])
        }
        cell_list = spread_service.get_cell_list(target_cell)
        cell_list = self.input_cell_list_todal_data(header, user_discovery_data, cell_list)
        spread_service.worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    # アカウント分析（日別）インサート
    def insert_spread_day_data(self, user_insights_day_data: dict):
        spread_service = SpreadService(self.SPREAD_ID)

        spread_service.get_worksheet("アカウント分析（日別）")
        spread_data = spread_service.get_all_value()
        header = spread_data[0]

        date = (datetime.now() - timedelta(1)).strftime('%Y/%m/%d')
        user_insights_day_data["date"] = date
        user_insights_day_data["profile_views_rate"] = user_insights_day_data["profile_views"] / user_insights_day_data[
            "reach"]

        target_cell = {
            "row_start": len(spread_data) + 1,
            "col_start": 1,
            "row_end": len(spread_data) + 1,
            "col_end": len(spread_data[0])
        }
        cell_list = spread_service.get_cell_list(target_cell)
        cell_list = self.input_cell_list_day_data(header, user_insights_day_data, cell_list)
        spread_service.worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    @classmethod
    def input_cell_list_todal_data(cls, header, user_discovery_data, cell_list) -> list:
        for idx, column in enumerate(header):
            if "<date>" in column:
                cell_list[idx].value = user_discovery_data["date"]
            elif "<followers_count>" in column:
                cell_list[idx].value = user_discovery_data["followers_count"]
            elif "<media_count>" in column:
                cell_list[idx].value = user_discovery_data["media_count"]

        return cell_list

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
    print("update")