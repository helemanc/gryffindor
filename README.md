# Draw Me Like Your Triples: Leveraging Generative AI for the Completion of Wikidata

This repository contains the code and resources for the research project "Draw Me Like Your Triples: Leveraging Generative AI for the Completion of Wikidata". The project was conducted by Raia Abu Ahmad, Martin Critelli, Şefika Efeoğlu, Eleonora Mancini, Célian Ringwald and Xinyue Zhang under the supervision of Prof. Albert Merono.

## Project Description
wip!
## Repository Structure
Folder Structure:
``` 
.
├── dataset                    --->  Dataset folder
│   ├── image-data 
│   │   ├── generated-data     ---> Generated images of the fictional characters
│   │   └── ground-truth       ---> Original images of the fictional characters
│   ├── prompt-data            ---> Prompts generated from raw-data.
│   ├── raw-data               ---> This directory contains the datasets created by querying Wikidata and DBpedia for fictional characters
│   └── unavailable_pic_ids    ---> Fictional characters with unaccessible images, but have an image property in the Wikidata KB
├── scripts                    ---> Bash scripts
└── src
    ├── data-preprocessing     ---> Data collection codes from DBpedia and Wikipedia, and ground truth image downloader
    ├── evaluation             ---> Result evaluation
    │   ├── evaluation-emotion
    │   └── evaluation-image-semantic
    ├── image-generator        ---> text (prompt) to image generator
    ├── notebooks              ---> visualization codes
    ├── prompt-generator       ---> prompt generation codes
    └── utils                  ---> read, write, download, and data loader functions
```
The repository is organized as follows:

- **data**: This directory contains the datasets created by querying Wikidata for fictional characters and enriching them with the prompts we generated.
- **data/images**: Each item present in the data has its own folder within this directory. Each folder contains four images: the ground truth image retrieved from Wikidata (if available) and the four images generated using DALL-E based on the corresponding prompts we created.
- **results**: This directory presents the results of our evaluation framework. It includes both a CSV and a JSON version of the analysis of prompts and their corresponding images.
- **src**: The source code required to obtain the data, build the dataset, and run the evaluation framework can be found in this directory.
- **src/utils**: This directory contains utility functions used for data retrieval, dataset construction, and building the evaluation framework.

## Usage

### 1.) Raw Data Collection
* Wikidata Dataset Creation
```bash
cd src/data-preprocessing
python wiki_query_service.py
```
* DBpedia Abstract Collection
```bash
cd src/data-preprocessing
python get_dbpedia_abstracts.py
```

### 2.) Prompt Generation

(wip)

### 3.) Ground Truth Image Collection
```bash
cd src/data-preprocessing
python ground_truth_image_collection.py
```
### 4.) Image Generation
```bash
cd src/image-generator
python image_generation.py
```
### 5.) Evaluation
* Image Semantic Evaluation

```bash
cd src/evaluation/evaluation-image-semantic
python evaluation_uqi.py
```
* Emotion Evaluation
```bash
cd src/evaluation/evaluation-emotion
python evaluation_emotion.py
```

## Contact

For any inquiries or further information regarding this research project, please feel free to reach out NAME(EMAIL).

We appreciate your interest in our work and hope that this repository proves useful to the research community.
