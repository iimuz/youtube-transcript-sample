---
title: YouTube Transcript Sample
date: 2023-12-26
lastmod: 2024-01-07
---

## 概要

YouTube から Transcript を取得するためのサンプルコードです。

## ファイル構成

- フォルダ
  - `.github`: GitHubのworkflow設定を記述します。
  - `.vscode`: VSCodeの基本設定を記述します。
  - `src`: 開発するスクリプトを格納します。
- ファイル
  - `.cspell.json`: [CSpell](https://cspell.org/)の設定を記述します。
  - `.editorconfig`: Editorの共通設定を記述します。
  - `.gitignore`: 以下のignore設定を結合しています。
    - [python gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
    - [node gitignore](https://github.com/github/gitignore/blob/main/Node.gitignore)
  - `.prettierignore`: [prettier](https://prettier.io/)の設定を記述します。
  - `.sample.env`: 環境変数のサンプルを記載します。利用時は`.env`に変更して利用します。
  - `dprint.json`: dprintの設定を記述します。
  - `LICENSE`: ライセンスを記載します。MITライセンスを設定しています。
  - `package.json`: nodeのパッケージ情報を記載します。
  - `pyproject.toml`/`setup.py`/`setup.cfg`: python バージョンなどを明記します。
  - `README.md`: 本ドキュメントです。
  - `Taskfile.yml`: [task](https://taskfile.dev/)コマンドの設定を記述します。

## ローカル環境の構築

仮想環境などの構築は下記のコマンドで実行します。

```sh
# 実行だけできればよい場合
task init
# 開発環境もインストールする場合
task init-dev
```

## 実行方法

事前に下記が利用できるように環境を設定してください。

- [node.js](https://nodejs.org/en): 開発環境のlinterに利用します。
- [python](https://nodejs.org/en)
- [task](https://taskfile.dev/): タスクランナーとして利用します。

主なコマンドを下記に記載します。
その他の実行可能なタスクは`task -l`で確認してください。
また、スクリプトの引数についての詳細は、`hoge.py`で参照してください。

- 実行環境の構築
  - 実行だけできればよい場合: `task init`
  - 開発環境もインストールする場合: `task init-dev`
- トランスクリプトファイルを取得するスクリプトの実行: `python src/get_transcript.py https://www.youtube.com/watch?v=XXXXXXXXXXX`

## code style

コードの整形などはは下記を利用しています。

- json, markdown, toml
  - [dprint](https://github.com/dprint/dprint): formatter
- python
  - [ruff](https://github.com/astral-sh/ruff): python linter and formatter.
  - [mypy](https://github.com/python/mypy): static typing.
  - docstring: [numpy形式](https://numpydoc.readthedocs.io/en/latest/format.html)を想定しています。
    - vscodeの場合は[autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)拡張機能によりひな型を自動生成できます。
- yml
  - [prettier](https://prettier.io/): formatter

## 保存形式

出力はjsonファイルで下記のような形式で保存します。

```json
[
  {
    "text": "hoge",
    "start": 0.75,
    "duration": 8.0
  },
  {
    "text": "geho",
    "start": 5.6,
    "duration": 7.1
  }
]
```
