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
st.session_state.sidebar_state = "collapsed"
style.load_css()

page = web_utils.show_pages_menu(index=2)
if page == "Home":
    switch_page("micw2graph home")
elif page == "Exploratory data analysis":
    switch_page("exploratory data analysis")
elif page == "Knowledge graph":
    switch_page("knowledge graph and subgraphs")
elif page == "Case studies":
    switch_page("case studies")

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

st.markdown(
    "<h3 style='text-align: center; color: black;'>Microbial association networks by wastewater treatment sub-biome and experiment types</h3>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    subcol1, subcol2 = st.columns(2)

    with subcol1:
        # Selectbox to choose the sub-biome to explore
        sub_biome = st.selectbox(
            " ",
            [
                "Activated sludge",
                "Wastewater",
                "Industrial wastewater",
                "Water and sludge",
            ],
            index=None,
            placeholder="Sub-biome:",
            label_visibility="collapsed",
        )

    with subcol2:
        # Selectbox to choose the experiment type
        exp_type = st.selectbox(
            " ",
            ["Metagenomics", "Metatranscriptomics", "Assembly"],
            index=None,
            placeholder="Experiment type:",
            label_visibility="collapsed",
        )

    if sub_biome == None or exp_type == None:
        st.warning("Please select a sub-biome and experiment type.", icon="⚠️")
        st.stop()

    # Replace spaces with underscores
    sub_biome = sub_biome.replace(" ", "_")

    try:
        # Get the microbial asso net path from the config file
        microbial_asso_net_path = st.session_state.config["microbial_asso_nets"][
            sub_biome
        ][exp_type]

        # Add the .graphml extension to the path
        microbial_asso_net_graphml = microbial_asso_net_path + ".graphml"

        # Load and preprocess the network data
        G = web_utils.load_and_preprocess_net(microbial_asso_net_graphml)
    except:
        st.warning(
            "The network is not available. Please select another sub-biome and experiment type.",
            icon="⚠️",
        )
        st.stop()

    # Initiate PyVis network object
    net = Network(height="600px", width="100%", bgcolor="white", font_color="#555555")

    # Take Networkx graph and translate it to a PyVis graph format
    net.from_nx(G)

    # Show number of nodes and edges
    st.markdown(
        f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {len(net.nodes)} </p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {len(net.edges)} </p>",
        unsafe_allow_html=True,
    )

    # Modify nodes to add custom labels, titles, border widths, and colors
    for node in net.nodes:
        node_id = node["id"]
        node_data = G.nodes[node_id]
        node["font"] = {"size": 12}
        node_data.get("name", node_id)
        node["borderWidth"] = 2
        node["borderWidthSelected"] = 2.5

    # Streamlit checkbox for physics interactivity
    control_layout = st.checkbox("Add panel to control layout", value=False)

    # Conditionally apply the force_atlas_2based layout based on checkbox
    if control_layout:
        net.force_atlas_2based(
            gravity=-30,
            central_gravity=0.005,
            spring_length=100,
            spring_strength=0.1,
            damping=0.4,
        )
        net.show_buttons(filter_=["physics"])
    else:
        net.force_atlas_2based(
            gravity=-30,
            central_gravity=0.005,
            spring_length=100,
            spring_strength=0.1,
            damping=0.4,
        )

    # Add the .html extension to the path
    microbial_asso_net_html = microbial_asso_net_path + ".html"

    # Save network as HTML
    net.save_graph(microbial_asso_net_html)

    # Load HTML data
    html_data = utils.load_html_file(microbial_asso_net_html)

    if control_layout:
        # Load HTML into HTML component for display on Streamlit
        components.html(html_data, height=1100)
    else:
        # Load HTML into HTML component for display on Streamlit
        components.html(html_data, height=600)

    c1, c2, c3 = st.columns(3)

    with c1:
        # Add the .csv extension to the path
        microbial_asso_net_csv = microbial_asso_net_path + ".csv"
        st.download_button(
            label="Download as edge list (.csv)",
            data=open(microbial_asso_net_csv, "r", encoding="utf-8"),
            file_name=f"{sub_biome}_{exp_type}_microb_asso_net.csv",
            mime="text/plain",
        )
    with c2:
        st.download_button(
            label="Download as GraphML",
            data=open(microbial_asso_net_graphml, "r", encoding="utf-8"),
            file_name=f"{sub_biome}_{exp_type}_microb_asso_net.graphml",
            mime="text/plain",
        )
    with c3:
        # Add the .cyjs extension to the path
        microbial_asso_net_cyjs = microbial_asso_net_path + ".cyjs"
        st.download_button(
            label="Download as Cyjs",
            data=open(microbial_asso_net_cyjs, "r", encoding="utf-8"),
            file_name=f"{sub_biome}_{exp_type}_microb_asso_net.cyjs",
            mime="text/plain",
        )

with col3:
    st.write("")

# Footer
with st.container():
    web_utils.footer()
