import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SpreadService:
    SERVICE_ACCOUNT_JSON_FILE_NAME = "./config/applyer-data.json"
    SCOPE = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    def __init__(self, spread_id):
        self.spreadsheet: gspread.Spreadsheet = gspread.authorize(
            ServiceAccountCredentials.from_json_keyfile_name(
                self.SERVICE_ACCOUNT_JSON_FILE_NAME,
                self.SCOPE
            )
        ).open_by_key(spread_id)
        self.worksheet: gspread.worksheet = None

    def get_worksheet(self, sheet_name):
        self.worksheet: gspread.worksheet = self.spreadsheet.worksheet(sheet_name)

    # スプレッド全て取得
    def get_all_value(self) -> list:
        list_of_lists = list(filter(self.row_none, self.worksheet.get_all_values()))
        return list_of_lists

    @staticmethod
    def row_none(row: list) -> bool:
        return row[0] != ""

    # ヘッダー取得
    def get_header(self) -> list:
        header = self.worksheet.row_values(1)
        return header

    # 範囲指定取得
    def get_cell_list(self, target_cell: dict) -> list:
        cell_list = self.worksheet.range(
            target_cell["row_start"], target_cell["col_start"],
            target_cell["row_end"], target_cell["col_end"],
        )
        return cell_list

    # 範囲更新
    def update_cell_list(self, cell_list: list, data_list: list):
        for i, data in enumerate(data_list):
            cell_list[i].value = data
        self.worksheet.update_cells(cell_list)

    def input_data_to_spread(self, to_spread_data_list, header):
        """
            スプレッドにデータ投入
        """

        print("google認証------------------------------")
        end_row = int(to_spread_data_list[len(to_spread_data_list) - 1][0])
        print(end_row)
        cell_list = self.worksheet.range(2, 1, end_row, header.index("更新日時") + 1)
        print(cell_list)

        for data_array in to_spread_data_list:
            no = data_array[0]
            data_array.pop(0)
            for c, _ in enumerate(header):
                col_num = (int(no) - 2) * (header.index("更新日時") + 1) + c
                if c == header.index("求人ID"):
                    cell_list[col_num].value = data_array[0]
                elif c == header.index("転記ステータス"):
                    cell_list[col_num].value = data_array[1]
                elif c == header.index("エラー"):
                    cell_list[col_num].value = data_array[2]
                elif c == header.index("更新日時"):
                    cell_list[col_num].value = data_array[3]

        self.worksheet.update_cells(cell_list)

