"""
1. Open a file with a list of website.
2. Make a request to each website in the file, print the status of all request, and log it to a new file.
3. Make a report to show a recap of request status that are over or equal 400.
"""
import requests
import time
from bs4 import BeautifulSoup


def main():
    # Open the file with the list of website
    with open('websites.txt', 'r') as f:
        websites = f.read().splitlines()

    # Make a request to each website in the file
    for website in websites:
        try:
            r = requests.get(website, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"})
            print(f'{website} - {r.status_code}')
            with open('log.txt', 'a') as f:
                f.write(f'{website} - {r.status_code}\n')
            if 'youtube.com' in website:
                soup = BeautifulSoup(r.content, "html.parser")
                errors_video = soup.findAll("noscript")
                for error_video in errors_video:
                    title = soup.find(class_="message").text
                    # print('title = ', title)

                    if 'error' in title:
                        print(f'{website} - {r.status_code} ERROR VIDEO NOT PLAYING!!!')
                        with open('log.txt', 'a') as f:
                            f.write(f'{website} - 9999 \n')

        except requests.exceptions.ConnectionError:
            print(f'{website} - Connection Error')
            with open('log.txt', 'w') as f:
                f.write(f'{website} - Connection Error\n')
        time.sleep(1)

    # Make a report to show a recap of request status that are over or equal 400
    with open('log.txt', 'r') as f:
        log = f.read().splitlines()
        over_400 = [line for line in log if int(line.split(' - ')[1]) >= 400]
        print('\n\n')
        print('Report:')
        print('-' * 50)
        print(f'{len(over_400)} websites returned over 400 status code.')
        print('-' * 50)
        print('\n\n')
        for over in over_400:
            print(over)


if __name__ == '__main__':
    main()