import utils
import web_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from css import style
from PIL import Image

# General web settings
im = Image.open("images/MicW2Graph_logo.ico")
st.set_page_config(layout="wide", page_title="MicW2Graph", menu_items={}, page_icon=im)
st.session_state.sidebar_state = "collapsed"
style.load_css()

# Menu options
page = web_utils.show_pages_menu(index=0)
if page == "Exploratory data analysis":
    switch_page("exploratory data analysis")
elif page == "Microbial association networks":
    switch_page("microbial association networks")
elif page == "Knowledge graph":
    switch_page("knowledge graph and subgraphs")
elif page == "Case studies":
    switch_page("case studies")

# Read config yaml file
# This will be done only once and all the pages will have access to the data
if "config" not in st.session_state:
    st.session_state.config = utils.read_yaml("config.yml")

# Title of the app
st.markdown(
    "<h1 style='text-align: center; color: #023858;'>MicW2Graph</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #2b8cbe;'>Building a knowledge graph of the wastewater treatment microbiome and its biological context</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Summary of the project
st.markdown(
    """
<p style="text-align: justify;"><strong style="color: #023858">Wastewater treatment</strong> (WWT) is the process of removing contaminants from used water before it is discharged 
back into the environment, which contributes to address water scarcity and to protect aquatic ecosystems. In this project, we investigated the microbiome of WWT to build 
<strong style="color: #023858">MicW2Graph</strong>, an open-source <strong style="color: #023858">knowledge graph</strong> (KG) that integrates metagenomic 
and metatranscriptomic information with their biological context, including biological processes, environmental and phenotypic features, chemical compounds, 
and additional metadata. We developed a workflow to collect meta-omics datasets from <strong style="color: #023858">MGnify</strong> and infer potential 
interactions among microorganisms through <strong style="color: #023858">microbial association networks</strong> (MANs). MicW2Graph enables the investigation of research 
questions related to WWT, focusing on aspects such as microbial connections, community memberships, and potential ecological functions.</p>
""",
    unsafe_allow_html=True,
)

# Schematic summary of the project
st.markdown(
    "<h3 style='text-align: center; color: black;'>Schematic summary of the MicW2Graph project</h3>",
    unsafe_allow_html=True,
)
st.image("images/Methods_MicW2Graph.svg", use_column_width=True)

# Credits
st.markdown(
    "<h3 style='text-align: center; color: black;'>Credits and Contributors</h3>",
    unsafe_allow_html=True,
)
st.write(
    """
- Developed by [Sebastián Ayala Ruano][myweb] under the supervision of [Dr. Alberto Santos][Alberto], head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- MicW2Graph was built for the thesis project from the [MSc in Systems Biology][sysbio] at the MoNA group.
- The data for this project was obtained from [Mgnify](https://www.ebi.ac.uk/metagenomics/api/latest/), using the scripts available in this [GitHub repository][retrieve_info_mgnify].

[sysbio]: https://www.maastrichtuniversity.nl/education/master/systems-biology
[myweb]: https://sayalaruano.github.io/
[Alberto]: https://orbit.dtu.dk/en/persons/alberto-santos-delgado
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[retrieve_info_mgnify]: https://github.com/Multiomics-Analytics-Group/Retrieve_info_MGnifyAPI
"""
)

# Footer
with st.container():
    web_utils.footer()
