# BookWise — Rule-Based Book Recommendation Expert System

A small AI laboratory mini-project using a curated CSV knowledge base and transparent IF–THEN rules.

## Run
1. Install Python 3.10+.
2. In this folder, run `pip install -r requirements.txt`.
3. Run `streamlit run app.py`.
4. Open the local URL shown in the terminal.

## Test
`python -m unittest discover -s tests -v`

## Rule weights
Genre 3; theme 2; reading level 2; length 1; mood/purpose 2. These are illustrative design choices. The percentage denominator includes only the weights of preferences the user supplied.

## Limitations
The dataset is small and manually curated; recommendation tags are educational classifications. The system uses no machine-learning training, feedback learning, live catalogue, or external service. Verify local execution before presenting.
