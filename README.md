# Draw Me Like Your Triples: Leveraging Generative AI for the Completion of Wikidata

This repository contains the code and resources for the research project "Draw Me Like Your Triples: Leveraging Generative AI for the Completion of Wikidata". The project was conducted by Raia Abu Ahmad, Martin Critelli, Şefika Efeoğlu, Eleonora Mancini, Célian Ringwald and Xinyue Zhang under the supervision of Prof. Albert Merono.

## Repository Structure

The repository is organized as follows:

- **data**: This directory contains the datasets created by querying Wikidata for fictional characters and enriching them with the prompts we generated.
- **data/images**: Each item present in the data has its own folder within this directory. Each folder contains four images: the ground truth image retrieved from Wikidata (if available) and the four images generated using DALL-E based on the corresponding prompts we created.
- **results**: This directory presents the results of our evaluation framework. It includes both a CSV and a JSON version of the analysis of prompts and their corresponding images.
- **src**: The source code required to obtain the data, build the dataset, and run the evaluation framework can be found in this directory.
- **src/utils**: This directory contains utility functions used for data retrieval, dataset construction, and building the evaluation framework.

## Usage

To replicate our experiments or use our code, please refer to the individual directories mentioned above. The `src` directory contains the main codebase, while the `data` and `images` directories hold the relevant datasets and generated images. The `results` directory provides the outcome of our evaluation framework.

## Contact

For any inquiries or further information regarding this research project, please feel free to reach out NAME(EMAIL).

We appreciate your interest in our work and hope that this repository proves useful to the research community.
