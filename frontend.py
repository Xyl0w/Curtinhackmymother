import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import os
import time
# Load your DataFrame
df = pd.read_csv('test.csv', index_col=0)

st.header("Tommy's Findings")
_function = st.sidebar.radio("Functions", ['Display Provided Dataset', 'Display EDMS Dataset', 'SELF DESTRUCT'])

if _function == 'Display Dataset 1':
    df = pd.read_csv('test.csv', index_col=0)
    st.write('Displaying Dataset 1')
    
if _function == 'Display Dataset 2':
    df = pd.read_csv('test_emd.csv', index_col=0)
    st.write('Displaying Dataset 2')
# Configure grid options with pagination
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_side_bar()
gd.configure_grid_options(domLayout='normal', rowHeight=50)
gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
gd.configure_selection('multiple', use_checkbox=True)

sel_mode = st.selectbox("Selection Mode", ['single', 'multiple'])
gd.configure_selection(sel_mode, use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)

grid_table = AgGrid(df, gridOptions=gd.build(),
                    height=500,
                    width='100%',
                    data_return_mode=DataReturnMode.AS_INPUT,
                    update_mode=GridUpdateMode.MODEL_CHANGED)
selected_rows = grid_table['selected_rows']
clusters = df['cluster']
classes = df['group']
pca1_values = df['pca1']
pca2_values = df['pca2']

# Function to create PCA plot
def create_pca_plot(X_pca, clusters, classes):
    row = 0 
    col = 1
    color_wheel = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    marker_wheel = ["o", "s", "D", "^", "v", "p", "*", "+", "x", "h", "H", "d", "|", "_", "<", ">"]
    ci, mi = 0, 0 
    fig, ax = plt.subplots()

    for cluster_value in set(clusters):
        mi = 0
        for class_value in set(classes):
            mask = [True if clusters[idx] == cluster_value and classes[idx] == class_value else False for idx in range(len(clusters))]
            plt.scatter(X_pca[:, row][mask], X_pca[:, col][mask], c=color_wheel[ci], marker=marker_wheel[mi])
            mi += 1
        ci += 1
    
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('PCA Plot')
    
    return fig

# From selected rows, check the values of the selected row from the 6th column onwards and print the best 3 values
if _function == 'Display Dataset 1' or _function == 'Display Dataset 2':
    if selected_rows:
        for selected_row in selected_rows:
            with st.expander("See Full Selected Data"):
                st.write(selected_row)
            
            # Create X_pca as a list of tuples
            X_pca = np.array(list(zip(pca1_values, pca2_values)))

            # Create a PCA plot
            pca_plot = create_pca_plot(X_pca, clusters, classes)

            with st.expander("See Real Time Analysis"):
                st.write("The Chart Below Shows Clusters Based on Component Importance.")
                st.pyplot(pca_plot)
            
            # Assuming you want to access columns starting from the 6th column
            selected_values = [selected_row[column] for column in selected_row.keys()][5:]

            # Get column names corresponding to the selected values
            column_names = list(selected_row.keys())[5:]
            # Create a list of tuples (column name, value) for sorting
            values_with_column_names = [(column, value) for column, value in zip(column_names, selected_values)]

            # Sort the values based on value (assuming they are numeric)
            sorted_values_with_column_names = sorted(values_with_column_names, key=lambda x: x[1], reverse=True)

            # Select the top 3 values with column names
            top_3_values_with_column_names = sorted_values_with_column_names[:3]
            
            # Display top 3 as a table
            display_df = pd.DataFrame(top_3_values_with_column_names, columns=['Object Most Similar', 'Probability'])
            
            with st.expander("See Top 3 Similar Objects"):
                col1, col2 = st.columns(2)
                with col1:
                    display_df = pd.DataFrame(top_3_values_with_column_names, columns=['Object Most Similar', 'Probability'])
                    st.write(display_df)

            # Display the image in the second column
                with col2:
                    filepath = selected_row['filepath']
                    st.image(filepath, width=200)
            
    else:
        st.write('No rows selected')
     
        
if _function == 'SELF DESTRUCT':
    st.balloons()
    st.write('Say goodbye to tommy! ;-; ')
    time.sleep(3)
    st.write('JK don\'t kill tommy pls :3')
    time.sleep(3)
    st.write('Putting you back now...')
    #select display
    _function = 'Display'
    
