"""YouTubeからTranscriptをダウンロードするスクリプト.

実行方法の例:
    `python get_transcript.py https://www.youtube.com/watch?v=XXXXXXXXXXX -l=ja`
"""
import json
import logging
import sys
import urllib.parse
from argparse import ArgumentParser
from enum import Enum
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

_logger = logging.getLogger(__name__)


class _Language(Enum):
    """ダウンロードする言語."""

    JA = "ja"  # 日本語
    EN = "en"  # 英語


class _RunConfig(BaseModel):
    """スクリプト実行のためのオプション."""

    video_url: str  # YouTubeの動画URL
    languages: list[_Language]  # 取得する言語

    verbose: int  # ログレベル


def _main() -> None:
    """スクリプトのエントリポイント."""
    # 実行時引数の取得
    config = _parse_args()

    # データフォルダの設定
    data_dir = Path("data")
    interim_dir = data_dir / "interim"
    raw_dir = data_dir / "raw"

    # ログ設定
    loglevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(config.verbose, logging.DEBUG)
    log_filepath = interim_dir / (Path(__file__).stem + ".log")
    _setup_logger(filepath=log_filepath, loglevel=loglevel)
    _logger.info(config)

    parsed_url = urllib.parse.urlparse(config.video_url)
    query = urllib.parse.parse_qs(parsed_url.query)
    video_ids = query.get("v", [])
    if len(video_ids) != 1:
        _logger.error("Invalid video URL: %s", config.video_url)
        message = "Invalid video URL"
        raise ValueError(message)
    video_id = video_ids[0]

    _logger.info("video_id: %s", video_id)
    filepath = raw_dir / f"{video_id}.json"
    if filepath.exists():
        _logger.info("Skip downloading transcript: %s", filepath)
        return

    languages = [lang.value for lang in config.languages]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    filepath.write_text(json.dumps(transcript, indent=2, ensure_ascii=False))


def _parse_args() -> _RunConfig:
    """スクリプト実行のための引数を読み込む."""
    parser = ArgumentParser(
        description="pyannote-audio v3を利用するために必要なモデルをダウンロードする."
    )

    parser.add_argument("video_url", type=str, help="YouTubeの動画URL.")
    parser.add_argument(
        "-l",
        "--languages",
        choices=[v.value for v in _Language],
        nargs="+",
        help="取得する言語.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="詳細メッセージのレベルを設定.",
    )

    args = parser.parse_args()

    return _RunConfig(**vars(args))


def _setup_logger(
    filepath: Path | None,  # ログ出力するファイルパス. Noneの場合はファイル出力しない.
    loglevel: int,  # 出力するログレベル
) -> None:
    """ログ出力設定.

    Notes
    -----
    ファイル出力とコンソール出力を行うように設定する。
    """
    lib_logger = logging.getLogger("interim")

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
