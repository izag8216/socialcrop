<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:E67E22,100:E74C3C&height=220&section=header&text=socialcrop&fontSize=70&fontColor=FDF6E3&fontAlignY=42&desc=Social%20Media%20Image%20Resizer%20CLI&descSize=18&descAlignY=62" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/tests-59-brightgreen" alt="Tests" />
  <img src="https://img.shields.io/badge/coverage-92%25-green" alt="Coverage" />
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License" />
  <img src="https://img.shields.io/badge/linter-ruff-purple" alt="Ruff" />
  <img src="https://img.shields.io/badge/API-zero-orange" alt="Zero API" />
</p>

**socialcrop** は API 不要の CLI ツール。1枚の画像を 15以上のSNSプラットフォーム向けにリサイズ。スマートクロップ、バッチ出力、カスタムプリセット -- すべてオフライン、ローカル完結。

## 特徴

- **15+ プラットフォームプリセット** -- Instagram, Twitter/X, LinkedIn, YouTube, Facebook, TikTok, Pinterest, Discord, Slack, OpenGraph, Twitter Card, GitHub, LINE, WhatsApp, Threads
- **スマートクロップ** -- 中心重みのクロップアルゴリズム（アンカーポイント設定可能）
- **バッチエクスポート** -- `--platform all` で全サイズ一括生成
- **カスタムプリセット** -- `~/.socialcrop/presets.json` で独自サイズ追加
- **API ゼロ** -- クラウドサービス不要、アカウント不要、ネットワーク不要
- **フォーマット自動選択** -- プラットフォーム別に JPEG/PNG/WEBP を自動出力

## インストール

```bash
pip install socialcrop
```

## 使い方

```bash
# 単一プラットフォーム向けリサイズ
socialcrop resize photo.jpg --platform instagram-post

# 全プラットフォーム向け一括エクスポート
socialcrop batch photo.jpg --platform all --output ./resized/

# プリセット一覧表示
socialcrop platforms

# カスタムプリセット設定
socialcrop config
```

## コマンド

### `resize` -- 単一プラットフォーム

```bash
socialcrop resize <画像> --platform <名前> [--output <ディレクトリ>] [--anchor <位置>]
```

オプション:
- `--platform, -p` -- プラットフォームプリセット名（必須）
- `--output, -o` -- 出力ディレクトリ（デフォルト: 入力と同じ）
- `--anchor` -- クロップ基準点: `center`（デフォルト）, `top`, `bottom`, `left`, `right`

### `batch` -- 複数プラットフォーム一括出力

```bash
socialcrop batch <画像> --platform <名前> [--platform <名前> ...] [--output <ディレクトリ>]
```

`--platform all` で全対応プラットフォームを一括出力。

### `platforms` -- プリセット一覧

```bash
socialcrop platforms
```

### `config` -- カスタムプリセット管理

```bash
socialcrop config
```

カスタムプリセットは `~/.socialcrop/presets.json` に保存:

```json
{
  "my-blog-hero": {
    "name": "Blog Hero Image",
    "width": 1600,
    "height": 900,
    "format": "JPEG",
    "description": "Full-width blog hero"
  }
}
```

## 開発

```bash
# 開発依存込みでインストール
pip install -e ".[dev]"

# テスト実行
pytest tests/ -v --cov=socialcrop

# リント
ruff check src/ tests/
```

## ライセンス

MIT
