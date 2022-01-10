from numpy.core.fromnumeric import squeeze
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")

matplotlib.use("agg")
_lock = RendererAgg.lock
sns.set_style('darkgrid')
st.title('Downtown Condominium Market')

DATE_COLUMN = 'date/time'
DATA_PATH = ('data/data_clean_full0106.csv')
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
area_selector=st.selectbox('Select', list(df.neighbourhood.unique()))
st.write('')
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (.1, 1, .1, 1, .1))

#Filtering data by User selection
#area_selector


with row3_1, _lock:
    st.subheader('Listings in Downtown Neighbourhoods')
    if has_records:
        filtered= df[df.neighbourhood == area_selector]
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
        

#filtered= df[df.neighbourhood == 'Downtown']
with row3_2, _lock:
    st.subheader("Mean Rent Price")
    #Filtering data by User selection
    filtered= df[df.neighbourhood == area_selector]
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

#Might want to use st.cache for this data

# Drill down section for a specific area 
area_select_d=st.selectbox('Select an Area in toronto', list(df.neighbourhood.unique()))

# Filter neighbourhoods to only show ones from the selected area
filtered = df[df.neighbourhood == area_select_d]

#Select a specific area (drilling down)
neigh_select_d=st.selectbox('Select a neighbourhood', list(filtered.area.unique()))

#Filtering data again based on selection
filtered= filtered[filtered.area == neigh_select_d]


#creating figure plots 


    # Rent Price Histogram for one specific neighbourhood
    #st.subheader(f'Price Distribution for {area_name}')
    #fig = Figure()
    #ax = fig.subplots()
    #sns.histplot(filtered['price'],ax=ax,binwidth=65)
    #ax.set_xlabel('Price')
    #ax.set_ylabel('Count')
    #ax.bar_label(ax.containers[0])
    #st.pyplot(fig) """
    
    # Create Dynamic Title based on Selection (similar to what condos.ca has)
    #{building_name} in {area_name},{neighbourhood_name}, {city_name} e.g. 'Waterclub III in The Waterfront, Downtown, Toronto
    #building_name=filtered['building'].mode()[0]
area_name=filtered['area'].mode()[0]
neighbourhood_name=filtered['neighbourhood'].mode()[0]
city_name=filtered['city'].mode()[0]
    
st.markdown('')
st.header(f'{area_name}, {neighbourhood_name}, {city_name}')
st.markdown("<hr/>", unsafe_allow_html=True)    
#Change KPIs to their own row

with st.container():
    col1, col2,col3 = st.columns(3)
    
    with col1:
        st.subheader('Average Rent Price')
        mean_rent = int(np.mean(filtered['price']))
        st.markdown(f"<h1 style='text-align: center; color: white;'>${mean_rent:,}</h1>", unsafe_allow_html=True)
    
    with col2:
        st.subheader('Number of Listings')
        num_listings = len(filtered)
        st.markdown(f"<h1 style='text-align: center; color: white;'>{num_listings:,}</h1>", unsafe_allow_html=True)
    
    with col3:
        st.subheader('Mean Rent Price')
        mean_rent = int(np.mean(filtered['price']))
        st.markdown(f"<h1 style='text-align: center; color: white;'>${mean_rent:,}</h1>", unsafe_allow_html=True)
        
        
with st.container():
    col1, col2, col3 = st.columns([10, 10,12])
    
    with col1:
        st.subheader('Bedroom Distribution')
        #Distribution for the number of bedrooms 
        g=sns.catplot(x='bedrooms',kind='count', data=filtered).set_xlabels('Bedrooms').set_ylabels('Count')
        st.pyplot(g)
        
        
        
    with col2:
        st.subheader('Size Distribution')
        fig = Figure()
        ax = fig.subplots()
        sns.histplot(pd.to_numeric(filtered['size'],errors='coerce').dropna(), ax=ax)
        ax.set_xlabel('Size (Sqft.)')
        ax.set_ylabel('Count')
        st.pyplot(fig)
        
        
    with col3:
        st.subheader(f'Price Distribution')
        #st.write('')
        fig = Figure()
        ax = fig.subplots()
        sns.histplot(filtered['price'],ax=ax,binwidth=65)
        ax.set_xlabel('Price')
        ax.set_ylabel('Count')
        #ax.bar_label(ax.containers[0])
        st.pyplot(fig)
        