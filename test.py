from bs4 import BeautifulSoup

# サンプルHTML
html = """
<html>
<head><title>テストページ</title></head>
<body>
<h3>見出し1</h3>
<dl>
  <dt>項目1</dt>
  <dd>説明1</dd>
</dl>
<p>これは段落です。</p>
<h3>見出し2</h3>
<ul>
  <li>リスト項目1</li>
  <li>リスト項目2</li>
</ul>
<ul>
</ul>
<p>もう一つの段落です。</p>
<h3>見出し3</h3>
<p>これは別の段落です。</p>
<ul></ul>
</body>
</html>
"""

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(html, 'html.parser')

# 空のulタグをすべて探して削除
for ul in soup.find_all('ul'):
    if not ul.contents:  # タグが空かどうかを確認
        ul.decompose()  # 空のタグを削除

# 結果を表示
print(soup.prettify())