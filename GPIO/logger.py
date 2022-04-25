# LOG表示関連をまとめたヘッダーファイル
# コンソール出力用ハンドラー終了
import logging
import logging.handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    ' %(module)s -  %(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# ログファイルに出力する
# ローテーティングファイルハンドラを作成
rh = logging.handlers.RotatingFileHandler(
        r'./log/app.log', 
        encoding='utf-8',
        maxBytes=100000,    # 100kB
        backupCount=3
    )

rh.setFormatter(logging.Formatter(
    ' %(module)s -  %(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(rh)