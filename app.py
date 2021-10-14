import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

threated_urls = set()
resulting_urls = set()


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    found_urls = set()

    # Find embed video links
    for iframe_tag in soup.findAll("iframe"):
        src_tag = iframe_tag.attrs.get("src")
        # if src_tag == "" or src_tag is None:
        #     # href empty tag
        #     pass
        # else:
        found_urls.add(src_tag)

    # find A tag href
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        # if href == "" or href is None:
        #     # href empty tag
        #     pass
        # else: 
        found_urls.add(href)

    for found_url in found_urls:
        href = found_url
        if href == "" or href is None:
            # tag is empty
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if 'mailto' in href:
            # this is an email link
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"[!] External link: {href}")
                external_urls.add(href)
                resulting_urls.add(href)
            continue

        print(f"[*] Internal link: {href}")

        urls.add(href)
        internal_urls.add(href)

    return urls


# number of urls visited so far will be stored here
total_urls_visited = 0



class file_writer():
    def __init__(self, filename):
        self.filename = filename

    def write_lines(self, lines):

        with open(self.filename, 'w') as the_file:
            for element in lines:
                the_file.write(f"{element}\n")


def crawl(url, max_urls=30, existing_urls=None):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """

    global total_urls_visited
    global resulting_urls
    total_urls_visited += 1
    print(f"[*] Crawling: {url}")
    if url not in threated_urls:
        links = get_all_website_links(url)
        resulting_urls = resulting_urls.union(links)
    threated_urls.add(url)

    for link in links:
        if total_urls_visited > max_urls:
            break
        if link not in threated_urls:
            outputs = crawl(link, max_urls=max_urls)
            resulting_urls = resulting_urls.union(outputs)
    
    return resulting_urls


if __name__ == "__main__":
    results = set()
    with open('source_address.txt', 'r') as f:
        addresses = f.read().splitlines()

    for address in addresses:

        results = results.union(crawl(address, 100))
    print(results)
    file1 = file_writer('./websites.txt')
    file1.write_lines(results)
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", total_urls_visited)