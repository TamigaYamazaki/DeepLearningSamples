import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import DataCollection as dc

def collect_YouTube_Data(URL, months):
    id_type = dc.GetChannelID_from_URL(URL).GetURLtype()
    video_datas = dc.VideoList_csv(id_type).get_video_list(month=months)
    df = df = pd.DataFrame(video_datas, columns=["video_id", "view_count", "like_count", "comment_count", "tags"])
    df.to_csv("Datas/data_test.csv", sep=",")

#collect_YouTube_Data("https://www.youtube.com/@HikakinTV", 72)