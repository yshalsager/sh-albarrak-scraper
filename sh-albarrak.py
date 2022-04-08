from pathlib import Path
from sys import argv

import httpx
from bs4 import BeautifulSoup


def get_html(url):
    return BeautifulSoup(httpx.get(url).text, "html.parser")


def get_links(url, selector):
    html = get_html(url)
    links = []
    for group in html.select(selector):
        links.append(group["href"])
    next_page = html.select_one("ul.pagination > li:last-of-type > a")
    return links, bool(next_page and next_page.get("href"))


def main(lecture_group_url):
    # curl -s https://sh-albarrak.com/section/lecture/groups/14862 | pup  '#tabContent a attr{href}'
    lecture_pages_links = []
    has_next = True
    page = 1
    while has_next:
        lecture_pages, has_next = get_links(
            f"{lecture_group_url}?sort=0&page={page}", "#tabContent a"
        )
        lecture_pages_links.extend(lecture_pages)
        page += 1
        print(lecture_pages)

    # curl -s https://sh-albarrak.com/section/lecture/groups/14863 | pup 'a.ellipsis-in-list attr{href}'
    lecture_download_pages = []
    for lecture_page in lecture_pages_links:
        has_next = True
        page = 1
        while has_next:
            lecture_download_page, has_next = get_links(
                f"{lecture_page}?sort=0&page={page}", "a.ellipsis-in-list"
            )
            if lecture_download_page:
                lecture_download_pages.extend(lecture_download_page)
                print(lecture_download_page)
            else:
                lecture_download_pages.append(lecture_page)
                print(lecture_page)
            page += 1
    lecture_download_pages.sort()

    # curl -s https://sh-albarrak.com/article/14866 | pup 'audio > source attr{src}'
    download_links = []
    for lecture_download_page in lecture_download_pages:
        audio_link = get_html(lecture_download_page).select_one("audio > source")["src"]
        download_links.append(audio_link)
        print(audio_link)

    downloads_list = [
        f"{link}, {link.split('/')[-2]}_{link.split('/')[-1]}"
        for link in sorted(list(set(download_links)))
    ]
    Path("links.txt").write_text("\n".join(downloads_list), encoding="utf-8")


if __name__ == "__main__":
    main(argv[1])
