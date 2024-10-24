<h1 align="center">
    MicW2Graph
</h1>

<p align="center">
    <a href="https://github.com/Multiomics-Analytics-Group/MicW2Graph/blob/main/LICENSE">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/bioregistry" />
    </a>
    <a href="https://zenodo.org/doi/10.5281/zenodo.11394618">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.11394618.svg" alt="DOI">
    </a>
    <a href="https://micw2graph.streamlit.app/" title="MicW2Graph">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
</p>

<p align="center">
   Building a knowledge graph of the wastewater treatment microbiome and its biological context
</p>

## **Table of contents:**
- [About the project](#about-the-project)
- [Data](#data)
- [Exploratory data analysis](#exploratory-data-analysis)
- [Microbial associarion networks](#microbial-association-networks)
- [MicW2Graph](#micw2graph)
- [Case studies](#case-studies)
- [How to run the web app locally?](#how-to-run-the-web-app-locally)
- [Credits and Contributors](#credits-and-contributors)
- [Contact](#contact)

## **About the project**
**Wastewater treatment** (WWT) is the process of removing contaminants from used water before it is discharged back into the environment, which contributes to address water scarcity and to protect aquatic ecosystems. Recent advances in high-throughput omics technologies have facilitated the study of **microbiomes** from complex environmental samples such as WWT. A comprehensive study of an environmental microbiome requires integrating data from various studies and meta-omics technologies, as well as biological knowledge to interpret these data.

In this project, we investigated the microbiome of the WWT process to build **MicW2Graph**, an open-source **knowledge graph** that integrates metagenomic and metatranscriptomic information with their biological context, including biological processes, environmental and phenotypic features, chemical compounds, and additional metadata. We developed a workflow to collect meta-omics datasets from [MGnify][Mgnify] and infer potential interactions among microorganisms through **microbial association networks**. MicW2Graph enables the investigation of research questions related to WWT, focusing on aspects such as microbial connections, community memberships, and potential ecological functions.

The following figure shows the general workflow of the MicW2Graph project:
<p align="center">
<figure>
  <img src="./images/Methods_MicW2Graph.svg" alt="Methods MicW2Graph"/>
</figure>
</p>

## **Data**
WWT meta-omics studies were queried from the MGnify API using experiment type and biome parameters. Further filters were applied based on experimental and taxonomic criteria. The abundance tables from the filtered studies were then grouped by biome and experiment type to infer microbial association networks. The workflow for retrieving and filtering WWT meta-omics studies from MGnify is summarized in the diagram below:
<p align="center">
<figure>
  <img width="450px" src="./images/Funnel_filtering_MGnifystudies.svg" alt="MGnify studies filtering"/>
</figure>
</p>

The code to retrieve the data from MGnify is available in this [GitHub repository][retrieve_info_mgnify].

## **Exploratory data analysis**
A general overview of the filtered studies was provided through various plots, describing the number of studies and samples, experiment types, sampling countries, sub-biomes, and other relevant metadata.The exploratory data analysis was encapsulated in a module of the MicW2Graph web application, containing a general overview of all studies, studies by sub-biomes, individual studies, and a section for conducting pairwise comparisons between studies.
<p align="center">
<figure>
  <img src="./images/EDA_MicW2Graph.gif" alt="EDA MicW2Graph"/>
</figure>
</p>

## **Microbial association networks**
MANs are weighted and undirected networks, defined as *G = (V, E)*, where *V* is a set of nodes and *E* is a set of edges. Nodes in these networks are Operational Taxonomic Units at a specific taxonomic level, while edges indicate substantial co-presence (positive interaction) or mutual exclusion (negative interaction) trends in microorganism abundances across samples. Weights in MANs correspond to association values among species defined by the inference method, and there is an edge between two nodes if this number is greater than or equal to a given cutoff *t*. 

In this project, we selected the Correlation inference for [Compositional data through Lasso (CCLasso)][CCLasso] method. Network inference was conducted using the [NetCoMi][NetCoMi] R package. The MANs for this study are available for download and visualization in the MicW2Graph web application.
<p align="center">
<figure>
  <img src="./images/MANs_MicW2Graph.gif" alt="EDA MicW2Graph"/>
</figure>
</p>

The code for the network inference and analysis of MANs is available in this [GitHub repository][net_inf_analysis].

## **MicW2Graph**
MicW2Graph incorporates the MANs with the optimal association threshold for each WWT sub-biome and experiment type, the biological context of the species within the MANs, and ontologies that standardize and expand the information of this resource. This KG comprises 1247 nodes and 9749 relationships, categorized into 12 node labels and 8 relationship labels. The relationships in MicW2Graph are classified as taxonomic, functional, and data-driven, reflecting the different layers of knowledge available in the KG.

The MicW2Graph metagraph and a snapshot of the graph database with nodes and edges for all sub-biomes and experiment types are shown below:
<p align="center">
<figure>
  <img src="./images/MicW2Graph_metagraph_fig_horiz.svg" alt="MicW2Graph metagraph"/>
</figure>
</p>

The KG and sub-biome subgraphs are available for download and visualization in the MicW2Graph web application.
<p align="center">
<figure>
  <img src="./images/Kg_MicW2Graph.gif" alt="MicW2Graph metagraph"/>
</figure>
</p>

## **Case studies**
The use cases demonstrate the potential of MicW2Graph to discover new species associated with WWT biological processes, showing how the available information of well-known species can help to predict potential functions and traits for less studied species. These species and communities can be further investigated as potential candidates to optimize the bioremediation process. The subgraphs for the case studies can be visualized and downloaded in the MicW2Graph web application.
<p align="center">
<figure>
  <img src="./images/Case_studies_MicW2Grpah.gif" alt="Case studies MicW2Graph"/>
</figure>
</p>

## **How to run the web app locally?**
[Pyenv][Pyenv] and [Poetry][Poetry] were used to create a Python virtual environment, which allows the management of python libraries and their dependencies. Each Poetry virtual environment has a `pyproject.toml` file with the names and versions of libraries installed, and a `poetry.lock` file, a JSON file that contains versions of libraries and their dependencies.

To create a Python virtual environment with libraries and dependencies required for this project, you should install Pyenv and Poetry, create a Python virtual environment with the **3.11** version of Python, clone this GitHub repository, open a terminal, move to the folder containing this repository, and run the following commands:

```bash
# Activate 3.11.0 version of Python
$ pyenv local 3.11.0

# Create the Python virtual environment with Poetry
$ poetry install

# Activate the Python virtual environment 
$ poetry shell
```

You can find a detailed guide on how to use Poetry [here][Poetry-doc].

Alternatively, you can create a conda virtual environment with the required libraries using the `requirements.txt` file.

After installing the libraries, you can run the streamlit app locally with the command below:

```bash
$ streamlit run MicW2Graph_Home.py
```

## **Credits and Contributors**
- Developed by [Sebastián Ayala Ruano][myweb] under the supervision of [Dr. Alberto Santos][Alberto], head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- MicW2Graph was built for the thesis project from the [MSc in Systems Biology][sysbio] at the MoNA group.
- The data for this project was obtained from [Mgnify][Mgnify], using the scripts available in this [GitHub repository][retrieve_info_mgnify].

## **Contact**
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[CCLasso]: https://github.com/huayingfang/CCLasso
[NetCoMi]: https://github.com/stefpeschel/NetCoMi
[net_inf_analysis]: https://github.com/Multiomics-Analytics-Group/Microbial_network_inference_and_analysis_MicW2Graph
[Pyenv]: https://github.com/pyenv/pyenv
[Poetry]: https://python-poetry.org/
[Poetry-doc]: https://python-poetry.org/docs/basic-usage/
[sysbio]: https://www.maastrichtuniversity.nl/education/master/systems-biology
[myweb]: https://sayalaruano.github.io/
[Alberto]: https://orbit.dtu.dk/en/persons/alberto-santos-delgado
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[retrieve_info_mgnify]: https://github.com/Multiomics-Analytics-Group/Retrieve_info_MGnifyAPI
[Mgnify]: https://www.ebi.ac.uk/metagenomics/api/latest/
[issues]: https://github.com/Multiomics-Analytics-Group/MicW2Graph/issues/new





