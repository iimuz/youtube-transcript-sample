---
title: YouTube Transcript Sample
date: 2023-12-26
lastmod: 2023-12-26
---

## 概要

YouTube から Transcript を取得するためのサンプルコードです。

## ファイル構成

- フォルダ
  - `.vscode`: VSCode の基本設定を記述します。
  - `src`: 開発するスクリプトを格納します。
- ファイル
  - `.gitignore`: [python 用の gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) です。
  - `.sample.env`: 環境変数のサンプルを記載します。利用時は `.env` に変更して利用します。
  - `LICENSE`: ライセンスを記載します。 MIT ライセンスを設定しています。
  - `pyproject.toml`/`setup.py`/`setup.cfg`: python バージョンなどを明記します。
  - `README.md`: 本ドキュメントです。

## 仮想環境の構築

仮想環境の構築には python 標準で付属している venv の利用を想定しています。

```sh
# create virtual env
python -m venv .venv

# activate virtual env(linux)
source .venv/bin/activate
# or (windows)
source .venv/Scripts/activate.ps1

# install packages
pip install -e .[dev,test]

# freeze version
pip freeze > constraint.txt
pip install -e .[dev,test] -c constraint.txt
```

## code style

コードの整形などはは下記を利用しています。

- [black](https://github.com/psf/black): python code formmater.
- [flake8](https://github.com/PyCQA/flake8): style checker.
- [isort](https://github.com/PyCQA/isort): sort imports.
- [mypy](https://github.com/python/mypy): static typing.
- docstirng: [numpy 形式](https://numpydoc.readthedocs.io/en/latest/format.html)を想定しています。
  - vscode の場合は [autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) 拡張機能によりひな型を自動生成できます。
