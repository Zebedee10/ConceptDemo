# Technology Architecture App

Initial prototype for an enterprise Technology Architecture application.

## Prototype 1: Technology Taxonomy Explorer

The first page provides an interactive three-level taxonomy explorer:

- select a Level 1 taxonomy item;
- drill into its Level 2 categories;
- drill into its Level 3 categories;
- view the Level 3 description;
- view connected strategic technologies and their descriptions.

The prototype currently reads from `data/Sample_data.csv`.

The application is deliberately separated into:

- `app.py` — Streamlit user experience;
- `services/taxonomy_service.py` — taxonomy data access and domain logic;
- `data/Sample_data.csv` — temporary prototype data source.

This means the CSV can later be replaced by a LeanIX-backed service without redesigning the page.

## Run locally

Create and activate a virtual environment, install the requirements, then run:

```cmd
python -m streamlit run app.py
```
