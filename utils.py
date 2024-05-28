import os
import glob
import yaml
import json
import requests
import gzip
import itertools
import zipfile
import networkx as nx
import pandas as pd
import streamlit as st
import numpy as np
from skbio.diversity import beta_diversity

# Function to load data from wwt studies
@st.cache_data
def load_studies_data(input_file) -> pd.DataFrame:
    '''
    Load the data from the waste water treatment studies and process it.

    Parameters
    ----------
    input_file : str
        Path to the input file with the data.
    
    Returns
    -------
    DataFrame
        The processed data from the waste water treatment studies.
    '''
    all_data = pd.read_csv(input_file)

    # Rename the entries in the biome column
    all_data['biome'] = all_data['biome'].replace({
        "root:Engineered:Wastewater:Nutrient removal:Biological phosphorus removal:Activated sludge": "root:Engineered:Wastewater:Activated Sludge",
        "root:Engineered:Wastewater:Nutrient removal:Dissolved organics (anaerobic)": "root:Engineered:Wastewater",
        "root:Engineered:Wastewater:Nutrient removal:Nitrogen removal": "root:Engineered:Wastewater",
        "root:Engineered:Wastewater:Industrial wastewater:Petrochemical": "root:Engineered:Wastewater:Industrial wastewater",
        "root:Engineered:Wastewater:Industrial wastewater:Agricultural wastewater": "root:Engineered:Wastewater:Industrial wastewater",
        "root:Engineered:Wastewater:Activated Sludge, root:Engineered:Wastewater:Industrial wastewater": "root:Engineered:Wastewater:Activated Sludge"
    })
    
    # Filter out the MGYS00005846 study from the df
    all_data = all_data[all_data['study_id'] != 'MGYS00005846']

    # Remove the "root:Engineered:" part of the biome column entries
    all_data["biome"] = all_data["biome"].str.replace("root:Engineered:", "")

    # Drop Unnamed columns
    all_data = all_data.drop(all_data.columns[all_data.columns.str.contains('unnamed',case = False)],axis = 1)

    return all_data

# Function to read yaml files
def read_yaml(yaml_file) -> dict:
    """
    Read the content of a yaml file and return it as a dictionary.

    Parameters
    ----------
    yaml_file : str
        Path to the yaml file to be read.
    
    Returns
    -------
    dict
        The content of the yaml file as a dictionary.
    """
    content = None
    with open(yaml_file, 'r') as stream:
        try:
            content = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise yaml.YAMLError("The yaml file {} could not be parsed. {}".format(yaml_file, err))
    return content

# Function to convert DataFrame to CSV
@st.cache_data
def convert_df(df) -> bytes:
    '''
    Convert a DataFrame to a CSV file.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    bytes
        The DataFrame converted to a CSV file.
    '''
    return df.to_csv(sep=',', header=True, index=False).encode('utf-8')

# Function to calculate the Bray-Curtis dissimilarity matrix
def calculate_bray_curtis_dist(abund_df, type_input_data, sample_info=None, tax_rank=None):
    '''
    Calculates the Bray-Curtis dissimilarity matrix for the provided abundance data and preprocesses the sample information.

    Parameters
    ----------
    abund_df : DataFrame
        Abundance DataFrame.
    sample_info : DataFrame
        DataFrame containing sample information.
    type_input_data : str
        Type of input data ('all_biomes', 'biome', 'study', 'comparison').
    
    Returns
    -------
    np.ndarray
        The Bray-Curtis dissimilarity matrix.
    DataFrame
        The preprocessed sample information DataFrame.
    
    Examples
    --------
    >>> bc_mat, samples_df = calculate_bray_curtis_dist(abund_df, sample_info, 'study')
    '''
    if type_input_data in ['all_biomes', 'biome']:
        id_var = 'OTU'
    elif type_input_data in ['study', 'comparison']:        
        # Set id_var based on the taxonomic rank available in the study data
        if tax_rank == 'Phylum':
            id_var = 'phylum'
        elif tax_rank == 'Genus':
            id_var = 'Genus'
        elif tax_rank == 'Species':
            id_var = 'Genus_Species'
    
    if type_input_data == 'comparison':
        # Extract analyses names as numpy arrays
        analyses_names = list(abund_df.index.values)

        # Convert abundance table to numpy array
        abund_table_merged_mat = abund_df.apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()

        # Obtain bray-curtis distance matrix
        bc_mat = beta_diversity("braycurtis", abund_table_merged_mat, analyses_names)

        # Replace NaN values with 0
        bc_mat = np.nan_to_num(bc_mat.data, nan=0.0)

        return bc_mat, None
    
    # Reshape the abundance DataFrame
    abund_df_reshaped = abund_df.reset_index().melt(id_vars=id_var, var_name='assembly_run_ids', value_name='count')

    # Split the multiple IDs in the assembly_run_ids column of sample_info
    sample_info['assembly_run_ids'] = sample_info['assembly_run_ids'].str.split(';')

    # Explode the DataFrame based on the assembly_run_ids column
    sample_info_exploded = sample_info.explode('assembly_run_ids')

    # Merge DataFrames on the 'assembly_run_ids' column
    samples_df = pd.merge(sample_info_exploded, abund_df_reshaped, left_on='assembly_run_ids', right_on='assembly_run_ids')

    # Filter the merged DataFrame to keep unique rows based on the assembly_run_ids column
    samples_df = samples_df.drop_duplicates(subset=['assembly_run_ids'])

    if type_input_data == 'biome':
        # Filter the merged DataFrame to keep only the relevant columns
        samples_df = samples_df[['assembly_run_ids', 'sample_id', 'biome_feature', 'biome_material']].reset_index(drop=True)

        # Combine biome_feature and biome_material columns if there is info on the columns, otherwise add 'NA'
        samples_df['biome_feature'] = samples_df['biome_feature'].fillna('NA')
        samples_df['biome_material'] = samples_df['biome_material'].fillna('NA')
        samples_df['biome'] = samples_df['biome_feature'] + ' - ' + samples_df['biome_material']

    # Sort DataFrame by assembly_run_ids
    samples_df = samples_df.sort_values(by=['assembly_run_ids']).reset_index(drop=True)

    # Transpose the DataFrame
    abund_df_transp = abund_df.T

    # Convert abundance table to numpy array
    abund_table_mat = abund_df_transp.to_numpy()

    # Obtain Bray-Curtis distance matrix
    bc_mat = beta_diversity("braycurtis", abund_table_mat, samples_df['assembly_run_ids'])

    # Replace NaN values with 0
    bc_mat = np.nan_to_num(bc_mat.data, nan=0.0)

    return bc_mat, samples_df

# Function to load data for a specific study
@st.cache_data
def load_study_data(all_data, selected_study):
    '''
    Load the data for a specific study.

    Parameters
    ----------
    all_data : DataFrame
        DataFrame containing all the data.
    selected_study : str
        The selected study to load the data for.
    
    Returns
    -------
    DataFrame
        The data for the selected study.
    DataFrame
        The sample information for the selected study.
    
    '''
    # Filter data for the selected study
    study_info = all_data[all_data['study_id'] == selected_study]
    
    # Load sample information for the study
    sample_info = pd.read_csv(f"data/EDA/Samples_metadata/{selected_study}/{selected_study}_samples_metadata.csv")
    
    return study_info, sample_info

# Function to load the abundance table for a specific study
@st.cache_data
def load_abund_table(selected_study, tax_rank):
    '''
    Load the abundance table for a specific study and taxonomic rank.

    Parameters
    ----------
    selected_study : str
        The selected study to load the abundance table for.
    tax_rank : str
        The taxonomic rank to load the abundance table for.
    
    Returns
    -------
    DataFrame
        The abundance table for the selected study and taxonomic rank.
    '''
    # Set the folder name 
    folder_path = f"data/EDA/Abundance_tables/{selected_study}/"

    # Broad pattern to initially match files
    broad_pattern = f"{selected_study}*taxonomy*.csv"
    file_list = glob.glob(os.path.join(folder_path, broad_pattern))

    if tax_rank == 'phylum':
        # Filtering for phylum taxonomy files
        filtered_files = [f for f in file_list if 'phylum_taxonomy' in f]
    elif tax_rank == 'genus':
        # Filtering for genus taxonomy files
        filtered_files = [f for f in file_list if 'genus_taxonomy' in f]
    elif tax_rank == 'species':
        # Filtering for species taxonomy files
        filtered_files = [f for f in file_list if 'species_taxonomy' in f]

    # Check if the filtered list is not empty
    if filtered_files:
        filename = filtered_files[0]  # Selecting the first matching file
        # Check if the file has more than one row
        if os.path.getsize(filename) <= 1:
            print(f"File '{filename}' for the study '{selected_study}' is empty.")
            return None
    else:
        print(f"No files found for the study '{selected_study}' in folder '{folder_path}'.")
        return None

    # Load abundance table for the study
    abund_table = pd.read_csv(filename, sep=',')
    
    return abund_table

# Function to preprocess abundance table for a specific study
def preprocess_abund_table(abund_table, tax_rank):
    '''
    Preprocess the abundance table for a specific taxonomic rank.

    Parameters
    ----------
    abund_table : DataFrame
        The abundance table to preprocess.
    tax_rank : str
        The taxonomic rank to preprocess the abundance table for.
    
    Returns
    -------
    DataFrame
        The preprocessed abundance table.
    '''
    # Delete rows with NANs in all columns
    abund_table = abund_table.dropna(how='all')
    if tax_rank == 'phylum':
        # Delete kingdom and superkingdom columns
        if 'superkingdom' in abund_table.columns:
            abund_table = abund_table.drop(columns=['superkingdom', 'kingdom'])
        else:
            abund_table = abund_table.drop(columns=['kingdom'])
    
        # Set the phylum column as index
        abund_table = abund_table.set_index('phylum')
    
    elif tax_rank == 'genus':
        # Delete extra taxonomic columns
        # Check available taxonomic levels and drop the corresponding columns
        taxonomic_levels = ['Superkingdom', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Family_Genus']
        for level in taxonomic_levels:
            if level in abund_table.columns:
                abund_table = abund_table.drop(columns=level)
        
        # Set the genus column as index
        abund_table = abund_table.set_index('Genus')

    elif tax_rank == 'species':
        # Delete extra taxonomic columns
        # Check available taxonomic levels and drop the corresponding columns
        taxonomic_levels = ['Superkingdom', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
        for level in taxonomic_levels:
            if level in abund_table.columns:
                abund_table = abund_table.drop(columns=level)
        
        # Set the genus column as index
        abund_table = abund_table.set_index('Genus_Species')

    return abund_table

def export_graph(G, filename, format, output_dir):
    '''
    Export a networkx graph to a file.

    Parameters
    ----------
    G : nx.Graph
        The networkx graph to export.
    filename : str
        The name of the file to export the graph to.
    format : str
        The format to export the graph to ('graphml', 'edgelist', 'cytoscape').
    output_dir : str
        The directory to export the graph to.
    
    Examples
    --------
    >>> export_graph(G, 'network.graphml', 'graphml', 'data')
    '''
    file_path = os.path.join(output_dir, filename)
    if format == "graphml":
        nx.write_graphml_lxml(G, file_path)
    elif format == "edgelist":
        nx.write_edgelist(G, file_path)
    elif format == "cytoscape":
        cytoscape_data= nx.cytoscape_data(G)
        with open(file_path, 'w') as out:
            out.write(json.dumps(cytoscape_data))

def load_html_file(file_path):
    """
    Loads the contents of an HTML file.

    Parameters
    ----------
    file_path : str
        The path to the HTML file.

    Returns
    -------
    str
        The contents of the HTML file as a string.

    Examples
    --------
    >>> html_content = load_html_file('file.html')
    >>> print(html_content)
    """
    html_data = ""
    with open(file_path, 'r', encoding='utf-8') as HtmlFile:
        html_data = HtmlFile.read()
    
    return html_data


def read_config(filepath, field=None):
    """
    Read the configuration file and return either the full content or an specific field.
    
    :param str filepath: path to configuration file
    :param str field: field to be obtained from the configuration
    
    :return: dictionary with the content of the configuration or the field specified
    """
    content = read_yaml(filepath)
    if content is not None:
        if field is not None:
            if field in content:
                return content[field]

    return content

def download_file(url, data_dir='data'):
    """
    Download file from an url into an existing directory
    :param str url: URL address where to download the data from
    :param str data_dir: path to directory where to download the data
    :return: filepath to the downloaded data
    """
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    filename = url.split('/')[-1]
    filename = os.path.join(data_dir, filename)
    if not os.path.isfile(filename):
        r = requests.get(url, headers=header)
        with open(filename, 'wb') as out:
            out.write(r.content)
            
    return filename

def read_gzipped_file(filepath):
    """
    Opens an underlying process to access a gzip file through the creation of a new pipe to the child.
    :param str filepath: path to gzip file.
    :return: A bytes sequence that specifies the standard output.
    """
    handle = gzip.open(filepath, "rb")

    return handle

def read_zipped_file(filepath):
    '''
    Opens a handler to access the content of zip file
    :param str filepath: path to the zip file
    :return: A bytes sequence that specifies the standard output
    '''
    file_name = filepath.split('/')[-1].split('.')[0]+'.tsv'
    archive = zipfile.ZipFile(filepath, 'r')
    handle = archive.open(file_name)

    return handle

def merge_dict_of_dicts(dict_of_dicts):
    dictionary = {}
    for d in dict_of_dicts:
        dictionary.update(dict_of_dicts[d])
        
    return dictionary
    
def merge_list_of_lists(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))