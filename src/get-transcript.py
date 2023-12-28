"""YouTubeからTranscriptをダウンロードするスクリプト.

実行方法の例:
"""
import logging
import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

_logger = logging.getLogger(__name__)


class _RunConfig:
    """スクリプト実行のためのオプション."""

    verbose: int  # ログレベル


def _main() -> None:
    video_url = ""
    video_id = video_url.split("v=")[-1]
    YouTubeTranscriptApi.get_transcript(video_id)


def _parse_args() -> _RunConfig:
    """スクリプト実行のための引数を読み込む."""
    parser = ArgumentParser(description="pyannote-audio v3を利用するために必要なモデルをダウンロードする.")

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="詳細メッセージのレベルを設定."
    )

    args = parser.parse_args()
    config = _RunConfig(**vars(args))

    return config


def _setup_logger(
    filepath: Path | None,  # ログ出力するファイルパス. Noneの場合はファイル出力しない.
    loglevel: int,  # 出力するログレベル
) -> None:
    """ログ出力設定

    Notes
    -----
    ファイル出力とコンソール出力を行うように設定する。
    """
    lib_logger = logging.getLogger(f"interim")

    _logger.setLevel(loglevel)
    lib_logger.setLevel(loglevel)

    # consoleログ
    console_handler = StreamHandler()
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(
        Formatter("[%(levelname)7s] %(asctime)s (%(name)s) %(message)s")
    )
    _logger.addHandler(console_handler)
    lib_logger.addHandler(console_handler)

    # ファイル出力するログ
    # 基本的に大量に利用することを想定していないので、ログファイルは多くは残さない。
    if filepath is not None:
        file_handler = RotatingFileHandler(
            filepath,
            encoding="utf-8",
            mode="a",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=1,
        )
        file_handler.setLevel(loglevel)
        file_handler.setFormatter(
            Formatter("[%(levelname)7s] %(asctime)s (%(name)s) %(message)s")
        )
        _logger.addHandler(file_handler)
        lib_logger.addHandler(file_handler)


if __name__ == "__main__":
    try:
        _main()
    except Exception:
        _logger.exception("Unhandled error.")
        sys.exit(1)
