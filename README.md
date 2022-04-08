# sh-albarrak scraper

A simple Python 3 simple web scraper to grab mp3 files form https://sh-albarrak.com

## Installation

```bash
# Using poetry
poetry install

# or using pip 18+
pip install .
```

## Usage

```bash
python3 archiver.py url
# python3 sh-albarrak.py "https://sh-albarrak.com/section/lecture/groups/14862"
```

Then, you can download files using any external downloader.

```bash
cat links.txt | while IFS=, read -r url name; do axel -k -n16 $url -o $name; done
cat links.txt | while IFS=, read -r url name; do wget $url -o $name; done 
```



