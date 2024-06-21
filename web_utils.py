import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import colorcet as cc
from skbio.stats.ordination import pcoa
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from scipy.spatial.distance import squareform
import networkx as nx

def show_pages_menu(index=0) -> str:
    '''
    Shows a menu with the different pages of the app and returns the selected page.

    Parameters
    ----------
    index : int
        The index of the default page to be selected.

    Returns
    -------
    str
        The selected page.
    '''
    selected = option_menu(
    menu_title=None,  # required
    options=["Home", "Exploratory data analysis", "Microbial association networks", "Knowledge graph", "Case studies"],  # required
    icons=["house", "clipboard2-data", "asterisk", "database", "chat-text"],  # optional
    menu_icon="cast",  # optional
    default_index=index,  # optional
    orientation="horizontal",
    )
    return selected

def plot_histogram(data, column, x_title, y_title, nbins, color_palette) -> px.histogram:
    '''
    Plots a histogram of the provided data. It uses the Plotly library
    and it is meant to be used within a Streamlit app.

    Parameters
    ----------
    data : DataFrame
        The data to be plotted.
    column : str
        The column of the data to be plotted.
    x_title : str
        The title of the x-axis.
    y_title : str
        The title of the y-axis.
    nbins : int
        The number of bins to be used in the histogram.
    color_palette : list
        The color palette to be used in the histogram.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The histogram plot.
    
    Examples
    --------
    >>> hist_plot = plot_histogram(data, 'n_samples', 'Number of samples', 'Number of studies')
    >>> st.plotly_chart(hist_plot)
    '''
    hist_plot = px.histogram(data, x=column, nbins=nbins, opacity=0.8, color_discrete_sequence=color_palette)

    hist_plot.update_layout(
        xaxis=dict(title=x_title, tickfont=dict(size=18), titlefont=dict(size=20), dtick=10, tick0=0),
        yaxis=dict(title=y_title, tickfont=dict(size=18), titlefont=dict(size=20))
        ).update_xaxes(
            showgrid=False
        ).update_yaxes(
            showgrid=False)
    
    return hist_plot

def plot_pie(data, column, legend_title, color_palette) -> px.pie:
    '''
    Plots a pie chart of the provided data. It uses the Plotly library
    and it is meant to be used within a Streamlit app.

    Parameters
    ----------
    data : DataFrame
        The data to be plotted.
    column : str
        The column of the data to be plotted.
    legend_title : str
        The title of the legend.
    color_palette : list
        The color palette to be used in the pie chart.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The pie chart plot.
    
    Examples
    --------
    >>> pie_plot = pie_plot(data, 'biome')
    >>> st.plotly_chart(pie_plot)
    '''
    pie_plot = px.pie(values = data[column].value_counts(), names=data[column].value_counts().index, 
                      opacity=0.8, color_discrete_sequence=color_palette)
    

    pie_plot.update_traces(
        textposition='inside',
        textinfo='value',
        insidetextfont=dict(size=18)
        ).update_layout(
            legend_title=dict(text=legend_title, font=dict(size=24)),
            legend=dict(font=dict(size=20))
        )
    return pie_plot

def plot_bar(data, x_column, color_column, legend_title, x_title, y_title, color_palette) -> px.histogram:
    '''
    Plots a bar chart of the provided data. It uses the Plotly library
    and it is meant to be used within a Streamlit app.

    Parameters
    ----------
    data : DataFrame
        The data to be plotted.
    x_column : str
        The column to be plotted on the x-axis.
    color_column : str
        The column to be used for color grouping.
    color_palette : list
        The color palette to be used in the bar chart.
    x_title : str
        The title of the x-axis.
    y_title : str
        The title of the y-axis.
    legend_title : str
        The title of the legend.

    Returns
    -------
    plotly.graph_objects.Figure
        The bar chart plot.

    Examples
    --------
    >>> bar_plot = plot_bar(data, 'experiment_type', 'biome', px.colors.qualitative.Dark24, 'Experiment type', 'Number of studies', 'Biome')
    >>> st.plotly_chart(bar_plot)
    '''
    bar_plot = px.histogram(data, x=x_column, opacity=0.8, 
                            color=color_column, color_discrete_sequence=color_palette)

    bar_plot.update_layout(
        xaxis=dict(title=x_title, tickfont=dict(size=18), titlefont=dict(size=20)),
        yaxis=dict(title=y_title, tickfont=dict(size=18), titlefont=dict(size=20)),
        legend_title=dict(text=legend_title, font=dict(size=24)),
        legend=dict(font=dict(size=20)),
    ).update_xaxes(
        showgrid=False
    ).update_yaxes(
        showgrid=False)

    return bar_plot

def plot_two_pies(labels, values1, values2, title1, title2, legend_title, color_palette) -> go.Figure:
    '''
    Plots two pie charts side by side for the provided labels and values. 
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    labels : list
        The labels for the pie chart slices.
    values1 : list
        The values for the first pie chart.
    values2 : list
        The values for the second pie chart.
    title1 : str
        The title for the first pie chart.
    title2 : str
        The title for the second pie chart.
    legend_title : str
        The title of the legend.
    color_palette : list
        The color palette to be used in the pie charts.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The figure containing the pie charts.
    
    Examples
    --------
    >>> pie_plots = plot_two_pie(biomes, studies_per_biome, samples_per_biome, 
                           'Studies', 'Samples', 'Biomes', px.colors.qualitative.Dark24)
    >>> st.plotly_chart(pie_plots)
    '''
    # Create subplots
    pie_plots = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=[title1, title2])

    # Add the first pie chart
    pie_plots.add_trace(go.Pie(labels=labels, values=values1, name=title1,
                         marker=dict(colors=color_palette)), 1, 1)

    # Add the second pie chart
    pie_plots.add_trace(go.Pie(labels=labels, values=values2, name=title2,
                         marker=dict(colors=color_palette)), 1, 2)

    # Update layout
    pie_plots.update_layout(
        legend_title=dict(text=legend_title, font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )
    pie_plots.update_traces(textposition='inside', textinfo='value', insidetextfont=dict(size=18))

    return pie_plots

def plot_stacked_bar_allbiomes(abund_dfs, tax_dfs, biome_names, color_palette) -> px.bar:
    '''
    Plots a stacked bar chart for the top 5 species in each biome. 
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    abund_dfs : list
        List of abundance DataFrames for each biome.
    tax_dfs : list
        List of taxonomy DataFrames for each biome.
    biome_names : list
        List of names of the biomes.
    color_palette : list
        The color palette to be used in the bar chart.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The bar chart plot.
    
    Examples
    --------
    >>> fig = plot_stacked_bar(abund_dfs, tax_dfs, biome_names, px.colors.qualitative.Dark24)
    >>> st.plotly_chart(fig)
    '''
    # Initialize an empty DataFrame for the top 5 species data
    top_species_df_all_biomes = pd.DataFrame()

    # Process each biome
    for abund_df, tax_df, biome_name in zip(abund_dfs, tax_dfs, biome_names):
        # Merge the abundance and taxonomy dataframes by index
        abund_tax_merged = abund_df.merge(tax_df, left_index=True, right_index=True)
        abund_tax_merged.index = abund_tax_merged['Species']
        abund_tax_merged.drop(columns=['Superkingdom', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'], inplace=True)
        abund_tax_merged_transp = abund_tax_merged.T

        # Calculate top 5 species
        top_species = abund_tax_merged_transp.sum().nlargest(5)
        
        # Get total abundance for all species
        total_abundance = abund_tax_merged_transp.sum().sum()
        top_species_relative = (top_species / total_abundance) * 100

        temp_df = pd.DataFrame({
            'Biome': biome_name,
            'Species': top_species_relative.index,
            'Relative Abundance': top_species_relative.values
        })
        top_species_df_all_biomes = pd.concat([top_species_df_all_biomes, temp_df])

    # Create a stacked bar chart for the top 5 species in each biome
    bar_plot = px.bar(top_species_df_all_biomes, x='Biome', y='Relative Abundance', color='Species',
                      category_orders={"Species": top_species_df_all_biomes['Species'].unique()}, opacity=0.8,
                      color_discrete_sequence=color_palette)

    # Update layout
    bar_plot.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title='Biome',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        yaxis=dict(
            title='Relative abundance (%)',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return bar_plot, abund_tax_merged

def plot_stacked_bar_bybiome(abund_df, tax_df, study_ids) -> px.bar:
    '''
    Creates a stacked bar chart of the top 5 species for each study based on relative abundance.
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    abund_df : DataFrame
        Abundance DataFrame.
    tax_df : DataFrame
        Taxonomy DataFrame.
    study_ids : DataFrame
        DataFrame containing study IDs.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The stacked bar chart of the top 5 species.
    
    Examples
    --------
    >>> top_taxa_plot = plot_stacked_bar_bybiome(abund_df_species, tax_df_species, study_ids)
    >>> st.plotly_chart(top_taxa_plot, use_container_width=True)
    '''
    # Merge the abundance and taxonomy DataFrames by index
    abund_df_merged = abund_df.merge(tax_df, left_index=True, right_index=True)

    # Set "Species" column as index for the merged DataFrame
    abund_df_merged.index = abund_df_merged['Species']

    # Delete extra taxonomic columns
    abund_df_merged.drop(columns=['Superkingdom', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'], inplace=True)

    # Transpose the DataFrame
    abund_df_merged_transp = abund_df_merged.T

    # Add study_id back to the transposed DataFrame
    abund_df_merged_transp['study_id'] = study_ids

    # Initialize an empty DataFrame for the top 5 species data
    top_species_df = pd.DataFrame()

    # Loop over each study to find the top 5 species
    for study in abund_df_merged_transp['study_id'].unique():
        study_data = abund_df_merged_transp[abund_df_merged_transp['study_id'] == study]
        top_species = study_data.drop(columns='study_id').sum().nlargest(5)
        total_abundance = study_data.drop(columns='study_id').sum().sum()

        # Normalize the abundance for relative comparison
        top_species_relative = (top_species / total_abundance) * 100

        temp_df = pd.DataFrame({
            'Study': study,
            'Species': top_species_relative.index,
            'Relative Abundance': top_species_relative.values
        })
        top_species_df = pd.concat([top_species_df, temp_df])

    # Generate a palette with many unique colors and convert the colorcet palette to HEX format
    palette_hex = ['#' + ''.join([f'{int(c*255):02x}' for c in rgb]) for rgb in cc.glasbey_bw_minc_20]

    # Select colors based on the unique values of the species column
    unique_values_top_species = top_species_df["Species"].nunique()
    selected_palette_top_species = palette_hex[:unique_values_top_species]

    # Create a stacked bar chart for the top 5 species
    top_taxa_plot = px.bar(top_species_df, x='Study', y='Relative Abundance', color='Species',
                              category_orders={"Species": top_species_df['Species'].unique()}, opacity=0.8,
                              color_discrete_sequence=selected_palette_top_species)

    # Update layout to adjust the margin, if necessary, to ensure text is not cut off
    top_taxa_plot.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title='Study',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        yaxis=dict(
            title='Relative abundance (%)',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return top_taxa_plot, abund_df_merged

def plot_pcoa(bc_mat, samples_df, studies_data, color_option, legend_title, type_input_data, study_ids=None) -> px.scatter:
    '''
    Plots a PCoA plot for the provided Bray-Curtis dissimilarity matrix colored by various variables.
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    bc_mat : np.ndarray
        Bray-Curtis dissimilarity matrix.
    samples_df : DataFrame
        Preprocessed sample information DataFrame.
    studies_data : DataFrame
        DataFrame containing additional study data.
    color_option : str
        The variable to color by in the PCoA plot.
    legend_title : str
        The title for the legend in the PCoA plot.
    type_input_data : str
        Type of input data ('all_biomes', 'biome', 'study').
    study_ids : DataFrame, optional
        DataFrame containing study IDs (only needed for 'all_biomes' and 'biome' cases).
    
    Returns
    -------
    plotly.graph_objects.Figure
        The PCoA scatter plot.
    
    Examples
    --------
    >>> pcoa_plot = plot_pcoa(bc_mat, samples_df, studies_data, color_option, 'Legend Title', 'study')
    >>> st.plotly_chart(pcoa_plot)
    '''
    # Run PCoA
    bc_pcoa = pcoa(bc_mat)

    # Extract the data to plot the PCoA
    bc_pcoa_data = pd.DataFrame(data=bc_pcoa.samples, columns=['PC1', 'PC2'])

    # Reset index
    bc_pcoa_data = bc_pcoa_data.reset_index(drop=True)

    # Add analyses names as index
    bc_pcoa_data.index = samples_df['assembly_run_ids']

    if type_input_data in ['all_biomes', 'biome']:
        # Add study_id column to the PCoA DataFrame
        bc_pcoa_data['study_id'] = study_ids['study_id']

        # Merge additional columns from the studies_data
        additional_columns = ['biome', 'sampling_country', 'experiment_type', 'pipeline_version', 'instrument_platform']
        for column in additional_columns:
            bc_pcoa_data = bc_pcoa_data.merge(studies_data[['study_id', column]], on='study_id')

        if type_input_data == 'biome':
            # Add specific biome column to the PCoA DataFrame
            bc_pcoa_data['specific_biome'] = samples_df['biome']
            
            # If specific biome is "NA - NA", replace it with the general biome
            bc_pcoa_data['specific_biome'] = np.where(bc_pcoa_data['specific_biome'] == 'NA - NA', bc_pcoa_data['biome'], bc_pcoa_data['specific_biome'])

        # Change the pipeline version to a string column
        bc_pcoa_data['pipeline_version'] = bc_pcoa_data['pipeline_version'].astype(str)

        # Add biome in the study_id column
        bc_pcoa_data['study_id'] = bc_pcoa_data['study_id'].str.cat(bc_pcoa_data['biome'], sep=' - ')

    elif type_input_data == 'study':
        # Add the biome column directly to the PCoA DataFrame
        bc_pcoa_data['biome'] = samples_df['biome']

    # Get explained variance ratio
    explained_var_ratio = bc_pcoa.proportion_explained

    # Generate a palette with many unique colors and convert the colorcet palette to HEX format
    palette_hex = ['#' + ''.join([f'{int(c*255):02x}' for c in rgb]) for rgb in cc.glasbey_bw_minc_20]

    # Select colors based on the unique values of the selected variable
    unique_values_pcoa = bc_pcoa_data[color_option].nunique()
    selected_palette_pcoa = palette_hex[:unique_values_pcoa]

    # Modify experiment type column by adding upper case in the first letter if it exists
    if 'experiment_type' in bc_pcoa_data.columns:
        bc_pcoa_data['experiment_type'] = bc_pcoa_data['experiment_type'].str.capitalize()

    # Make the plot
    pcoa_plot = px.scatter(bc_pcoa_data, x='PC1', y='PC2', opacity=0.8, color=color_option,
                           hover_data=['study_id' if 'study_id' in bc_pcoa_data.columns else 'biome'], 
                           color_discrete_sequence=selected_palette_pcoa)

    # Add title and axis labels
    pcoa_plot.update_traces(
        marker=dict(size=7)
    ).update_layout(
        xaxis=dict(
            title=f'PCo1 ({explained_var_ratio[0]:.2%})',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        yaxis=dict(
            title=f'PCo2 ({explained_var_ratio[1]:.2%})',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(text=legend_title, font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return pcoa_plot

def plot_pcoa_stud_comp(bc_mat, abund_df, studies_data, study_ids) -> px.scatter:
    '''
    Plots a PCoA plot for the provided Bray-Curtis dissimilarity matrix, 
    colored by study ID and biome. It uses the Plotly library and is 
    meant to be used within a Streamlit app.

    Parameters
    ----------
    bc_mat : np.ndarray
        Bray-Curtis dissimilarity matrix.
    merged_df : DataFrame
        DataFrame containing the merged data.
    study_id : Series
        Series containing the study IDs.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The PCoA scatter plot.
    
    Examples
    --------
    >>> pcoa_plot = plot_pcoa_stud_comp(bc_mat, merged_df, study_id)
    >>> st.plotly_chart(pcoa_plot)
    '''
    # Run PCoA
    bc_pcoa = pcoa(bc_mat)

    # Extract the data to plot the PCoA
    bc_pcoa_data = pd.DataFrame(data=bc_pcoa.samples, columns=['PC1', 'PC2'])

    # Reset index
    bc_pcoa_data = bc_pcoa_data.reset_index(drop=True)

    # Transpose the abundance DataFrame
    abund_df_transp = abund_df.T
    
    # Add analyses names as index
    bc_pcoa_data.index = abund_df_transp.columns

    # Add study_id column to the PCoA DataFrame
    bc_pcoa_data['study_id'] = study_ids

    # Add biome column to the PCoA DataFrame
    bc_pcoa_data = bc_pcoa_data.merge(studies_data[['study_id', 'biome']], on='study_id')

    # Add biome in the study_id column
    bc_pcoa_data['study_id'] = bc_pcoa_data['study_id'].str.cat(bc_pcoa_data['biome'], sep=' - ')

    # Get explained variance ratio
    explained_var_ratio = bc_pcoa.proportion_explained

    # Create a plotly figure
    pcoa_plot = px.scatter(bc_pcoa_data, x='PC1', y='PC2', opacity=0.8, color='study_id', 
                           hover_data=['study_id'], color_discrete_sequence=px.colors.qualitative.Plotly)

    # Add title and axis labels
    pcoa_plot.update_traces(
        marker=dict(size=7)
    ).update_layout(
        xaxis=dict(
            title=f'PCo1 ({explained_var_ratio[0] * 100:.2f}%)',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        yaxis=dict(
            title=f'PCo2 ({explained_var_ratio[1] * 100:.2f}%)',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(text='Study ID - Biome', font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return pcoa_plot

def plot_distances_violins(bc_mat, study_ids) -> px.violin:
    '''
    Creates a violin plot of Bray-Curtis distances of studies in the provided matrix.
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    bc_mat : np.ndarray
        Bray-Curtis dissimilarity matrix.
    study_ids : np.ndarray
        Array of study IDs corresponding to the samples.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The violin plot of Bray-Curtis distances.
    
    Examples
    --------
    >>> violin_plot = create_violin_distances_plot(bc_mat, study_ids)
    >>> st.plotly_chart(violin_plot, use_container_width=True)
    >>> violin_plot.write_image("path_to_save_image.png", width=1500, height=750)
    '''
    # Initialize an empty DataFrame to store distances and corresponding study IDs
    distances_df = pd.DataFrame()

    # Loop over each unique study ID
    for study in np.unique(study_ids):
        # Get the indices of samples belonging to this study
        indices = np.where(study_ids == study)[0]

        # Extract the submatrix of distances for these samples
        submatrix = bc_mat[np.ix_(indices, indices)]

        # Convert the submatrix to a 1D array of distances
        dist_within = squareform(submatrix)

        # Filter out zero distances (self-comparisons)
        dist_within = dist_within[dist_within != 0]

        # Add these distances to the DataFrame
        temp_df = pd.DataFrame({'Distance': dist_within, 'Study': study})
        distances_df = pd.concat([distances_df, temp_df], ignore_index=True)

    # Create the violin plot for each study
    violin_plot = px.violin(distances_df, y='Distance', x='Study', box=True,
                            color='Study', color_discrete_sequence=px.colors.qualitative.Dark24)

    # Rotate x-axis labels to display them vertically
    violin_plot.update_layout(
        xaxis=dict(
            tickfont=dict(size=18),
            titlefont=dict(size=20)
        ),
        yaxis=dict(
            title='Bray-Curtis distance',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(text='Study', font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return violin_plot

def plot_distances_violin(bc_mat) -> px.violin:
    '''
    Plots a violin plot for the provided Bray-Curtis dissimilarity matrix.
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    bc_mat : np.ndarray
        Bray-Curtis dissimilarity matrix.
    
    Returns
    -------
    plotly.graph_objects.Figure
        The violin plot.
    
    Examples
    --------
    >>> violin_plot = plot_violin_br_curtis(bc_mat)
    >>> st.plotly_chart(violin_plot)
    '''
    # Convert the distance matrix to a 1D array of distances
    dist_within = squareform(bc_mat)

    # Filter out zero distances (self-comparisons)
    dist_within = dist_within[dist_within != 0]

    # Prepare data for violin plot
    data = {'Distance': dist_within}
    df_violin_plot = pd.DataFrame(data)

    # Create the violin plot
    violin_plot = px.violin(df_violin_plot, y='Distance', box=True, color_discrete_sequence=px.colors.qualitative.Plotly)

    # Add title and axis labels
    violin_plot.update_layout(
        yaxis=dict(
            title='Bray-Curtis Distance',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(text='Distance', font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return violin_plot

def plot_bar_top10taxa(abund_table, tax_rank) -> px.bar:
    '''
    Plots a bar plot for the top 10 most abundant taxa.
    It uses the Plotly library and is meant to be used within a Streamlit app.

    Parameters
    ----------
    abund_table : DataFrame
        Abundance DataFrame.
    tax_rank : str
        The taxonomic rank to use ('Phylum', 'Genus', 'Species').
    
    Returns
    -------
    plotly.graph_objects.Figure
        The bar plot.
    
    Examples
    --------
    >>> top10_plot = plot_top10_taxa(abund_table, 'Phylum')
    >>> st.plotly_chart(top10_plot)
    '''
    # Reset the index of the DataFrame, this will add the index as a new column
    abund_table_reset = abund_table.reset_index()

    # Remove the first row (which is the index)
    abund_table_reset = abund_table_reset.drop(abund_table_reset.index[0])

    if tax_rank == 'Phylum':
        # Now use the taxa column as id_vars in melt
        abund_table_top10 = abund_table_reset.melt(id_vars='phylum', var_name='assembly_run_ids', value_name='count')
        # Rename the column
        abund_table_top10 = abund_table_top10.rename(columns={'phylum': 'taxa'})
    elif tax_rank == 'Genus':
        abund_table_top10 = abund_table_reset.melt(id_vars='Genus', var_name='assembly_run_ids', value_name='count')
        abund_table_top10 = abund_table_top10.rename(columns={'Genus': 'taxa'})
    elif tax_rank == 'Species':
        abund_table_top10 = abund_table_reset.melt(id_vars='Genus_Species', var_name='assembly_run_ids', value_name='count')
        abund_table_top10 = abund_table_top10.rename(columns={'Genus_Species': 'taxa'})

    # Group by taxonomic rank and sum the counts
    abund_table_top10 = abund_table_top10.groupby('taxa').sum().reset_index()

    # Sort values by count
    abund_table_top10 = abund_table_top10.sort_values(by='count', ascending=False).reset_index(drop=True)

    # Keep only the top 10 most abundant taxa
    abund_table_top10 = abund_table_top10.head(10)

    # Create a bar plot to show the top 10 most abundant taxa
    top10_plot = px.bar(abund_table_top10, x="taxa", y='count', color_discrete_sequence=px.colors.qualitative.Plotly)

    # Add title and axis labels
    top10_plot.update_layout(
        xaxis=dict(
            title=f'{tax_rank}',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        yaxis=dict(
            title='Count',
            tickfont=dict(size=18),
            titlefont=dict(size=20),
            showgrid=False
        ),
        legend_title=dict(text='Count', font=dict(size=24)),
        legend=dict(font=dict(size=20))
    )

    return top10_plot

def display_dataframe_with_aggrid(df, pagination_page_size=15) -> None:
    '''
    Displays a DataFrame using AgGrid with configurable options.
    It is meant to be used within a Streamlit app.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to be displayed.
    pagination_page_size : int, optional
        The number of rows per page for pagination (default is 15).
    
    Examples
    --------
    >>> display_dataframe_with_aggrid(sample_info)
    '''
    builder = GridOptionsBuilder.from_dataframe(df)
    builder.configure_default_column(editable=True, groupable=True)
    builder.configure_side_bar(filters_panel=True, columns_panel=True)
    builder.configure_selection(selection_mode="multiple")
    builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=pagination_page_size)
    go = builder.build()

    AgGrid(df, gridOptions=go)

def load_and_preprocess_net(graphml_file, color_palette=px.colors.qualitative.Dark24, min_size = 6, max_size = 30) -> nx.Graph:
    """
    Loads and preprocesses a network graph from a GraphML file.

    Parameters
    ----------
    graphml_file : str
        The path to the GraphML file containing the graph data.
    color_palette : list, optional
        A list of colors to be used for different clusters in the graph. 
        Default is Plotly's 'Dark24' qualitative palette.
    min_size : int, optional
        The minimum size for nodes.
    max_size : int, optional
        The maximum size for nodes.

    Returns
    -------
    networkx.Graph
        The preprocessed NetworkX graph object.

    Examples
    --------
    >>> G = load_and_preprocess_net('data/graph.graphml)
    >>> nx.draw(G)
    """
    # Read the graph from the GraphML file
    G = nx.read_graphml(graphml_file)

    # Clean up edge attributes to avoid conflicts
    for u, v, data in G.edges(data=True):
        data.pop('source', None)
        data.pop('target', None)

    # Assign node labels as their IDs and obtain degree values
    degrees = {}
    for node, data in G.nodes(data=True):
        G.nodes[node]['label'] = G.nodes[node].get('name', node)

        # Obtain the degree of the node
        degree = data.get('degree', '0')
        try:
            # Add the degree to the dictionary
            degrees[node] = float(degree)
        except ValueError:
            degrees[node] = 0.0

    # Assign colors to clusters
    clusters = nx.get_node_attributes(G, 'cluster')
    unique_clusters = sorted(set(clusters.values()))
    color_map = {cluster: color_palette[i % len(color_palette)] for i, cluster in enumerate(unique_clusters)}

    # Calculate the min and max degree
    #degrees = dict(G.degree())
    min_degree = min(degrees.values())
    max_degree = max(degrees.values())

    # Assign node sizes and colors based on degree and cluster
    for node in G.nodes():
        degree = degrees[node]
        if degree == min_degree:
            size = min_size
        elif degree == max_degree:
            size = max_size
        else:
            size = min_size + (max_size - min_size) * ((degree - min_degree) / (max_degree - min_degree))
        
        G.nodes[node]['size'] = size
        G.nodes[node]['color'] = color_map.get(G.nodes[node].get('cluster'))  # Default to green if no cluster color

    return G

def load_and_preprocess_kg(graphml_file, node_colors, edge_colors, min_size = 10, max_size = 50) -> nx.Graph:
    """
    Loads and preprocesses a knowledge graph from a GraphML file, applying specific colors and border colors to nodes, 
    and specific colors to edges based on their labels. Also assigns node sizes based on precomputed betweenness centrality.

    Parameters
    ----------
    graphml_file : str
        The path to the GraphML file containing the graph data.
    node_colors : dict
        The color configuration dictionary for nodes.
    edge_colors : dict
        The color configuration dictionary for edges.
    min_size : int, optional
        The minimum size for nodes.
    max_size : int, optional
        The maximum size for nodes.

    Returns
    -------
    networkx.Graph
        The preprocessed NetworkX graph object.
    """
    # Read the graph from the GraphML file
    G = nx.read_graphml(graphml_file)

    # Extract betweenness centrality values from the graphml file
    betweenness = {}
    for node, data in G.nodes(data=True):
        raw_value = data.get('betweenness_centrality', '0')
        try:
            betweenness[node] = float(raw_value)
        except ValueError:
            betweenness[node] = 0.0

    # Get min and max betweenness centrality values
    min_betweenness = min(betweenness.values())
    max_betweenness = max(betweenness.values())

    # Assign colors, border colors, and sizes to nodes
    for node, data in G.nodes(data=True):
        label = data.get('labels', '')
        # Remove the ":" from the label
        label = label.split(':')[-1]
        if label in node_colors:
            data['color'] = node_colors[label]['color']
            data['border-color'] = node_colors[label]['border-color']
        
        # Assign size based on betweenness centrality
        betweenness_centrality = betweenness.get(node, 0)
        if betweenness_centrality == min_betweenness:
            size = min_size
        elif betweenness_centrality == max_betweenness:
            size = max_size
        else:
            size = min_size + (max_size - min_size) * ((betweenness_centrality - min_betweenness) / (max_betweenness - min_betweenness))
        data['size'] = size

    # Assign colors to edges based on their labels
    for u, v, data in G.edges(data=True):
        label = data.get('label', '')
        if label in edge_colors:
            data['color'] = edge_colors[label]['color']

    return G

def footer():
    st.write("Developed with data and annotations from:")

    cols = st.columns(5)
    with cols[0]:
        st.image('images/mgnify.svg', width=200)
    with cols[1]:
        st.image('images/midas_logo.svg', width=200)
    with cols[2]:
        st.image('images/kg-microbe.png', width=100)
    with cols[3]:
        st.image('images/NCBI-Logo.svg', width=75)
    with cols[4]:
        st.image('images/biolink-logo.png', width=100)

    st.markdown('The code for this project is available under the [MIT License](https://mit-license.org/) in this [GitHub repo](https://github.com/Multiomics-Analytics-Group/MicW2Graph). If you use or modify the source code or the outputs of this project, cite this work using the following DOI: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11394618.svg)](https://doi.org/10.5281/zenodo.11394618)')