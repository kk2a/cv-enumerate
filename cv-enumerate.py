from bs4 import BeautifulSoup
import requests
from flask import *
from main import get_cv_info

app = Flask(__name__)

all_type_dict = {"TV_anime": "テレビアニメ", "theater_anime": "劇場アニメ", "OVA": "OVA", "web_anime": "ウェブアニメ", "game": "ゲーム", "radio": "ラジオ"}

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
		res += f"{request.form['actor_name']}の検索結果：<br>"
		sellect = []
		for label in all_type_dict.keys():
			if request.form.get(label):
				sellect.append(all_type_dict[label])
		res += get_cv_info(request.form["actor_name"], scope=sellect, is_only_main_character=request.form.get("main_char"))
	return res

if __name__ == "__main__":
	app.run()
