import pandas as pd

file_path = "/home/shiva/GIT_C/Clinical_Chat_RAG/data/NOTEEVENTS.csv"


data = pd.read_csv(file_path)

df = pd.DataFrame(data)

df_100 = df.head(100)

df_100.to_csv("NOTEEVENTS_s.csv", index=False)
