import utils
import web_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from css import style
from PIL import Image

# General web settings
im = Image.open("images/favicon.ico")
st.set_page_config(layout="wide", page_title="MicW2Graph", menu_items={}, page_icon=im)
st.session_state.sidebar_state = 'collapsed'
style.load_css()

# Menu options
page = web_utils.show_pages_menu(index=0)
if page == "Exploratory data analysis":
    switch_page("exploratory data analysis")
elif page == "Microbial association networks":
    switch_page('microbial association networks')
elif page == "Knowledge graph":
    switch_page('knowledge graph and subgraphs')
elif page == "Case studies":
    switch_page('case studies')

# Read config yaml file 
# This will be done only once and all the pages will have access to the data
if 'config' not in st.session_state:
    st.session_state.config = utils.read_yaml('config.yml')
    
# Title of the app    
st.markdown("<h1 style='text-align: center; color: #023858;'>MicW2Graph</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2b8cbe;'>Building a knowledge graph of the wastewater treatment microbiome and its biological context</h3>", unsafe_allow_html=True)
st.markdown("---")

with st.expander('About the project'):
    st.write('''
    In this project, we investigated the microbiome of the **wastewater treatment** (WWT) process to build **MicW2Graph**, an open-source **knowledge graph** that 
    integrates WWT metagenomic and metatranscriptomic information with their biological context, including biological processes, environmental and 
    phenotypic features, chemical compounds, and additional metadata. We developed a workflow to collect meta-omics datasets from **MGnify** and infer 
    potential interactions among microorganisms through **microbial association networks**. MicW2Graph enables the investigation of research questions 
    related to WWT, focusing on aspects such as microbial connections, community memberships, and potential ecological functions.
    
    **Credits**
    - Developed by [Sebastián Ayala Ruano][myweb]. MicW2Graph was built for the thesis project from the [MSc in Systems Biology][sysbio].
    - The data for this project was obtained from [Mgnify](https://www.ebi.ac.uk/metagenomics/api/latest/), using the scripts available in this [GitHub repository][retrieve_info_mgnify].
    
    [sysbio]: https://www.maastrichtuniversity.nl/education/master/systems-biology
    [myweb]: https://sayalaruano.github.io/
    [retrieve_info_mgnify]: https://github.com/Multiomics-Analytics-Group/Retrieve_info_MGnifyAPI
    ''')

st.markdown("<h3 style='text-align: center; color: black;'>Schematic summary of the MicW2Graph project</h3>", unsafe_allow_html=True)
st.image('images/Methods_MicW2Graph.svg', use_column_width=True)

# Footer
with st.container():
    web_utils.footer()

