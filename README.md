
# Optimizing TPSA with the Ascent Bio API

## Background: Why Optimize TPSA?

The Ascent Bio model leverages deep learning and transformer-based methods to map molecular structures and SMILES sequences to properties like TPSA, logP, and more. Trained on datasets with millions of molecular variations, the model captures intricate relationships between structure and properties. It recommends precise, property-specific modifications while maintaining molecular integrity and drug-like characteristics.

Topological Polar Surface Area (TPSA) measures the polar surface area of a molecule, correlating with its ability to cross biological membranes. Molecules with low TPSA values (<140 Å²) often have better cell membrane permeability, enhancing oral bioavailability and blood-brain barrier penetration. Conversely, higher TPSA values can improve solubility. Optimizing TPSA enables tailored pharmacokinetics to align with specific therapeutic goals, balancing solubility and permeability.

---

## Step-by-Step Guide: Using the Ascent Bio API to Optimize TPSA

### Step 1: Define Your Starting Molecule

Start by identifying your molecule using its SMILES notation, e.g., `"CC(=O)OC1=CC=CC=C1C(=O)O"`. This molecule (acetylsalicylic acid, as just an example) serves as input to the API for TPSA optimization. Knowing the baseline TPSA value can help set realistic goals for adjustment.

---

### Step 2: Specify TPSA as the Target Property

Configure the API request to optimize TPSA:

- **`"target_props": ["TPSA"]`**: Specifies TPSA as the target property.
- **`"target_changes": [1]`**: Indicates increasing TPSA (use `[-1]` to decrease it).

For example:
- To enhance solubility, increase TPSA with `"target_changes": [1]`.
- For better membrane permeability, decrease TPSA with `"target_changes": [-1]`.

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
    "target_props": ["TPSA"],
    "target_changes": [1],  # Increase TPSA; use [-1] to decrease TPSA
    "model_id": "ascentbio-v1-base-large"
}

```

This code sends a POST request to the Ascent Bio API endpoint with your molecule’s SMILES string, optimization parameters, and your API key. The response will contain a modified SMILES string and updated property values for the molecule, showing how its TPSA has been adjusted.

### Interpreting the Results
Upon receiving the API response, review the optimized SMILES string and the reported TPSA value. If the TPSA has increased (or decreased) as specified, you can then assess whether this adjustment meets your design goals. For example, if your goal was to increase TPSA to enhance solubility, a significant increase should improve the compound’s interaction in aqueous environments. Alternatively, if you needed lower TPSA for enhanced membrane permeability, a reduction would signal that the molecule may now be more effective at crossing cell membranes or the blood-brain barrier.

This iterative process, powered by the Ascent Bio API, was designed to fine-tune TPSA and other properties efficiently, using the API’s robust search capability within an expansive chemical space. By optimizing TPSA, you can tailor your molecule’s properties to specific physiological and pharmacological needs, potentially enhancing therapeutic efficacy and safety profiles.
