# Data Augmentation using Datagen

## Why use Datagen?

The Datagen tool is a component of the Ascent Bio API useful for exploring and expanding chemical space around a given molecule or set of molecules. Whether you’re performing a virtual screen, preparing for an experimental assay, or generating training data for machine learning models, Datagen enables you to create a diverse library of molecules for downstream small-molecule design goals. By generating molecular variants that share structural similarities with your input molecule (e.g., share a common chemical scaffold), Datagen provides a rich dataset for screening or training purposes while ensuring chemical diversity and relevance.

Datagen works by leveraging an internal framework that integrates chemical space together to better explore the structure-property relationships. The tool analyzes the structural features of a molecule and systematically generates chemically meaningful modifications, such as adding, substituting, or removing functional groups. These changes are designed to explore adn examine areas of chemical space around a molecule of interest. In addition it can be used to generate molecules in effort to retain drug-like properties while introducing diversity or searchign for candidates with tuned properties. Whether for virtual screening to identify hits or creating data for model pre-training, Datagen provides a fast and easy way to effectively leverage learned chemical strucutre-property patterns.

Here’s a step-by-step guide to using Datagen to expand chemical space around a molecule:

---

## Step 1: Define the Input Molecule
The first step is to select the molecule you want to use as the starting point for chemical space expansion, by providing its SMILES string. For instance, if your input molecule is "CC(=O)OC1=CC=CC=C1C(=O)O", this will serve as the seed structure. Datagen will generate a library of molecules based on this starting point, applying systematic modifications while giving you the control to determine how many molecules to be generated and how far into chemical space to reach. 


You can control key aspects of the expansion, such as:

Scaffold: Specify a substructure or scaffold to ensure generated molecules retain key functional groups.

Number of Molecules: Define the number of variants (num_outputs) you want to generate.


---

## Step 2: Send the Request and Analyze Results


Here’s an example API request:

```
python
import requests

url = "[https://api.ascentbio.xyz/v1/design](https://ascentbio--ab-datagen-v1-inference.modal.run/generate)"
headers = {
    "Content-Type": "application/json",
    "ascent-api-key": "<your-api-key>"
}
data = {
    "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
	 "scaffold": "CCCC",
	 "num_outputs": "100"
}


response = requests.post(url, json=data, headers=headers)
molecule_library = response.json()
print(molecule_library)

```
---

## Step 3: Analyze the Results

The API response will return a JSON object containing a list of generated molecules - in this case 100 molecules were generated that were similar to the seed input molecule and (optionally) retained the scaffold of that same original molecule. Each output molecule is represented by its SMILES string and may include calculated properties, such as molecular weight, logP, and TPSA. These properties can help you evaluate the generated molecules for your specific application. 

This code sends a POST request to the Ascent Bio API endpoint with your molecule’s SMILES string, optimization parameters, and your API key. The response will contain a modified SMILES string and updated property values for the molecule, showing how its TPSA has been adjusted.

### Step 4: Iterate and Refine
Ultimately, Datagen allows for iterative chemical space exploration and subsetting to a particular region of chemical space of interest. If the initial library doesn’t fully meet your needs, you can modify parameters such as the scaffold, diversity, or input molecule and generate a new library within seconds. This iterative approach ensures you can thoroughly explore relevant chemical space for your application, leading to better results in virtual screening, experimental campaigns, or model training.
