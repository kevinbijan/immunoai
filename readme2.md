# Multi-Property Optimization with the Ascent Bio API

## Why Multi-Property Optimization?

Multi-property optimization is a key challenge in small-molecule drug design. Molecules often need to balance conflicting properties to achieve therapeutic efficacy and safety. For example, optimizing molecular solubility (logP) while improving drug-likeness (QED) requires fine-tuning chemical structures without compromising other attributes. The Ascent Bio API enables this precision, offering computational tools to guide molecular design across multiple properties.

---

## Goal: Decrease logP and Increase QED

Lowering logP (partition coefficient) improves a molecule's solubility and reduces lipophilicity, which can lead to better bioavailability. Increasing QED (quantitative estimate of drug-likeness) ensures the molecule maintains favorable characteristics for drug development. Together, these modifications can enhance pharmacological performance while addressing solubility and drug-likeness constraints.

---

## Step-by-Step Guide: Using the Ascent Bio API

### Step 1: Define Your Starting Molecule

Start by identifying your molecule using its SMILES notation, e.g., `"CC(=O)OC1=CC=CC=C1C(=O)O"`. This molecule serves as input to the API for multi-property optimization. 

---

### Step 2: Specify Two Properties Simultaneously as the Target Properties.

Configure the API request to optimize both properties simultaneously:

For example:
- To enhance druglikeness, increase QED.
- For better solubility, decrease LogP.

These settings guide the API to explore viable structural variations that align with drug-like properties.

---

### Step 3: Send the Request and Analyze Results


Here’s an example API request:

```
python
import requests

url = "https://api.ascentbio.xyz/v1/design"
headers = {
    "Content-Type": "application/json",
    "ascent-api-key": "<your-api-key>"
}
data = {
    "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "changes": {"MolLogP": "decrease", 
               "qed": "increase"}
}

```

This code sends a POST request to the Ascent Bio API endpoint with your molecule’s SMILES string, optimization parameters, and your API key. The response will contain a modified SMILES string and updated property values for the molecule, showing how its TPSA has been adjusted.

### Interpreting the Results
Upon receiving the API response, review the optimized SMILES string and the reported property values.Evaluate the output to verify whether (1) logP has decreased and (2) QED has increased: Reflects enhanced drug-likeness and overall suitability for therapeutic use. For example, a molecule with decreased logP and increased QED is more likely to exhibit favorable solubility while maintaining or improving its efficacy as a drug candidate.

Together, this multi-property approach enables a controlled optimization of two properties of interest in parallel. 
