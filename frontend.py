from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Load your DataFrame
df = pd.read_csv('test.csv', index_col=0)

st.header("Customize AgGrid")
_function = st.sidebar.radio("Functions", ['Display', 'Highlight', 'Delete'])

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
#from selected rows, check the values of the selected row from the 6th column onwards and print the best 3 values
if _function == 'Display':
    if selected_rows:
        # Assuming selected_rows is a list of dictionaries
        # Iterate through all selected rows
        for selected_row in selected_rows:
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
            
            st.write(display_df)
            
            # Take in filepath column value and display image
            filepath = selected_row['filepath']
            st.image(filepath, width=200)
    else:
        st.write('No rows selected')
