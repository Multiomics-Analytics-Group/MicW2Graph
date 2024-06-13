import utils
import web_utils
import web_utils
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from css import style
from PIL import Image
import plotly.express as px
import pandas as pd


# General web settings
im = Image.open("images/MicW2Graph_logo.ico")
st.set_page_config(layout="wide", page_title="MicW2Graph", menu_items={}, page_icon=im)
st.session_state.sidebar_state = 'collapsed'
style.load_css()

page = web_utils.show_pages_menu(index=1)
if page == "Home":
    switch_page("micw2graph home")
elif page == "Microbial association networks":
    switch_page('microbial association networks')
elif page == "Knowledge graph":
    switch_page('knowledge graph and subgraphs')
elif page == "Case studies":
    switch_page('case studies')

# Loading the Mgnify waste water treatment studies data
studies_data = utils.load_studies_data("data/EDA/wwtstudies_greater_mediantaxa_perbiome_species.csv")

# Title of the app    
st.markdown("<h1 style='text-align: center; color: #023858;'>MicW2Graph</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2b8cbe;'>Building a knowledge graph of the wastewater treatment microbiome and its biological context</h3>", unsafe_allow_html=True)
st.markdown("---")

# Selectbox for selecting the type of EDA
eda_type = st.selectbox(
    " ", 
    ["Summary of all studies", 
     "Summary of studies by biome", 
     "Summary of a specific study", 
     "Comparison between studies"],
     index = None,
     placeholder = "Select an exploratory data analysis type",
     label_visibility = "collapsed",)

if eda_type == "Summary of all studies":
    # Display title 
    st.markdown("<h3 style='text-align: center; color: black;'>Exploratory data analysis for all studies</h3>", unsafe_allow_html=True)
    
    # Create plot the number of studies per studies 
    st.markdown("<h4 style='text-align: left; color: black;'>Number of samples per study</h4>", unsafe_allow_html=True)
    hist_samples = web_utils.plot_histogram(studies_data, 'n_samples', 'Number of samples', 
                                         'Number of studies', 40, px.colors.qualitative.Plotly)
    st.plotly_chart(hist_samples, use_container_width=True)

    # Create a pie plot for the sampling countries of the studies
    st.markdown("<h4 style='text-align: left; color: black;'>Sampling countries for all studies</h4>", unsafe_allow_html=True)
    pie_plot_countries = web_utils.plot_pie(studies_data, 'sampling_country', 
                                            'Country', px.colors.qualitative.Dark24)
    st.plotly_chart(pie_plot_countries, use_container_width=True)

    # Create bar plot for the data types of the studies
    st.markdown("<h4 style='text-align: left; color: black;'>Data types for all studies</h4>", unsafe_allow_html=True)
    bar_plot_dtypes = web_utils.plot_bar(studies_data, 'experiment_type', 'biome', 'Biome',
                                             'Experiment type', 'Number of studies', px.colors.qualitative.Dark24)
    st.plotly_chart(bar_plot_dtypes, use_container_width=True)

    # Access the merged files per biome paths from the config file
    merged_files_per_biome = st.session_state.config['merged_files_per_biome']

    # Load the merged abundance and taxonomic data per biome
    abund_df_species_wwt = pd.read_csv(merged_files_per_biome["Wastewater"]["abundance"], index_col=0)
    tax_df_species_wwt = pd.read_csv(merged_files_per_biome["Wastewater"]["taxonomy"], index_col=0)

    abund_df_species_wwt_ws = pd.read_csv(merged_files_per_biome["Wastewater_Water_and_sludge"]["abundance"], index_col=0)
    tax_df_species_wwt_ws = pd.read_csv(merged_files_per_biome["Wastewater_Water_and_sludge"]["taxonomy"], index_col=0)

    abund_df_species_wwt_ind = pd.read_csv(merged_files_per_biome["Wastewater_Industrial_wastewater"]["abundance"], index_col=0)
    tax_df_species_wwt_ind = pd.read_csv(merged_files_per_biome["Wastewater_Industrial_wastewater"]["taxonomy"], index_col=0)

    abund_df_species_wwt_as = pd.read_csv(merged_files_per_biome["Wastewater_Activated_Sludge"]["abundance"], index_col=0)
    tax_df_species_wwt_as = pd.read_csv(merged_files_per_biome["Wastewater_Activated_Sludge"]["taxonomy"], index_col=0)
    
    # Create pie plot for the number of studies and samples per biome
    st.markdown("<h4 style='text-align: left; color: black;'>Number of studies and samples per biome</h4>", unsafe_allow_html=True)
    
    # Calculate the number of studies per biome
    studies_per_biome = studies_data["biome"].value_counts()
    biomes = studies_per_biome.index

    # Calculate the number of samples per biome by counting the number of columns in the abundance table, excluding the "Species" column
    samples_per_biome = [abund_df_species_wwt_as.shape[1], abund_df_species_wwt.shape[1], 
                        abund_df_species_wwt_ws.shape[1], abund_df_species_wwt_ind.shape[1]]

    # Create the pie plots
    pie_plots_biomes = web_utils.plot_two_pies(biomes, studies_per_biome.values, samples_per_biome, 
                    'Studies', 'Samples', 'Biomes', px.colors.qualitative.Dark24)
    st.plotly_chart(pie_plots_biomes, use_container_width=True)

    # Create a stacked bar plot for the top 5 species by biome
    st.markdown("<h4 style='text-align: left; color: black;'>Top 5 species by biome</h4>", unsafe_allow_html=True)
    
    # Prepare the lists of dataframes and biome names
    abund_dfs = [abund_df_species_wwt, abund_df_species_wwt_ws, abund_df_species_wwt_ind, abund_df_species_wwt_as]
    tax_dfs = [tax_df_species_wwt, tax_df_species_wwt_ws, tax_df_species_wwt_ind, tax_df_species_wwt_as]
    biome_names = ['Wastewater', 'Water and sludge', 'Industrial wastewater', 'Activated sludge']

    # Create the stacked bar plot
    top_species_plot_biome, abund_tax_merged = web_utils.plot_stacked_bar_allbiomes(abund_dfs, tax_dfs, biome_names, px.colors.qualitative.Dark24)
    st.plotly_chart(top_species_plot_biome, use_container_width=True)

    # Create PCoA plots for all studies colored by different variables
    st.markdown("<h4 style='text-align: left; color: black;'>PCoA plots of samples from all studies using Bray-Curtis dissimilarity matrices</h4>", unsafe_allow_html=True)

    # Access the merged files for all biomes from the config file
    merged_files_all_biomes = st.session_state.config['merged_files_allbiomes']
    
    # Load the merged abundance tables and metadata
    sample_info = pd.read_csv(merged_files_all_biomes["samples"])
    abund_df = pd.read_csv(merged_files_all_biomes["abundance"], index_col=0)
    study_ids = pd.read_csv(merged_files_all_biomes["study_ids"], index_col=0)
    
    # Calculate Bray-Curtis dissimilarity matrix and preprocess sample info
    bc_mat, samples_df = utils.calculate_bray_curtis_dist(abund_df, 'all_biomes', sample_info)
    
    # Dropdown menu for selecting the color variable
    color_option = st.selectbox("Select a variable to color by:", 
                                ('Biomes', 'Study ID and Biome', 'Sampling country', 'Experiment type',
                                'MGnify pipeline', 'Sequencing platform'))

    # Create a function to update the figure
    def update_figure(selected_variable):
        if selected_variable == 'Biomes':
            return 'biome'
        elif selected_variable == 'Study ID and Biome':
            return 'study_id'
        elif selected_variable == 'Sampling country':
            return 'sampling_country'
        elif selected_variable == 'Experiment type':
            return 'experiment_type'
        elif selected_variable == 'MGnify pipeline':
            return 'pipeline_version'
        elif selected_variable == 'Sequencing platform':
            return 'instrument_platform'

    # Select colors based on the unique values of the selected variable
    color_var = update_figure(color_option)

    # Show the PCoA plot
    pcoa_plot_all_studies = web_utils.plot_pcoa(bc_mat, samples_df, studies_data, color_var, color_option, 'all_biomes', study_ids)
    st.plotly_chart(pcoa_plot_all_studies, use_container_width=True)

    # Display sample information for all studies
    st.markdown("<h4 style='text-align: left; color: black;'>Sample information for all studies</h4>", unsafe_allow_html=True)
    web_utils.display_dataframe_with_aggrid(sample_info)

    # Button to download the sample information as a CSV file
    sample_info_csv = utils.convert_df(sample_info)
    st.download_button(
        label="Download sample data as CSV",
        data=sample_info_csv,
        file_name='sample_info_allbiomes.csv',
        mime='text/csv',
    )

    # Display merged abundance data for all studies
    st.markdown("<h4 style='text-align: left; color: black;'>Abundance data for all studies</h4>", unsafe_allow_html=True)

    # Reset the index to make it a column
    abund_table_with_index = abund_tax_merged.reset_index()

    # Ensure the index column is the first one
    column_order = ["Species"] + [col for col in abund_table_with_index.columns if col != "Species"]
    abund_table_with_index = abund_table_with_index[column_order]

    web_utils.display_dataframe_with_aggrid(abund_table_with_index)

    # Button to download the abundance data as a CSV file
    abund_df_csv = utils.convert_df(abund_df)
    st.download_button(
        label="Download abundance data as CSV",
        data=abund_df_csv,
        file_name='abundance_data_allbiomes.csv',
        mime='text/csv',
    )

elif eda_type == "Summary of studies by biome":
    # Get the unique biomes removing nan values
    biomes = studies_data["biome"].unique()
    biomes = [b for b in biomes if str(b) != 'nan']

    # Sort the biomes
    biomes.sort()

    # Title for the page
    st.markdown("<h3 style='text-align: center; color: black;'>Exploratory data analysis for studies by biome</h3>", unsafe_allow_html=True)

    # Create a selectbox to choose the biome
    biome = st.selectbox(
        " ", 
        biomes,
        index = None,
        placeholder = "Select a sub-biome",
        label_visibility = "collapsed",) 

    # Replace the ":" and " " characters by "_" in the biome name
    try:
        biome = biome.replace(":", "_").replace(" ", "_")
    except:
        st.warning("Please select a sub-biome", icon="⚠️")
        st.stop()

    # Load the merged abundance and sample data for the selected biome
    sample_info = pd.read_csv(f"data/EDA/Samples_metadata/Merged_tables/Biomes/{biome}_merged_samples_metadata.csv")
    abund_df = pd.read_csv(f"data/EDA/Abundance_tables/Merged_tables/Biomes/{biome}/{biome}_merged_abund_tables_species.csv", index_col=0)
    tax_df = pd.read_csv(f"data/EDA/Abundance_tables/Merged_tables/Biomes/{biome}/{biome}_merged_taxa_tables_species.csv", index_col=0)
    study_ids = pd.read_csv(f"data/EDA/Abundance_tables/Merged_tables/Biomes/{biome}/{biome}_studies_per_sample.csv", index_col=0)

    # Calculate Bray-Curtis dissimilarity matrix and preprocess sample info
    bc_mat, samples_df = utils.calculate_bray_curtis_dist(abund_df, 'biome', sample_info)

    # Create a violin plot to show the distribution of the distances within and between the studies
    st.markdown("<h4 style='text-align: left; color: black;'>Distribution of the Bray-Curtis distances</h4>", unsafe_allow_html=True)
    violin_distances = web_utils.plot_distances_violins(bc_mat, study_ids)
    st.plotly_chart(violin_distances, use_container_width=True)
    st.warning('Some studies have just a few samples, so they are not shown in this plot', icon="⚠️")

    # Create a barplot to show the top 5 species per study
    st.markdown("<h4 style='text-align: left; color: black;'>Top 5 species per study</h4>", unsafe_allow_html=True)
    top_species_plot, abund_df_merged = web_utils.plot_stacked_bar_bybiome(abund_df, tax_df, study_ids)
    st.plotly_chart(top_species_plot, use_container_width=True)

    # Create PCoA plots by biome for all studies 
    st.markdown(f"<h4 style='text-align: left; color: black;'>PCoA plots of samples from the {biome} biome using Bray-Curtis dissimilarity matrices</h4>", unsafe_allow_html=True)

    # Dropdown menu for selecting the color variable
    color_option = st.selectbox("Select a variable to color by:", 
                                ('Biomes', 'Study ID and Biome', 'Sampling country', 'Experiment type',
                                'MGnify pipeline', 'Sequencing platform'))

    # Create a function to update the figure
    def update_figure(selected_variable):
        if selected_variable == 'Biomes':
            return 'specific_biome'
        elif selected_variable == 'Study ID and Biome':
            return 'study_id'
        elif selected_variable == 'Sampling country':
            return 'sampling_country'
        elif selected_variable == 'Experiment type':
            return 'experiment_type'
        elif selected_variable == 'MGnify pipeline':
            return 'pipeline_version'
        elif selected_variable == 'Sequencing platform':
            return 'instrument_platform'
    
    # Select colors based on the unique values of the selected variable
    color_var = update_figure(color_option)

    # Show the PCoA plot
    pcoa_plot_biome = web_utils.plot_pcoa(bc_mat, samples_df, studies_data, color_var, color_option, 'biome', study_ids)
    st.plotly_chart(pcoa_plot_biome, use_container_width=True)

    # Display abundance data for the selected biome
    biome_title = biome.replace("Wastewater_", "").replace("_", " ")
    st.markdown(f"<h4 style='text-align: left; color: black;'>Abundance table for the {biome_title} biome</h4>", unsafe_allow_html=True)

    # Reset the index to make it a column
    abund_table_with_index = abund_df_merged.reset_index()

    # Ensure the index column is the first one
    column_order = ["Species"] + [col for col in abund_table_with_index.columns if col != "Species"]
    abund_table_with_index = abund_table_with_index[column_order]

    web_utils.display_dataframe_with_aggrid(abund_table_with_index)

    # Button to download the abundance data as a CSV file
    abund_df_csv = utils.convert_df(abund_df)
    st.download_button(
        label=f"Download abundance table as CSV",
        data=abund_df_csv,
        file_name=f"Abundance_data_{biome_title}.csv",
        mime='text/csv',
    )

    # Display sample information for the selected biome
    st.markdown(f"<h4 style='text-align: left; color: black;'>Sample table for the {biome_title} biome</h4>", unsafe_allow_html=True)
    web_utils.display_dataframe_with_aggrid(sample_info)

    # Button to download the sample information as a CSV file
    sample_info_csv = utils.convert_df(sample_info)
    st.download_button(
        label=f"Download sample data as CSV",
        data=sample_info_csv,
        file_name=f"Sample_info_{biome_title}.csv",
        mime='text/csv',
    )

elif eda_type == "Summary of a specific study":
    # Title for the page
    st.markdown("<h3 style='text-align: center; color: black;'>Exploratory data analysis for a specific study</h3>", unsafe_allow_html=True)
    
    # Get unique study names
    studies_list = studies_data['study_id'].unique()
    studies_list = studies_list[~pd.isnull(studies_list)]

    subcol1, subcol2 = st.columns(2)

    with subcol1:
        # Create a selectbox to choose the study
        selected_study = st.selectbox(
            " ", 
            studies_list,
            index = None,
            placeholder = "Select a Mgnify study ID",
            label_visibility = "collapsed",)
        
    with subcol2:
        # Create a selectbox to choose the taxonomic rank
        tax_rank = st.selectbox(
            " ",
            options=["Phylum", "Genus", "Species"],
            index = None,
            placeholder = "Select a taxonomic rank",
            label_visibility = "collapsed",
        )
    if selected_study == None or tax_rank == None:
        st.warning("Please select a study and a taxonomic rank", icon="⚠️")
        st.stop()   

    # Load data for the selected study
    study_info, sample_info = utils.load_study_data(studies_data, selected_study)

    # Load and preprocess abundance table for the selected study and taxonomic rank. Store it in an independent variable
    if tax_rank == 'Phylum':
        abund_table = utils.load_abund_table(selected_study, tax_rank='phylum')
        abund_table = utils.preprocess_abund_table(abund_table, tax_rank='phylum')
    elif tax_rank == 'Genus':
        abund_table = utils.load_abund_table(selected_study, tax_rank='genus')
        abund_table = utils.preprocess_abund_table(abund_table, tax_rank='genus')
    elif tax_rank == 'Species':
        abund_table = utils.load_abund_table(selected_study, tax_rank='species')
        abund_table = utils.preprocess_abund_table(abund_table, tax_rank='species')
    
    # Display study information
    st.markdown(f"<h4 style='text-align: left; color: black;'>Summary of the {selected_study} study</h4>", unsafe_allow_html=True)

    # Create a df to summarize the study information
    summ_df = pd.DataFrame(study_info).T

    # Remove study_id row
    summ_df = summ_df.drop(index='study_id')

    # Replace indices and column names
    summ_df.index = ['Description', 'Bioproject ID', 'Centre name', 'Number of samples', 
                    'Biome','Experiment type', 'Pipeline version', 'Instrument platform',
                    'Sampling country']

    summ_df.columns = ['Summary metrics']

    st.data_editor(
        summ_df,
        width = 1000,
        column_config={
            "widgets": st.column_config.TextColumn(
                f"Summary {selected_study}",
                help= f"Summary of the study {selected_study}"
            )
        },
        hide_index=False,
    )

    # Add condition to check if the study has more than one sample
    if len(sample_info) > 2:
        # Create a violin plot to show the distribution of the distances within the study
        st.markdown(f"<h4 style='text-align: left; color: black;'>Distribution of the Bray-Curtis distances for the {selected_study} study</h4>", unsafe_allow_html=True)

        # Calculate Bray-Curtis dissimilarity matrix and preprocess sample info
        bc_mat, samples_df = utils.calculate_bray_curtis_dist(abund_table, 'study', sample_info, tax_rank)
        
        # Show the violin plot
        violin_plot_study = web_utils.plot_distances_violin(bc_mat)
        st.plotly_chart(violin_plot_study, use_container_width=True)

        # Create a bar plot to show the top 10 most abundant taxa
        st.markdown(f"<h4 style='text-align: left; color: black;'>Top 10 most abundant {tax_rank} in the {selected_study} study</h4>", unsafe_allow_html=True)
        bar_plot_top10 = web_utils.plot_bar_top10taxa(abund_table, tax_rank)
        st.plotly_chart(bar_plot_top10, use_container_width=True)

        # Create PCoA plot for the selected study
        st.markdown(f"<h4 style='text-align: left; color: black;'>PCoA plot of samples from the {selected_study} study at {tax_rank} using Bray-Curtis dissimilarity matrices</h4>", unsafe_allow_html=True)
        pcoa_plot_biome = web_utils.plot_pcoa(bc_mat, samples_df, studies_data, 'biome', "Biome", 'study')
        st.plotly_chart(pcoa_plot_biome, use_container_width=True)

        # Display abundance data for the selected study
        st.markdown(f"<h4 style='text-align: left; color: black;'>Abundance data for the {selected_study} study at {tax_rank} level</h4>", unsafe_allow_html=True)

        # Capture the name of the index, or default to 'index' if it's unnamed
        index_name = abund_table.index.name if abund_table.index.name else 'index'

        # Reset the index to make it a column
        abund_table_with_index = abund_table.reset_index()

        # Ensure the index column is the first one
        column_order = [index_name] + [col for col in abund_table_with_index.columns if col != index_name]
        abund_table_with_index = abund_table_with_index[column_order]

        web_utils.display_dataframe_with_aggrid(abund_table_with_index)

        # Button to download the abundance data as a CSV file
        abund_df_csv = utils.convert_df(abund_table)
        st.download_button(
            label=f"Download abundance table as CSV",
            data=abund_df_csv,
            file_name=f"Abundance_data_{selected_study}_{tax_rank}.csv",
            mime='text/csv',
        )

        # Display sample information for the selected study
        st.markdown(f"<h4 style='text-align: left; color: black;'>Sample table for the {selected_study} study at {tax_rank} level</h4>", unsafe_allow_html=True)
        web_utils.display_dataframe_with_aggrid(sample_info)

        # Button to download the sample information as a CSV file
        sample_info_csv = utils.convert_df(sample_info)
        st.download_button(
            label=f"Download sample data as CSV",
            data=sample_info_csv,
            file_name=f"Sample_info_{selected_study}_{tax_rank}.csv",
            mime='text/csv',
        )

    else:
        st.warning('The selected study has less than two samples, so the PCoA plot and the distribution of the Bray-Curtis distances cannot be created.', icon='⚠️')

elif eda_type == "Comparison between studies":
    # Title for the page
    st.markdown("<h3 style='text-align: center; color: black;'>Exploratory data analysis for comparison between studies</h3>", unsafe_allow_html=True)

    # Create a selectbox to choose the taxonomic rank
    tax_rank = st.selectbox(
        "Taxonomic Rank:",
        options=["Phylum", "Genus", "Species"]
    )

    # Create a df with study ids and biomes
    filt_columns = ['study_id', 'biome']
    studies_biomes = studies_data[filt_columns].drop_duplicates()
    studies_biomes = studies_biomes.dropna()

    # Show the df
    st.markdown("<h4 style='text-align: left; color: black;'>List of studies and their biomes</h4>", unsafe_allow_html=True)
    studies_biomes.columns = ['Study ID', 'Biomes']

    st.data_editor(
        studies_biomes,
        width = 1000,
        column_config={
            "widgets": st.column_config.TextColumn(
                help= f"List of studies and their biomes"
            )
        },
        hide_index=True,
    )

    # Make comparison between studies
    st.markdown(f"<h4 style='text-align: left; color: black;'>Comparison between studies at {tax_rank} level</h4>", unsafe_allow_html=True)

    # Create a selectbox to choose the two studies
    selected_studies = st.multiselect("Selected studies:", studies_biomes['Study ID'].unique())

    if len(selected_studies) == 0:
        st.write('Please select two studies')
    elif len(selected_studies) == 1:
        st.write('Please select another study')
    else:
        # Display summary for the selected studies
        st.subheader(f'Studies {selected_studies[0]} and {selected_studies[1]}')

        # Load data for the selected studies
        study1_info, sample1_info = utils.load_study_data(studies_data, selected_studies[0])
        study1_info = study1_info.T
        study1_info = study1_info.drop(index='study_id')
        study1_info.columns = [selected_studies[0]]

        study2_info, sample2_info = utils.load_study_data(studies_data, selected_studies[1])
        study2_info = study2_info.T
        study2_info = study2_info.drop(index='study_id')
        study2_info.columns = [selected_studies[1]]

        # Merge the study info dfs
        studies_info = pd.merge(study1_info, study2_info, left_index=True, right_index=True)

        # Replace indices and column names
        studies_info.index = ['Description', 'Bioproject ID', 'Centre name', 'Number of samples',
                        'Biome','Experiment type', 'Pipeline version', 'Instrument platform',
                        'Sampling country']
        
        st.data_editor(
        studies_info,
        width = 2000,
        column_config={
            "widgets": st.column_config.TextColumn(
                f"Summary {selected_studies[0]} and {selected_studies[1]}",
                help= f"Summary of the studies {selected_studies[0]} and {selected_studies[1]}"
            )
            },
            hide_index=False,
            )

        # Load and preprocess abundance tables for the selected studies and store in independent variables
        if tax_rank == 'Phylum':
            abund_table1 = utils.load_abund_table(selected_studies[0], tax_rank='phylum')
            abund_table1 = utils.preprocess_abund_table(abund_table1, tax_rank='phylum')
            abund_table2 = utils.load_abund_table(selected_studies[1], tax_rank='phylum')
            abund_table2 = utils.preprocess_abund_table(abund_table2, tax_rank='phylum')
        elif tax_rank == 'Genus':
            abund_table1 = utils.load_abund_table(selected_studies[0], tax_rank='genus')
            abund_table1 = utils.preprocess_abund_table(abund_table1, tax_rank='genus')
            abund_table2 = utils.load_abund_table(selected_studies[1], tax_rank='genus')
            abund_table2 = utils.preprocess_abund_table(abund_table2, tax_rank='genus')
        elif tax_rank == 'Species':
            abund_table1 = utils.load_abund_table(selected_studies[0], tax_rank='species')
            abund_table1 = utils.preprocess_abund_table(abund_table1, tax_rank='species')
            abund_table2 = utils.load_abund_table(selected_studies[1], tax_rank='species')
            abund_table2 = utils.preprocess_abund_table(abund_table2, tax_rank='species')

        # Add a row with the study ID for all samples in the current study
        study_id_row1 = pd.Series(selected_studies[0], index=abund_table1.columns)
        study_id_row2 = pd.Series(selected_studies[1], index=abund_table2.columns)

        # Add the study id row to the abundance table
        abund_table1 = pd.concat([pd.DataFrame([study_id_row1]), abund_table1])
        abund_table2 = pd.concat([pd.DataFrame([study_id_row2]), abund_table2])

        # Merge the abundance tables
        merged_df = pd.concat([abund_table1, abund_table2], axis=1)

        # Fill NaN values with 0
        merged_df = merged_df.fillna(0)

        # Transpose the DataFrame
        merged_df_transp = merged_df.T

        # Rename study_id column
        merged_df_transp = merged_df_transp.rename(columns={0: 'study_id'})

        # Extract the study_id column and remove it from the DataFrame
        study_ids = merged_df_transp['study_id']
        merged_df = merged_df_transp.drop(columns=['study_id'])

        # Create PcoA plot for the selected studies
        st.markdown(f"<h4 style='text-align: left; color: black;'>PCoA plot of samples from the {selected_studies[0]} and {selected_studies[1]} studies at {tax_rank} level using Bray-Curtis dissimilarity matrices</h4>", unsafe_allow_html=True)
        
        # Calculate Bray-Curtis dissimilarity matrix and preprocess sample info
        bc_mat, samples_df = utils.calculate_bray_curtis_dist(merged_df, 'comparison', tax_rank = tax_rank)
        
        # Show the PCoA plot
        pcoa_plot_comp = web_utils.plot_pcoa_stud_comp(bc_mat, merged_df, studies_data, study_ids)
        st.plotly_chart(pcoa_plot_comp, use_container_width=True)

        # Show the merged abundance table
        st.markdown(f"<h4 style='text-align: left; color: black;'>Abundance table for the {selected_studies[0]} and {selected_studies[1]} studies at {tax_rank} level</h4>", unsafe_allow_html=True)
        web_utils.display_dataframe_with_aggrid(merged_df)

        # Button to download the sample information as a CSV file
        sample_info_csv = utils.convert_df(merged_df)
        st.download_button(
            label=f"Download abundance table as CSV",
            data=sample_info_csv,
            file_name=f"Abund_table_{selected_studies[0]}_and_{selected_studies[1]}.csv",
            mime='text/csv',
        )

# Footer
with st.container():
    web_utils.footer()
