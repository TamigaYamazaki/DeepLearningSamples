import pandas as pd
import datetime
from googleapiclient.discovery import build
from urllib.parse import urlparse
from dateutil.relativedelta import relativedelta

import private


"""IDのクラス(構造体)"""
class ID_type:
    def __init__(self, type, id="", url="", name="") -> None:
        self.type = type
        self.url = url
        self.name = name

        if self.type == "channel":
            self.id = id
            print(self.id)
        elif self.type == "old":
            self.id = private.youtube.channels().list(part="id", forUsername=self.name).execute()["items"][0]["id"]
            print(self.id)
        elif self.type == "custom":
            self.id = private.youtube.search().list(part="snippet", type="channel", q=self.name).execute()["items"][0]["id"]["channelId"]
            print(self.id)
        elif self.type == "handle":
            self.id = private.youtube.search().list(part="id", type="channel", q=self.name).execute()["items"][0]["id"]["channelId"]
            print(self.id)


"""受け取ったURLを分解しチャンネルIDを取得するクラス"""
class GetChannelID_from_URL:
    def __init__(self, allurl) -> None:
        self.url = allurl

    def GetURLtype(self):
        self.parse_url = urlparse(self.url)
        self.url_path = self.parse_url.path
        self.type_index = []
        self.type_text = ""
        self.text = []
        self.url_text = self.url_path
        
        for i in self.url_path:
            self.text.append(i)
            if i == "/":
                self.type_index.append(self.text)
                self.text = []

        self.type_index.append(self.text)
        
        print(self.type_index[1][0], len(self.type_index))
        
        if len(self.type_index) == 3:
            if "".join(self.type_index[1]) == "channel/":
                return ID_type("channel", id="".join(self.type_index[2]), url=self.url)
            elif "".join(self.type_index[1]) == "user/" :
                print(self.type_index[1])
                return ID_type("old", url=self.url, name="".join(self.type_index[2]))
            elif "".join(self.type_index[1]) == "c/":
                print(self.type_index[1])
                return ID_type("custom", url=self.url, name="".join(self.type_index[2]))
            
        elif len(self.type_index) == 2:
            return ID_type("handle", url=self.url, name="".join(self.type_index[1]))


"""チャンネル動画一覧をcsv出力するクラス"""
class VideoList_csv:
    def __init__(self, id: ID_type) -> None:
        self.id = id
        self.dic_list = []
        self.output = None
        self.response = None
        #self.columns = ["video_id", "view_count", "like_count"]
        self.lists = []

    def get_datas(self, id):
        snippet = private.youtube.videos().list(part="snippet", id=id).execute()["items"][0]#["statistics"]
        statistic = private.youtube.videos().list(part="statistics", id=id).execute()["items"][0]["statistics"]
        li = [snippet, statistic]
        return li

    def video_search(self, pagetoken, st, ed):
        self.response = private.youtube.search().list(part="snippet", channelId=self.id.id, type="video", maxResults=50, 
            publishedAfter=st, publishedBefore=ed, pageToken=pagetoken).execute()
        self.dic_list += self.response["items"]
        try:
            nextPagetoken = self.response["nextPageToken"]
            self.video_search(nextPagetoken, st, ed)
        except:
            return

    def get_video_list(self, month=1, when=datetime.datetime(datetime.datetime.now().year, 1, 1, 0, 0)):
        num = month + 1
        dt = when - relativedelta(months=month)
        self.dic_list = []
        
        for i in range(1, num):
            self.video_search("", dt.isoformat()+"Z", (dt + relativedelta(months=1)).isoformat()+'Z')
            dt += relativedelta(months=1)
        
        """動画ID取得"""
        video_ids = []
        #items = self.search_response["items"]
        items = self.dic_list
        for item in items:
            video_ids.append(item["id"]["videoId"])

        """再生回数、高評価数取得"""
        video_datas_statistics = []
        video_datas_snippet = []
        for item in video_ids:
            datas = self.get_datas(item)
            video_datas_statistics.append(datas[1])
            video_datas_snippet.append(datas[0]["snippet"].get("tags"))
        #print(video_datas[0]["likeCount"])

        """DataFrame作成"""
        for i in range(0, len(video_datas_statistics)):
            list = [video_ids[i], video_datas_statistics[i]["viewCount"], video_datas_statistics[i]["likeCount"], 
                    video_datas_statistics[i]["commentCount"], list(video_datas_snippet[i])]
            self.lists.append(list)
        print(self.lists)
        
        return self.lists

def omit_string(sentence, sprit_word) -> str:
    if len(sprit_word) > 1:
        raise ValueError("引数 sprit_word は1文字だけ入力して下さい")
    else:
        omit_index = len(sentence)

        for i in range(0, len(sentence)):
            if sentence[i] == sprit_word:
                omit_index = i
                break
        return "".join(sentence[0:omit_index])

#https://www.youtube.com/user/HikakinTV
#https://www.youtube.com/@ooo0eve0ooo
#collect_YouTube_Data("https://www.youtube.com/@ooo0eve0ooo", 60, "Data2")

#data = VideoList_csv(None).get_datas("TvRVcN-fJLE")[0]["snippet"]["tags"]
#print(data)

def collect_YouTube_Data(URL, months):
    id_type = GetChannelID_from_URL(URL).GetURLtype()
    video_datas = VideoList_csv(id_type).get_video_list(month=months)
    df = df = pd.DataFrame(video_datas, columns=["video_id", "view_count", "like_count", "comment_count", "tags"])
    df.to_csv("Datas/Data_Pocky.csv", sep=",")