import streamlit as st
import pandas as pd
from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import load_diabetes, fetch_california_housing
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

# Override OneHotEncoder class to remove 'sparse' argument
class MyOneHotEncoder(OneHotEncoder):
    def __init__(self, handle_unknown='error', categories='auto', drop=None):
        super().__init__(handle_unknown=handle_unknown, categories=categories, drop=drop)

# Replace OneHotEncoder with MyOneHotEncoder
def build_model(df):
    df = df.loc[:100] # FOR TESTING PURPOSE, COMMENT THIS OUT FOR PRODUCTION
    
    # Select the target variable (Y)
    target_variable = st.selectbox('Select the target variable:', df.columns)
    Y = df[target_variable]
    X = df.drop(columns=[target_variable])

    # Encode categorical features
    categorical_features = []  # Replace with your categorical feature names
    for feature in categorical_features:
        le = LabelEncoder()
        X[feature] = le.fit_transform(X[feature])

    st.markdown('**1.2. Dataset dimension**')
    st.write('X')
    st.info(X.shape)
    st.write('Y')
    st.info(Y.shape)

    st.markdown('**1.3. Variable details**:')
    st.write('X variable (first 20 are shown)')
    st.info(list(X.columns[:20]))
    st.write('Y variable')
    st.info(Y.name)

    # Build lazy model
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=split_size, random_state=seed_number)
    reg = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None)
    models_train, predictions_train = reg.fit(X_train, X_train, Y_train, Y_train)
    models_test, predictions_test = reg.fit(X_train, X_test, Y_train, Y_test)

    st.subheader('2. Table of Model Performance')

    st.write('Training set')
    st.write(predictions_train)
    st.markdown(filedownload(predictions_train, 'training.csv'), unsafe_allow_html=True)

    st.write('Test set')
    st.write(predictions_test)
    st.markdown(filedownload(predictions_test, 'test.csv'), unsafe_allow_html=True)

    st.subheader('3. Plot of Model Performance (Test set)')

    with st.expander("R-squared"):
        # Tall
        predictions_test["R-Squared"] = [0 if i < 0 else i for i in predictions_test["R-Squared"]]
        fig, ax = plt.subplots(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(y=predictions_test.index, x="R-Squared", data=predictions_test)
        ax.set(xlim=(0, 1))
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-r2-tall.pdf'), unsafe_allow_html=True)
        
        # Wide
        fig, ax = plt.subplots(figsize=(9, 3))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x=predictions_test.index, y="R-Squared", data=predictions_test)
        ax.set(ylim=(0, 1))
        plt.xticks(rotation=90)
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-r2-wide.pdf'), unsafe_allow_html=True)

    with st.expander("RMSE (capped at 50)"):
        # Tall
        predictions_test["RMSE"] = [50 if i > 50 else i for i in predictions_test["RMSE"]]
        fig, ax = plt.subplots(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(y=predictions_test.index, x="RMSE", data=predictions_test)
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-rmse-tall.pdf'), unsafe_allow_html=True)
        
        # Wide
        fig, ax = plt.subplots(figsize=(9, 3))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x=predictions_test.index, y="RMSE", data=predictions_test)
        plt.xticks(rotation=90)
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-rmse-wide.pdf'), unsafe_allow_html=True)

    with st.expander("Calculation time"):
        # Tall
        predictions_test["Time Taken"] = [0 if i < 0 else i for i in predictions_test["Time Taken"]]
        fig, ax = plt.subplots(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(y=predictions_test.index, x="Time Taken", data=predictions_test)
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-calculation-time-tall.pdf'), unsafe_allow_html=True)
        
        # Wide
        fig, ax = plt.subplots(figsize=(9, 3))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x=predictions_test.index, y="Time Taken", data=predictions_test)
        plt.xticks(rotation=90)
        st.pyplot(fig)
        st.markdown(imagedownload(fig, 'plot-calculation-time-wide.pdf'), unsafe_allow_html=True)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

def imagedownload(fig, filename):
    s = io.BytesIO()
    fig.savefig(s, format='pdf', bbox_inches='tight')
    plt.close(fig)
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

#---------------------------------#
st.write("""
# The Algorithm Atlas Comparison App

In this implementation, the **lazypredict** library is used for building several machine learning models at once.

Developed by: Me(Abhishek Singh)

""")

#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)
    seed_number = st.sidebar.slider('Set the random seed number', 1, 100, 42, 1)

#---------------------------------#
# Main panel

# Displays the dataset
st.subheader('1. Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df)
    build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Diabetes dataset
        diabetes = load_diabetes()
        X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        Y = pd.Series(diabetes.target, name='response')
        df = pd.concat([X, Y], axis=1)

        st.markdown('The Diabetes dataset is used as the example.')
        st.write(df.head(5))

        # California housing dataset
        california = fetch_california_housing()
        X = pd.DataFrame(california.data, columns=california.feature_names).loc[:100] # FOR TESTING PURPOSE, COMMENT THIS OUT FOR PRODUCTION
        Y = pd.Series(california.target, name='MedHouseVal').loc[:100] # FOR TESTING PURPOSE, COMMENT THIS OUT FOR PRODUCTION
        df = pd.concat([X, Y], axis=1)

        st.markdown('The California housing dataset is used as the example.')
        st.write(df.head(5))
