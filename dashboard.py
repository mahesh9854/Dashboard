import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CSV Dashboard", layout="wide")
st.title("CSV Data Explorer Dashboard")

st.markdown("Upload a CSV file to explore and visualize your data interactively.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")
    
    with st.expander("Data Preview", expanded=True):
        st.dataframe(df, use_container_width=True)

    with st.expander("Summary Statistics"):
        st.write(df.describe())

    with st.expander("Missing Values"):
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0] if missing.sum() > 0 else "No missing values.")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    st.subheader("Visualizations")
    chart_type = st.selectbox("Choose a chart type:", ['Histogram', 'Line', 'Boxplot', 'Pie Chart', 'Scatterplot', 'Correlation Heatmap'])

    if chart_type == 'Histogram':
        col = st.selectbox("Select numeric column", numeric_cols)
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f'Histogram of {col}')
        st.pyplot(fig)

    elif chart_type == 'Line':
        col = st.selectbox("Select numeric column", numeric_cols)
        st.line_chart(df[col])

    elif chart_type == 'Boxplot':
        col = st.selectbox("Select numeric column", numeric_cols)
        fig, ax = plt.subplots()
        sns.boxplot(x=df[col], ax=ax, color='orange')
        ax.set_title(f'Boxplot of {col}')
        st.pyplot(fig)

    elif chart_type == 'Pie Chart':
        if categorical_cols:
            col = st.selectbox("Select categorical column", categorical_cols)
            pie_data = df[col].value_counts().head(10)
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title(f'Pie Chart of {col}')
            st.pyplot(fig)
        else:
            st.warning("No categorical columns available for pie chart.")

    elif chart_type == 'Scatterplot':
        col_x = st.selectbox("X-axis", numeric_cols, index=0)
        col_y = st.selectbox("Y-axis", numeric_cols, index=1)
        fig, ax = plt.subplots()
        sns.scatterplot(x=col_x, y=col_y, data=df, ax=ax)
        ax.set_title(f'Scatterplot: {col_x} vs {col_y}')
        st.pyplot(fig)

    elif chart_type == 'Correlation Heatmap':
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
        ax.set_title('Correlation Heatmap')
        st.pyplot(fig)

