from bs4 import BeautifulSoup
import requests

def output_clear(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('')

def output_write(filename, text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

scope_init = ["テレビアニメ", "劇場アニメ", "OVA", "Webアニメ", "ゲーム", "ラジオ"]

def main(actor_name, output_filename='', scope=scope_init, is_only_main_character=False):
    string_url_encode = requests.utils.quote(actor_name)
    url = f'https://ja.wikipedia.org/wiki/{string_url_encode}'
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
            if next_sibling and next_sibling.name == 'dt':
                dt_tag.decompose()

    # h3タグを取得
    h3_tags = soup.select('h3')
    index = []
    for h3_tag in h3_tags:
        # 関係のない項目はスキップ
        if h3_tag.getText() not in scope:
            continue
        index.append(h3_tag)

        # 次のh3までを見ていく
        now = h3_tag.find_next_sibling()

        # now が最後になるか，次にh3が来るまでを探索
        while now and now.name != 'h3':
            # この3つ以外は要らないと感じたので消す
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
    s = main('田村ゆかり', is_only_main_character=True)
    out = "output.html"
    output_clear(out)
    output_write(out, s)
