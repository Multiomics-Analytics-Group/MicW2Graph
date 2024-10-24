import utils
import web_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from css import style
from PIL import Image
from pyvis.network import Network
import streamlit.components.v1 as components

# General web settings
im = Image.open("images/MicW2Graph_logo.ico")
st.set_page_config(layout="wide", page_title="MicW2Graph", menu_items={}, page_icon=im)
st.session_state.sidebar_state = 'collapsed'
style.load_css()

page = web_utils.show_pages_menu(index=4)
if page == "Home":
    switch_page("micw2graph home")
elif page == "Exploratory data analysis":
    switch_page("exploratory data analysis")
elif page == "Microbial association networks":
    switch_page('microbial association networks')
elif page == "Knowledge graph":
    switch_page('knowledge graph and subgraphs')

# Title of the app    
st.markdown("<h1 style='text-align: center; color: #023858;'>MicW2Graph</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2b8cbe;'>Building a knowledge graph of the wastewater treatment microbiome and its biological context</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("<h3 style='text-align: center; color: black;'>Case studies based on an association and functional clusters</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:

    # Selectbox to choose the case study
    case_study = st.selectbox(" ", 
                              ["Wastewater and metagenomics association cluster1", 
                               "Wastewater and metagenomics functional cluster", 
                               "Wastewater and metagenomics association cluster2", 
                               "Activated sludge and metagenomics association cluster"],
                               index = None,
                               placeholder = "Case study:",
                               label_visibility = "collapsed",)
    
    try:
        # Replace spaces with underscores
        case_study = case_study.replace(" ", "_")
        
    except:
        st.warning("Please select a case study.", icon="⚠️")
        st.stop()

    try:                 
        # Get the case study path from the config file
        case_study_path = st.session_state.config['case_studies'][case_study]

        # Add the .graphml extension to the path
        case_study_graphml = case_study_path + ".graphml"

        # Get the node and edge colors from the config file
        color_nodes = st.session_state.config['kg_nodes']
        edge_colors = st.session_state.config['kg_edges']
        
        # Load and preprocess the network data
        G = web_utils.load_and_preprocess_kg(case_study_graphml, color_nodes, edge_colors, min_size = 8, max_size = 24)
    except:
        st.warning("The knowledge graph is not available. Please select another sub-biome and experiment type.", icon="⚠️")
        st.stop()

    # Initiate PyVis network object
    net = Network(height='600px', width="100%", bgcolor='white', font_color='#555555')
    
    # Take Networkx graph and translate it to a PyVis graph format
    net.from_nx(G)

    # Show number of nodes and edges
    st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {len(net.nodes)} </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {len(net.edges)} </p>", unsafe_allow_html=True)

    # Modify nodes to add custom labels, titles, border widths, and colors
    for node in net.nodes:
        node_id = node['id']
        node_data = G.nodes[node_id]
        node['font'] = {'size': 12}
        label = node_data.get('name')
        node['label'] = label
        #node['title'] = label  # Tooltip text
        node_data.get('name', node_id)  # Tooltip text
        node['borderWidth'] = 1.5
        node['borderWidthSelected'] = 2
        node['color'] = {
            'background': node_data['color'],
            'border': node_data['border-color']
        }

    # Modify edges to add custom colors and labels
    for edge in net.edges:
        u, v = edge['from'], edge['to']
        edge_data = G.get_edge_data(u, v)
        edge['color'] = edge_data['color']
        edge['font'] = {'size': 6}
    
    # Streamlit checkbox for physics interactivity
    control_layout = st.checkbox('Add panel to control layout', value=False)

    # Conditionally apply the force_atlas_2based layout based on checkbox
    if control_layout:
        net.force_atlas_2based(gravity=-15, central_gravity=0.005, spring_length=100, spring_strength=0.1, damping=0.4)
        net.show_buttons(filter_=['physics'])
    else:
        net.force_atlas_2based(gravity=-15, central_gravity=0.005, spring_length=100, spring_strength=0.1, damping=0.4)

    # Add the .html extension to the path
    case_study_html = case_study_path + ".html"
    
    # Save network as HTML
    net.save_graph(case_study_html)

    # Load HTML data
    html_data = utils.load_html_file(case_study_html)
    
    if control_layout: 
        # Load HTML into HTML component for display on Streamlit
        components.html(html_data, height=1100)
    else:
        # Load HTML into HTML component for display on Streamlit
        components.html(html_data, height=600)
    
    subcol1, subcol2, subcol3 = st.columns(3)

    with subcol1:
        st.write('')
    
    with subcol2:
        st.download_button(
            label="Download as GraphML",
            data=open(case_study_graphml,'r',encoding='utf-8'),
            file_name=f'{case_study}_subgraph.graphml',
            mime='text/plain',
        )
    with subcol3:
        st.write('')

with col3:
    st.write('')    

# Footer
with st.container():
    web_utils.footer()
