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

## **About the project**
In this project, we investigated the microbiome of the **wastewater treatment** (WWT) process to build **MicW2Graph**, an open-source **knowledge graph** that integrates WWT metagenomic and metatranscriptomic information with their biological context, including biological processes, environmental and phenotypic features, chemical compounds, and additional metadata. We developed a workflow to collect meta-omics datasets from **MGnify** and infer potential interactions among microorganisms through **microbial association networks**. MicW2Graph enables the investigation of research questions related to WWT, focusing on aspects such as microbial connections, community memberships, and potential ecological functions.

The following figure shows the general workflow of the MicW2Graph project:
<p align="center">
<figure>
  <img src="./images/Methods_MicW2Graph.svg" alt="my alt text"/>
</figure>
</p>

## **Credits and Contributors**
- Developed by [Sebastián Ayala Ruano][myweb] under the supervision of [Dr. Alberto Santos][Alberto], head of the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- MicW2Graph was built for the thesis project from the [MSc in Systems Biology][sysbio] at the MoNA group.
- The data for this project was obtained from [Mgnify](https://www.ebi.ac.uk/metagenomics/api/latest/), using the scripts available in this [GitHub repository][retrieve_info_mgnify].

## **Contact**
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[sysbio]: https://www.maastrichtuniversity.nl/education/master/systems-biology
[myweb]: https://sayalaruano.github.io/
[Alberto]: https://orbit.dtu.dk/en/persons/alberto-santos-delgado
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[retrieve_info_mgnify]: https://github.com/Multiomics-Analytics-Group/Retrieve_info_MGnifyAPI
[Mgnify]: https://www.ebi.ac.uk/metagenomics/api/latest/
[issues]: https://github.com/Multiomics-Analytics-Group/MicW2Graph/issues/new





