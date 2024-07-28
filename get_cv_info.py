from bs4 import BeautifulSoup
import requests

def output_clear(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('')

def output_write(filename, text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

scope_init = ["テレビアニメ", "劇場アニメ", "OVA", "Webアニメ", "ゲーム", "ラジオ"]

def get_cv_info(actor_name, output_filename='', scope=scope_init, is_only_main_character=False):
    string_url_encode = requests.utils.quote(actor_name)
    url = f'https://ja.wikipedia.org/wiki/{string_url_encode}'
    # url = "https://ja.wikipedia.org/wiki/%E9%BB%92%E6%B2%A2%E3%81%A8%E3%82%82%E3%82%88"
    # print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # reference系を削除
    tag = soup.find_all('sup', class_='reference')
    for i in tag:
        i.decompose()
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        del a_tag['href']
    edit_span_tags = soup.find_all('span')
    for span_tag in edit_span_tags:
        if span_tag.getText() == '[編集]':
            span_tag.decompose()

    # 主要キャラクターのみを取得
    if is_only_main_character:
        li_tags = soup.select('li')
        for li_tag in li_tags:
            if not li_tag.find("b"):
                li_tag.decompose()

        # 空っぽになったタグの消去
        # 空っぽのddタグを削除
        dd_tags = soup.select('dd')
        for dd_tag in dd_tags:
            if not dd_tag.getText(strip=True):
                dd_tag.decompose()

        dt_tags = soup.select('dt')
        for dt_tag in dt_tags:
            next_sibling = dt_tag.find_next_sibling()
            if not next_sibling:
                dt_tag.decompose()
            if next_sibling and next_sibling.name == 'dt':
                dt_tag.decompose()

    # divタグを取得
    div_tags = soup.find_all('div', class_='mw-heading mw-heading3')
    index = []
    for div_tag in div_tags:
        if div_tag.getText(strip=True) not in scope:
            div_tag.decompose()
            continue
        index.append(div_tag)
        now = div_tag.find_next_sibling()
        while now and now.name != 'div':
            if now.name in ['ul', 'dl', 'h4']:
                index.append(now)
            now = now.find_next_sibling()

    res = ""
    for i in index:
        res += i.prettify()

    if output_filename:
        output_clear(output_filename)
        output_write(output_filename, res)
    return res

if __name__ == '__main__':
    s = get_cv_info('田村ゆかり')
    out = "output.html"
    output_clear(out)
    output_write(out, s)
