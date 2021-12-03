import pandas as pd

df = pd.read_csv('./crawling_data/reviews_2019_1.csv', index_col=0)
df.to_csv('./crawling_data/reviews_2019_1.csv', index=False)
df.info()

for i in range(1, 44):
    df_temp = pd.read_csv('./crawling_data/reviews_2019_{}.csv'.format(i))
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates() #중복값 제거
    df_temp.columns = ['title','reviews']
    df_temp.to_csv('./crawling_data/reviews_2019_{}.csv'.format(i), index=False)
    df = pd.concat([df, df_temp], ignore_index=True)

df.info()
df.to_csv('./crawling_data/reviews_2019.csv', index=False)