import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure

st.set_page_config(layout="wide")

matplotlib.use("agg")
_lock = RendererAgg.lock
sns.set_style('darkgrid')
st.title('Downtown Condominium Market')

DATE_COLUMN = 'date/time'
DATA_PATH = ('data/data_clean5.csv')
@st.cache
def load_data():
    data = pd.read_csv(DATA_PATH)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
#data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

df=load_data()
has_records=any(df['neighbourhood'])
#remove duplicate entries
bool_series = df.duplicated(keep='first')
df=df[~bool_series]
st.write('Choose an Area of Toronto')
area_selector=st.multiselect('Multiselect', list(df.neighbourhood.unique()))
st.write('')
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (.1, 1, .1, 1, .1))

#Filtering data by User selection
#area_selector
filtered= df[df.neighbourhood == 'Downtown']

with row3_1, _lock:
    st.subheader('Listings in Downtown Neighbourhoods')
    if has_records:
        
        chart_data = filtered.groupby(['area'])['price'].agg([len]).rename(columns={'len':'listings'}).reset_index()
        fig = Figure()
        ax = fig.subplots()
        sns.barplot(x=chart_data['area'],
                    y=chart_data['listings'], color='goldenrod', ax=ax)
        ax.set_xlabel('Neighbourhoods')
        ax.set_ylabel('Number of Listings')
        st.pyplot(fig)
    else:
        st.markdown(
            "We do not have information to find out _when_ you read your books")

    #st.markdown("It looks like you've read a grand total of **{} books with {} authors,** with {} being your most read author! That's awesome. Here's what your reading habits look like since you've started using Goodreads.".format(
        #u_books, u_authors, df['book.authors.author.name'].mode()[0]))
        
#Filtering data by User selection
#filtered= df[df.neighbourhood == 'Downtown']
with row3_2, _lock:
    st.subheader("Mean Rent Price")
    
    chart_data = filtered.groupby(['area'])['price'].mean().reset_index()
    fig = Figure()
    ax=fig.subplots()
    sns.barplot(x=chart_data['area'],y=chart_data['price'], color='goldenrod', ax=ax)
    ax.set_xlabel('Neighbourhood')
    ax.set_ylabel('Mean Rent Price')
    st.pyplot(fig)
    
    #Add some commentary
    st.markdown("")
    
    
st.write('')
#row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    #(.1, 1, .1, 1, .1))
row4_1, row4_2, row4_3 = st.columns((.3,.3,.5))
#Filtering data by User selection
filtered= df[df.neighbourhood == 'Downtown']

def format_vals(x): return f'{x:,.0f}'
with row4_1, _lock:
    st.subheader("Downtown Neighbourhoods")
    
    chart_data = filtered.groupby(['area'])['price'].agg([len,np.mean,np.median]).reset_index()
    chart_data.rename(columns={'len':'listings','area':'Downtown Neighbourhoods'},inplace=True)
    chart_data['mean']=chart_data['mean'].map(format_vals)
    chart_data['median']=chart_data['median'].map(lambda x: f'{x:,.0f}')
    #fig = Figure()
    #ax = fig.subplots()
    st.table(chart_data)
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Your Book Ratings')
    #st.pyplot(fig)

    
with row4_2, _lock:
    st.subheader("Areas in Toronto")
    chart_data = df.groupby(['neighbourhood'],as_index=False)['price'].agg([len,np.mean,np.median]).reset_index()
    chart_data.rename(columns={'len':'listings','neighbourhood':'areas'},inplace=True)
    chart_data['mean']=chart_data['mean'].map(lambda x: f'{x:,.0f}')
    chart_data['median']=chart_data['median'].map(lambda x: f'{x:,.0f}')
    st.table(chart_data)
    
    #st.markdown("Here is the distribution of average rating by other Goodreads users for the books that you've read. Note that this is a distribution of averages, which explains the lack of extreme values!")

with row4_3, _lock:
    st.subheader("Areas in Toronto")
    chart_data = df.groupby(['neighbourhood'],as_index=False)['price'].agg([len,np.mean,np.median]).reset_index()
    chart_data.rename(columns={'len':'listings','neighbourhood':'areas'},inplace=True)
    fig = Figure()
    ax=fig.subplots()
    #sns.barplot(x=chart_data['areas'],y=chart_data['median'], color='goldenrod', ax=ax)
    sns.barplot(x=chart_data['median'],y=chart_data['areas'], color='goldenrod', ax=ax)
    ax.set_ylabel('Toronto Areas')
    ax.set_xlabel('Median Rent Price')
    ax.bar_label(ax.containers[0])
    
    st.pyplot(fig)

st.write('')
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (.1, 1, .1, 1, .1))
#Filtering data by User selection
filtered= df[df.neighbourhood == 'Downtown']

with row5_1, _lock:
    # page breakdown
    st.subheader('Book Length Distribution')
    


with row5_2, _lock:
    # length of time until completion
    st.subheader('How Quickly Do You Read?')
        