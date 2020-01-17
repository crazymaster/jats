# jats [![Build Status](https://travis-ci.org/crazymaster/jats.svg?branch=master)](https://travis-ci.org/crazymaster/jats)

Build Parallel Corpus for Japanese Text Simplification

## Requirements

* [MeCab](http://taku910.github.io/mecab/)

### Ubuntu

```bash
sudo apt install mecab libmecab-dev unidic-mecab swig nkf
```

### macOS

```bash
brew install mecab mecab-unidic swig nkf
```

### Setup

```bash
make setup
```

## Usage

```bash
echo 'お腹が空いた。' | python3 -m jatr
```

```bash
python3 -m jatr < data/サンプルテキスト/中級前半.txt
```

```bash
python3 -m jatr data/サンプルテキスト/上級後半.txt
```

```bash
make help
```

## Note

語彙表やコーパスは `data` ディレクトリ以下に配置
