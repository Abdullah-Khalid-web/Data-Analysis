import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Base",page_icon="favicon.ico",layout = "wide",initial_sidebar_state="auto")

st.title("Display and Filter Graph And Table")

st.write("Use Default and upload File DataSheet for Graphing and Filtering Data")
Select_datasheet = st.radio("Select a DataSheet", ("Default","Upload"))
if Select_datasheet == "Default":
    df = pd.read_csv('xAPI-Edu-Data.csv')
elif Select_datasheet == "Upload":
    uploaded_file = st.file_uploader("Upload a file (CSV, Excel, etc.)")
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            try: 
                df = pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                st.error("Unable to decode the file. Try other encodings if needed." )   
                st.stop()
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()
    else:
        st.warning("Please upload a file.")
        st.stop()

if df is not None:    
    column_selections = {}

    for column_name in df.columns:
        selected_values = st.sidebar.multiselect(
            f"Select {column_name}",
            options=df[column_name].unique(),
            default=df[column_name].unique()
        )
        column_selections[column_name] = selected_values

    df_selection = df
    for column_name, selected_values in column_selections.items():
        if selected_values:
            df_selection = df_selection[df_selection[column_name].isin(selected_values)]

    st.subheader("Data Table")
    st.dataframe(df_selection)
    
    
    
    st.header("You can Make Graph Here:")

    graph_value = st.selectbox("Select the Type of Graph:", ("None","Single value Graph","Double value Graph","Triple value Graph","Fourth value Graph"))

    if graph_value == "None":
        st.error("You Yes You enter Graph Type First")

    elif graph_value == "Single value Graph":
        x_column = st.selectbox("Select the X-Axis Column", df.columns)  
        
        graph_type_choice = st.radio("Select a Graph Type", ("None","Bar Graph", "Scatter Graph","Circle Graph","Line Graph","Pie Graph","Area Graph"))

    
        if graph_type_choice == "Bar Graph":
            fig = px.bar(
                df_selection,
                x=x_column,
                title=x_column + "Class Distribution",
                labels={x_column: x_column},
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif graph_type_choice == "Scatter Graph":
            fig = px.scatter(
                df_selection,
                x=x_column,
                title=x_column + " Distribution",
                labels={x_column: x_column},
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif graph_type_choice == "Circle Graph":    
            fig = px.line_polar(
                df_selection,
                r=x_column,
                theta=x_column,
                line_close=True, 
                title=x_column + " Distribution (Radar Chart)",
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif graph_type_choice == "Line Graph":
            fig = px.line(
                df_selection,
                x=x_column,
                title=x_column + " Distribution",
                labels={x_column : x_column},
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif graph_type_choice == "Pie Graph":
            fig = px.pie(
                df_selection,
                names=x_column,
                title=x_column + " Distribution",
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif graph_type_choice == "Area Graph":
            fig = px.area(
                df_selection,
                x=x_column,
                title=x_column + " Distribution",
                labels={x_column: x_column},
                color=x_column
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)


    elif graph_value == "Double value Graph":
        x_column = st.selectbox("Select the X-Axis Column", df_selection.columns)
        y_column = st.selectbox("Select the Y-Axis Column", df_selection.columns)
    
        plot_type = st.radio("Select the type of plot", ["Bar Chart", "Line Chart", "Area Chart","Scatter Graph"])
        if plot_type == "Bar Chart":
            fig = px.bar(df_selection,
                        x=x_column, 
                        y=y_column, 
                        color= y_column,
                        title="Bar Chart")
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
            
        elif plot_type == "Line Chart":
            fig = px.line(df_selection, 
                        x=x_column,
                        y=y_column, 
                        color= y_column,
                        title="Line Chart",)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
            
        elif plot_type == "Area Chart":
            fig = px.area(df_selection,
                        x=x_column, 
                        y=y_column, 
                        title=" Area Chart",
                        color= y_column)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        elif plot_type == "Scatter Graph":
            fig = px.scatter(df_selection, 
                x=x_column, 
                y=y_column, 
                title=" Scatter Graph",
                color= y_column)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)



    elif graph_value == "Triple value Graph":
        x_column = st.selectbox("Select the X-Axis Column", df_selection.columns)
        y_column = st.selectbox("Select the Y-Axis Column", df_selection.columns)
        z_column = st.selectbox("Select the Z-Axis Column ", df_selection.select_dtypes(include=['number']).columns)
        plot_type = st.radio("Select the type of plot", ["3D Scatter","Bubble Scatter"])
        if plot_type == "3D Scatter":
            fig = px.scatter_3d(df_selection, 
                x=x_column, 
                y=y_column, 
                z=z_column, 
                title=x_column + " " + y_column + " " + z_column + " 3D Scatter Plot",
                color= z_column)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
        
        elif plot_type == "Bubble Scatter":
            fig = px.scatter(df_selection, 
                x=x_column, y=y_column, 
                size=z_column, 
                title=x_column + " " + y_column + " " + z_column + " Bubble Chart",
                color= z_column)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
                
    
    elif graph_value == "Fourth value Graph":
        x_column = st.selectbox("Select the X-Axis Column", df_selection.columns)
        y_column = st.selectbox("Select the Y-Axis Column", df_selection.columns)
        z_column = st.selectbox("Select the Z-Axis Column ", df_selection.columns)
        b_column = st.selectbox("Select For Bubbles ", df_selection.select_dtypes(include=['number']).columns)
        plot_type = st.radio("Select the type of plot", ["3D Scatter Bubble "])
        if plot_type == "3D Scatter Bubble ":
            fig = px.scatter_3d(df_selection, 
                x=x_column, 
                y=y_column,z=z_column, 
                size=b_column, 
                title=x_column + " " + y_column + " " + z_column + " " + b_column,
                color= b_column)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig)
            
st.subheader("Data Management App Made By SE Mafia")