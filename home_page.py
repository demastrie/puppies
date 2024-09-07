import streamlit as st
import pandas as pd


st.title('Puppy Weight Tracker')
df_puppy_weights = pd.read_csv('puppy-weights.csv')
df_puppy_weights = df_puppy_weights.dropna()
df_puppy_weights['date'] = pd.to_datetime(df_puppy_weights['date'])
df_puppy_weights['weight-oz'] = df_puppy_weights['weight-gm'] * 0.03527396

# Add a pounds and ounces column


def format_weight(row):
    '''format_weight(row) returns the weight in pounds and ounces'''
    pounds_str = f"{row['pounds']} lb " if row['pounds'] > 0 else ""
    ounces_str = f"{row['ounces']} oz" if row['ounces'] > 0 else ""
    return pounds_str + ounces_str


df_puppy_weights['pounds_float'] = df_puppy_weights['weight-oz'] / 16
df_puppy_weights['pounds'] = df_puppy_weights['pounds_float'].astype(int)
df_puppy_weights['ounces'] = ((df_puppy_weights['pounds_float']
                               - df_puppy_weights['pounds']) * 16) \
                                .round().astype(int)
df_puppy_weights['weight-lboz'] = df_puppy_weights.apply(format_weight, axis=1)
df_puppy_weights.drop(['pounds_float', 'pounds', 'ounces'],
                      axis=1, inplace=True)

# shape data and show a line chart
df_puppy_weights_pivoted = df_puppy_weights.pivot(index='date',
                                                  columns='name')['weight-gm']

earliest_date = df_puppy_weights['date'].min()
df_puppy_weights['days-old'] = df_puppy_weights['date'] - earliest_date
df_puppy_weights['days-old'] = df_puppy_weights['days-old'].dt.days.astype(int)

df_puppy_weights_pivoted.columns.name = None

st.line_chart(df_puppy_weights_pivoted, y=df_puppy_weights_pivoted.columns,
              x_label="2024", y_label="Weight in grams")
st.dataframe(df_puppy_weights_pivoted)

# show the larger dataframe
if st.checkbox('Show all puppy weight data'):
    st.dataframe(df_puppy_weights)
