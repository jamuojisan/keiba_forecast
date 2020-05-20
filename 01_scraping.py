import sys
import requests
import lxml.html
from bs4 import BeautifulSoup
import re
import csv

def main(argv):
    url = "https://race.netkeiba.com/race/result.html?race_id=202008030301&rf=race_list" #コマンドライン引数からURLを取得
    race_html=requests.get(url)
    race_html.encoding = race_html.apparent_encoding  
    race_soup=BeautifulSoup(race_html.text,'html.parser')

    # レース表だけを取得して保存
    HorseList = race_soup.find_all("tr",class_="HorseList")

    # レース表の整形
    # レース表を入れるリストを作成
    Race_lists = []
    # 表の横列の数=15("着順,枠,馬番,馬名,性齢,斤量,騎手,タイム,着差,人気,単勝オッズ,後3F,コーナー通過順,厩舎,馬体重(増減))
    Race_row = 15

    # 出馬数をカウント
    uma_num = len(HorseList)

    #　無駄な文字列を取り除いてリストへ格納
    for i in range(uma_num):
        Race_lists.insert(1+i, HorseList[i])

        Race_lists[i] = re.sub(r"\n","",str(Race_lists[i]))
        Race_lists[i] = re.sub(r" ","",str(Race_lists[i]))
        Race_lists[i] = re.sub(r"</td>",",",str(Race_lists[i]))
        Race_lists[i] = re.sub(r"<[^>]*?>","",str(Race_lists[i]))
        Race_lists[i] = re.sub(r"\[","",str(Race_lists[i]))
        Race_lists[i] = re.sub(r"\]","",str(Race_lists[i]))
        print(Race_lists[i])
def fetch(url :str): 
    r = requests.get(url) #urlのWebページを保存する
    r.encoding = r.apparent_encoding #文字化けを防ぐためにencodingの値をappearent_encodingで判定した値に変更する
    return r.text #取得データを文字列で返す

def scrape(html: str):
    html = lxml.html.fromstring(html) #fetch()での取得結果をパース
    print(html.cssselect('#race_main > div > table > tr'))
    result = [] #スクレイピング結果を格納
    for h in html.cssselect('#race_main > div > table > tr'):#スクレイピング箇所をCSSセレクタで指定
        print(h)
        exit()
        column = ((",".join(h.text_content().split("\n"))).lstrip(",").rstrip(",")).split(",")
        #text_content()はcssselectでマッチした部分のテキストを改行文字で連結して返すので、
        #splitを使って改行文字で分割して、その結果をカンマ区切りでjoinする。
        #前と後ろに余計な空白とカンマが入っている(tdじゃなくてtrまでのセレクタをしていした分の空文字が入っちゃってる?ようわからん)ので、
        #splitで空白を、lstrip,rstripでカンマを削除してさらにそれをカンマで区切ってリストにしている
        column.pop(4) if column[4] == "" else None  #1行目以外、馬名と性齢の間に空文字が入っちゃってるので取り出す
        result.append(column) #リストに行のデータ(リストを追加)

    return result #結果を返す

def save(file_path, result):
     with open(file_path, 'w', newline='') as f: #ファイルに書き込む
         writer = csv.writer(f) #ファイルオブジェクトを引数に指定する
         writer.writerow(result.pop(0)) #一行目のフィールド名を書き込む
         writer.writerows(result) #残りの行を書き込む

if __name__ == '__main__':
    main(sys.argv) 