import requests
import re
from bs4 import BeautifulSoup


def get_page(url):
    headers = {'User-Agent': 'mozilla/5.0 (Linux; Android 6.0.1; '
                            'Nexus 5x build/mtc19t applewebkit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2702.81 Mobile Safari/537.36'}
    resp = requests.get(url, headers=headers)
    content = resp.content.decode('utf-8')
    
    return resp.status_code, BeautifulSoup(content, 'html.parser')

def processLayer1(tag1, tag2, url):
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll(tag1, class_=tag2)
    for elem in elems:
        item_url = [result['href'] for result in elem.findAll('a', href=True)]
        item_url = ''.join(str(e) for e in item_url)
        # print(item_url)
        processGeneric(item_url)

# process https://dailycoursereviews.com
def processDCR(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll('div', class_='news-ticker-title')
    for elem in elems:
        url = [result['href'] for result in elem.findAll('a', href=True)]
        url = ''.join(str(e) for e in url)
        url = 'http' + url.split('https')[-1]
        if ( "https://" not in url or len(url) < 5 or len(url) > 200):
            continue
        else:
            _, detail_soup = get_page(url)
            detail_elems = detail_soup.findAll('div', class_="mt-container")
            for detail_elem in detail_elems:
                urls = [result['href'] for result in detail_elem.findAll('a', href=True)]
                for item_url in urls:
                    if "couponCode" in item_url:
                        if item_url not in pool:
                            collision -=1
                            pool.add(item_url)
                            print(item_url)
                            f = open("udemy_free.txt", "a")
                            f.write(item_url + "\n")
                            f.close()
                        elif collision > 5:
                            return None
                        else:
                            collision +=1


# process https://freecoupondiscount.com
def processFCD(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll('div', class_='content_constructor')
    for elem in elems:
        url = [result['href'] for result in elem.findAll('a', href=True)]
        url = ''.join(str(e) for e in url)
        if (len(url) < 5 or len(url) > 200):
            continue
        else:
            _, detail_soup = get_page(url)
            detail_elems = detail_soup.findAll('div', class_="row row--component-margin")
            for detail_elem in detail_elems:
                url = [result['href'] for result in detail_elem.findAll('a', href=True)]
                item_url = url = ''.join(str(e) for e in url)             
                if "couponCode" in item_url:
                    try:
                        item_url = item_url.split('&murl=')[1]
                    except IndexError:
                        item_url = url
                    item_url = item_url.replace('%3A', ':')
                    item_url = item_url.replace('%2F', '/')
                    item_url = item_url.replace('%3F', '?')
                    item_url = item_url.replace('%3D', '=')   
                    if item_url not in pool:
                        collision -=1
                        pool.add(item_url)
                        print(item_url)
                        f = open("udemy_free.txt", "a")
                        f.write(item_url + "\n")
                        f.close()
                    elif collision > 5:
                        return None
                    else:
                        collision +=1


# process https://onlinecoursesworld.com
def processOCW(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll('div', class_='readMore')
    for elem in elems:
        url = [result['href'] for result in elem.findAll('a', href=True)]
        url = ''.join(str(e) for e in url)
        if (len(url) < 5 or len(url) > 200):
            continue
        else:
            _, detail_soup = get_page(url)
            detail_elems = detail_soup.findAll('div', class_="button-linkwa")
            for detail_elem in detail_elems:
                url = [result['href'] for result in detail_elem.findAll('a', href=True)]
                item_url = url = ''.join(str(e) for e in url)
                if "couponCode" in item_url:
                    try:
                        item_url = item_url.split('&murl=')[1]
                    except IndexError:
                        item_url = url
                    item_url = item_url.replace('%3A', ':')
                    item_url = item_url.replace('%2F', '/')
                    item_url = item_url.replace('%3F', '?')
                    item_url = item_url.replace('%3D', '=')  
                    if item_url not in pool:
                        collision -=1
                        pool.add(item_url)
                        print(item_url)
                        f = open("udemy_free.txt", "a")
                        f.write(item_url + "\n")
                        f.close()
                    elif collision > 5:
                        return None
                    else:
                        collision +=1


# process https://wwfw.udemycouponpro.com
def processUCP(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll('div', class_ = 'td-module-thumb')
    for elem in elems:
        url = [result['href'] for result in elem.findAll('a', href=True)]
        url = ''.join(str(e) for e in url)
        if (len(url) < 5 or len(url) > 200):
            continue
        else:
            details = requests.get(url)
            detail_soup = BeautifulSoup(details.text, 'html.parser')
            detail_elems = detail_soup.findAll('div', class_ = 'clp-component-render')
            for detail_elem in detail_elems:
                url = [result['href'] for result in detail_elem.findAll('a', href=True)]
                url = ''.join(str(e) for e in url)
                item_url = "https://www.udemy.com/" + url.split('/https://www.udemy.com/')[1]
                if "couponCode" in item_url:
                    if item_url not in pool:
                        collision -=1
                        pool.add(item_url)
                        print(item_url)
                        f = open("udemy_free.txt", "a")
                        f.write(item_url + "\n")
                        f.close()
                    elif collision > 5:
                        return None
                    else:
                        collision +=1


# process https://udemycoupon.learnviral.com
# directly parsing page to extract all href and check if having couponCode or not
def processGeneric(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    results = soup.findAll('a', href=True)
    for result in results:
        item_url = result['href']
        if "couponCode" in item_url:
            if "&murl=" in item_url:
                item_url = item_url.split('&murl=')[1]
                item_url = item_url.replace('%3A', ':')
                item_url = item_url.replace('%2F', '/')
                item_url = item_url.replace('%3F', '?')
                item_url = item_url.replace('%3D', '=')                
            if item_url not in pool:
                collision -=1
                pool.add(item_url)
                print(item_url)
                f = open("udemy_free.txt", "a")
                f.write(item_url + "\n")
                f.close()
            elif collision > 5:
                return None
            else:
                collision +=1


# process https://www.discudemy.com
def processDU(url):
    collision = 0
    status_code, soup = get_page(url)

    if status_code != 200:
        print('Invalid url:', url)
        return None

    elems = soup.findAll('section', class_ = 'card')
    for elem in elems:
        url = [result['href'] for result in elem.findAll('a', {'class':'card-header'})]
        url = ''.join(str(e) for e in url)
        url = url.replace('/english/', '/go/')
        if (len(url) < 5 or len(url) > 200):
            continue
        else:
            details = requests.get(url).text
            item_url = "https://www.udemy.com/" + details.split('<a  href="https://www.udemy.com/')[1].split('" target="_blank">')[0]
            if "couponCode" in item_url:
                item_url = item_url.replace('&site_ref=discudemy.com', '')
                if item_url not in pool:
                    collision -=1
                    pool.add(item_url)
                    print(item_url)
                    f = open("udemy_free.txt", "a")
                    f.write(item_url + "\n")
                    f.close()
                elif collision > 5:
                    return None
                else:
                    collision +=1


if __name__ == "__main__":
    global pool 
    pool = set()
    with open("udemy_free.txt") as file:
        lines = file.read().splitlines()

    file.close()    
    pool = set(sorted(lines))

    print(len(pool))

    processGeneric("https://www.guru99.com/free-udemy-course.html")
    processGeneric("https://udemycoupon.learnviral.com")  
    processGeneric("https://www.promocoupons24.com") 
    processGeneric("http://www.free-courses.co.in")
    processGeneric("https://offersallin1.com/coupons-category/udemy-courses")
    processUCP("https://www.udemycouponpro.com")
    processDU("https://www.discudemy.com/language/english/1")
    processOCW("https://onlinecoursesworld.com")
    processFCD("https://freecoupondiscount.com")
    processDCR("https://dailycoursereviews.com")
    processLayer1('div', 'content_constructor', "https://freecoupondiscount.com")

    print(len(pool))
