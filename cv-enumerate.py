# from bs4 import BeautifulSoup
import requests
from flask import *

scope_init = ["テレビアニメ", "劇場アニメ", "OVA", "Webアニメ", "ゲーム", "ラジオ"]

def CVEnumerate(actor_name, scope=scope_init, is_only_main_character=False):
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

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def CVEnumerate():
	scope_name_list =["TV_anime", "theater_anime", "OVA", "game", "radio"]
	res = """
	声優の名前をフルネームで入力してください
	<form action="/" method="POST">
	<input type="text" name="actor_name">
	<input type="submit" value="送信">
	<br>
	<input type="checkbox" name="TV_anime" checked> テレビアニメ
	<input type="checkbox" name="theater_anime" checked> 劇場アニメ
	<input type="checkbox" name="OVA" checked> OVA
	<input type="checkbox" name="web_anime" checked> ウェブアニメ
	<input type="checkbox" name="game" checked> ゲーム
	<input type="checkbox" name="radio" checked> ラジオ
	<br>
	<input type="checkbox" name="main_char"> メインキャラクターのみを選択しますか？
	</form>
	<br>
	""" 
	if request.method == "POST":
		res += f"{request.form['actor_name']}の検索結果：\n<br>"
		print(request.form["TV_anime"])

	return res
		
if __name__ == "__main__":
	app.run()
