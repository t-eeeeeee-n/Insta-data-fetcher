from main import Main


def lambda_handler(event, lambda_context):
    """
    インスタグラム情報取得
    Author:
        Tensho arai
    """
    try:
        print("開始========================================")
        Main().exec()
        print("終了========================================")
    except Exception as e:
        print(str(e))


