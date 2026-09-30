# Architecture Governance Navigator — GitHub Copilot Repository Instructions

## Purpose of this file

This file gives GitHub Copilot the persistent repository context needed to work effectively on the **Architecture Governance Navigator** project.

Treat the information below as the current architectural intent and development conventions for this repository. Before making changes, inspect the relevant existing files and preserve established behaviour unless the user explicitly asks for a redesign.

---

# 1. Product purpose

The **Architecture Governance Navigator** is a Python / Streamlit proof of concept for digitising enterprise technology architecture guidance, governance and decision support.

The core proposition is:

> **Make the right architecture path easier to understand, follow and evidence.**

The longer-term ambition is:

> **Embed architecture guidance and governance into the way technology change is designed and delivered.**

The application is intended to bring together the interconnecting parts of technology governance so that analysis and decisions can become increasingly digital, traceable and reusable.

The intended target-state flow is:

**Enterprise facts → Architecture context → Explicit rules → AI assistance → Human decision → Enterprise knowledge**

Important design principles:

- Keep the experience document-light.
- Focus on decisions, risks, standards, patterns and outcomes.
- Separate facts, explicit rules and human judgement.
- AI is not the system of record.
- Deterministic logic should be used for explicit governance rules.
- AI assistance must be traceable and augment human decision-making.
- Humans remain accountable for architecture and governance decisions.
- Deliver iteratively; do not over-engineer the proof of concept.
- LeanIX is expected to become the authoritative source for architecture facts.
- The Navigator should become the insight / decision layer, not a duplicate system of record.

---

# 2. Current technology stack

Current proof-of-concept stack:

- Python
- Streamlit
- pandas
- Plotly
- `streamlit-plotly-events2`
- CSV files as temporary data sources

The current application is deliberately lightweight.

Do not introduce databases, APIs, microservices, FastAPI, queues or other infrastructure unless the user explicitly asks for them.

Future deployment is expected to be Azure-based, potentially using:

- Azure App Service or Azure Container Apps
- Microsoft Entra ID
- Azure Key Vault
- Azure Monitor / Application Insights
- Azure Database for PostgreSQL, if persistent application-owned workflow data is needed
- Azure OpenAI or another approved enterprise LLM capability

---

# 3. Repository structure

The current repository structure is conceptually:

```text
marcstechgov/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── components/
│   ├── __init__.py
│   ├── theme.py
│   └── ui.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── Sample_data.csv
│   ├── Sample_exceptions.csv
│   ├── Sample_adrs.csv
│   ├── Sample_change_portfolios.csv
│   ├── Sample_patterns.csv
│   ├── Sample_commercial_renewals.csv
│   └── Sample_commercial_division_roadmaps.csv
├── domain/
│   ├── __init__.py
│   └── models.py
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py
│   └── csv_repository.py
├── services/
│   ├── __init__.py
│   └── taxonomy_service.py
└── views/
    ├── __init__.py
    ├── taxonomy_page.py
    ├── exceptions_page.py
    ├── adr_page.py
    ├── change_portfolios_page.py
    ├── triage_page.py
    └── commercial_renewals_page.py
```

Generated folders such as `.venv/`, `__pycache__/` and `*.pyc` files are not part of the application source.

---

# 4. Logical architecture

The preferred architectural layering is:

```text
Presentation
    ↓
Application & Services
    ↓
Domain & Decision Logic
    ↓
Data & Repository
    ↓
Integration
    ↓
Platform & Infrastructure
```

Cross-cutting capabilities include:

- AI assistance / knowledge services
- security and identity
- logging and monitoring
- secrets management
- CI/CD
- human decision and governance

In the current POC this maps approximately to:

```text
app.py / views/*
        ↓
services/*
        ↓
domain models + explicit rules
        ↓
repository interfaces
        ↓
CSV repository today
        ↓
LeanIX / enterprise adapters later
```

The UI should not need to know whether data comes from CSV, LeanIX or another future system.

---

# 5. File responsibilities

## `app.py`

Role:

- Streamlit application shell
- page configuration
- dependency creation
- sidebar navigation
- routing between views
- query parameter handling where required

Current navigation concept:

```text
EXPLORE
  STL Lookup

CHANGE
  Change Portfolios

COMMERCIAL
  Commercial Renewals

GOVERN
  Governance Triage
  STL Exceptions
  Architecture Decisions
```

`app.py` should remain relatively thin.

Do not move business rules into `app.py`.

---

## `components/theme.py`

Role:

- shared Streamlit / CSS visual styling
- application theme conventions
- reusable style definitions

Keep visual changes centralised here where practical.

---

## `components/ui.py`

Role:

- shared UI helpers

Important helper:

```python
from textwrap import dedent
import streamlit as st

def render_html(content: str):
    st.html(dedent(content))
```

Use `st.html()` via `render_html()` for multiline custom HTML.

Do not revert multiline HTML to `st.markdown(..., unsafe_allow_html=True)` because indentation previously caused raw HTML to render incorrectly.

---

## `config/settings.py`

Role:

- application settings
- file paths
- configuration constants

Prefer centralised file paths here instead of scattering literal paths throughout the application.

---

## `domain/models.py`

Role:

- domain entities and data structures
- source-independent representation of taxonomy / technology concepts

Domain models should not contain Streamlit-specific code.

---

## `repositories/base_repository.py`

Role:

- repository interface / abstraction

The repository pattern exists specifically so CSV-backed data can later be replaced by enterprise sources such as LeanIX without redesigning the UI.

---

## `repositories/csv_repository.py`

Role:

- current CSV implementation of repository interfaces
- transforms CSV records into domain objects consumed by services

Keep CSV parsing details out of views.

Long-term direction:

```text
Repository interface
       ↓
LeanIX repository adapter
       ↓
LeanIX GraphQL / API
```

---

## `services/taxonomy_service.py`

Role:

- taxonomy navigation and application logic
- resolves paths between Level 1, Level 2 and Level 3
- returns taxonomy data to presentation views
- shields the UI from repository implementation details

Reusable taxonomy behaviour should live here rather than being duplicated between pages.

---

# 6. Current pages and behaviours

## `views/taxonomy_page.py`

Page title:

**STL Navigator**

Purpose:

Allow users to navigate the Strategic Technology List hierarchy and discover approved strategic technologies.

Current UX:

- Level 1 interactive Plotly donut / radial wheel
- Level 2 category buttons
- Level 3 category buttons
- selected Level 3 detail panel
- Strategic Technology cards
- search / autocomplete across categories and technologies
- governance status shown on the Level 1 wheel

### Level 1 governance state

Current POC status logic:

```python
LEVEL_1_STATUS = {
    "Tax_L1": "approved",
    "Tax_L2": "approved",
    "Tax_L3": "approved",
    "Tax_L4": "approved",
    "Tax_L5": "approved",
    "Tax_L6": "approved",
    "Tax_L7": "defining",
    "Tax_L8": "defining",
    "Tax_L9": "defining",
    "Tax_L10": "defining",
}
```

Approved domains use their assigned colour.

Domains still being defined use:

```python
DEFINING_COLOUR = "#D9DEE7"
```

Grey domains remain clickable.

For a defining domain the detail area shows:

> Strategic technologies still to be defined

The number of controls is not the point; governance status is presentation of enterprise-approved content.

Eventually domain approval status should come from authoritative data rather than a view-level dictionary.

### Level 1 wheel text

Long Level 1 names are supported.

Labels must:

- remain horizontal
- wrap over multiple lines when needed
- remain readable
- retain approximately the same font size
- not break click behaviour

The displayed label may contain HTML line breaks, but the real category ID remains the navigation key.

### Search behaviour

The STL Navigator includes an interactive search / autocomplete experience.

Search results should be concise.

Category result format:

```text
Cat: L1
Cat: L1 → L2
Cat: L1 → L2 → L3
```

Technology result format:

```text
Tech: Technology Name
```

Search rules:

- category search matches category names
- technology search matches technology names
- matching a category must NOT return every technology underneath that category
- selecting a category must navigate the wheel / L2 / L3 state to the selected path
- selecting a technology must navigate to its Level 3 category
- if a technology exists in multiple Level 3 categories, the user must be offered those category contexts so they can choose which one they mean
- search state should not repeatedly re-trigger the same navigation after rerun

Preserve this behaviour when editing the page.

---

## `views/exceptions_page.py`

Page title:

**STL Exceptions**

Purpose:

Navigate the same taxonomy while showing strategic technologies and associated exceptions side by side.

This is conceptually a governance-user capability rather than a broad lookup capability.

Exception cards should remain concise.

They show:

- exception technology
- exception status
- exception ID
- link to the associated ADR

Do not duplicate the full rationale from the ADR in the exception card.

The ADR is the authoritative decision record.

Current URL pattern for linking to an ADR:

```html
<a href="?page=Architecture%20Decisions&adr={adr_id}" target="_self">
```

---

## `views/adr_page.py`

Page title:

**Architecture Decision Records**

Purpose:

Display Architecture Decision Records and allow filtering by deciding authority.

Current deciding authorities:

- Enterprise Decision
- Division A
- Division B
- Division C

Typical statuses include:

- Approved
- Proposed
- Superseded

Cards show:

- ADR ID
- title
- summary
- status
- deciding authority
- decision date

If the page receives an `adr` query parameter, that ADR should be highlighted / surfaced first.

---

## `views/change_portfolios_page.py`

Purpose:

Show change initiatives grouped by managed change portfolio.

Current portfolio tabs:

- Enterprise Change Portfolio
- Division A
- Division B
- Division C

Each initiative contains:

- Portfolio
- Initiative ID
- Initiative Name
- Status
- Business Area
- Target Date

Typical statuses:

- In Delivery
- Mobilising
- Planned

The broader governance principle is that managed change should be linked to an agreed portfolio where possible.

---

## `views/triage_page.py`

Page title:

**Governance Triage**

Purpose:

Demonstrate a future deterministic governance assessment flow.

Current workflow:

### 1. Change Initiative

User selects a managed change initiative.

There is also an option that the change is not associated with managed change.

This represents a governance exception / consideration.

### 2. Technologies

User selects Strategic Technologies.

There is also an option that a technology outside the STL is required.

A non-strategic technology is expected to trigger:

- an exception
- EDA / appropriate governance approval

### 3. Architecture Patterns

Approved patterns associated with selected technologies are displayed / selected.

If no approved pattern applies, the project is expected to create / agree a pattern as part of architecture engagement.

### 4. Governance Position

The page summarises items such as:

- Managed Change
- Strategic Technology
- Approved Pattern
- EDA Approval Required / Not Currently Required

### 5. Generate Design Document

There is a prominent **Generate Design Document** concept action.

Today this is proof-of-concept behaviour only.

Future intent:

An approved enterprise LLM would consume change context, selected technologies, applicable patterns and governance context to draft initial design documentation for architect review.

The LLM must not make the final architecture decision.

---

## `views/commercial_renewals_page.py`

Page title:

**Commercial Renewals**

Purpose:

Provide architecture-informed commercial renewal decision support.

A contract can support multiple technologies and multiple consuming divisions.

A critical design principle is:

> A shared contract does not have one roadmap; it has consumer-specific roadmap positions.

The page shows:

- contract ID
- contract name
- supplier
- renewal date
- technologies
- consuming divisions
- Division Roadmaps
- indicative renewal guidance

For each consuming division, a roadmap can contain:

- roadmap status
- roadmap summary
- target exit date

If a division has not provided a roadmap, the POC presents an action such as:

```text
Raise JIRA Request — Division B
```

This currently displays a proof-of-concept message.

Future behaviour could create a real workflow request.

Long term, indicative renewal guidance should be derived from consolidated divisional roadmap positions rather than manually maintained.

---

# 7. Data files and current data contracts

## `data/Sample_data.csv`

Purpose:

Primary STL taxonomy and Strategic Technology dataset.

Current columns:

```text
Level 1
Level 2
Level 3
Level 3 Description
Strategic Technology
Strategic Technology Description
```

Examples use taxonomy identifiers such as:

```text
Tax_L1
Tax_L1.1
Tax_L1.1.1
Tech001
```

Do not assume taxonomy names will always be short.

The UI must tolerate realistic long category names.

---

## `data/Sample_exceptions.csv`

Purpose:

Illustrative STL exception data.

Columns:

```text
Exception ID
Level 1
Level 2
Level 3
Strategic Technology
Exception Technology
Status
ADR ID
```

The exception record links back to taxonomy context and an ADR.

---

## `data/Sample_adrs.csv`

Purpose:

Illustrative Architecture Decision Record data.

Columns:

```text
ADR ID
Title
Deciding Authority
Status
Decision Date
Summary
```

---

## `data/Sample_change_portfolios.csv`

Purpose:

Illustrative managed-change portfolio data.

Columns:

```text
Portfolio
Initiative ID
Initiative Name
Status
Business Area
Target Date
```

---

## `data/Sample_patterns.csv`

Purpose:

Illustrative approved architecture pattern data.

Columns:

```text
Pattern ID
Pattern Name
Strategic Technology
Description
```

Patterns are associated with Strategic Technologies.

---

## `data/Sample_commercial_renewals.csv`

Purpose:

Illustrative contract renewal data.

Columns include:

```text
Contract ID
Supplier
Contract Name
Renewal Date
Technologies
Consuming Divisions
Roadmap Status
Roadmap Summary
Target Exit Date
Indicative Renewal Guidance
```

Note:

The older single-roadmap fields may remain in the sample contract dataset, but the preferred conceptual model is divisional roadmaps.

---

## `data/Sample_commercial_division_roadmaps.csv`

Purpose:

Division-specific technology / contract roadmap positions.

Columns:

```text
Contract ID
Division
Roadmap Status
Roadmap Summary
Target Exit Date
```

This file represents the preferred roadmap model for shared contracts.

---

# 8. Key relationships

The most important relationships in the current concept are:

```text
Technology Domain
    ↓
Level 2 Category
    ↓
Level 3 Category
    ↓
Strategic Technology
```

A Strategic Technology can potentially appear in multiple Level 3 categories.

Therefore never assume:

```text
Strategic Technology → exactly one taxonomy path
```

Instead treat the relationship as potentially many-to-many / multiple-context.

Other important relationships:

```text
Change Initiative
    ↓
uses
Strategic Technology
    ↓
may map to
Architecture Pattern
```

```text
Exception
    ↓
relates to
Strategic Technology / taxonomy context
    ↓
is evidenced by
Architecture Decision Record
```

```text
Commercial Contract
    ↓
supports
Technology / Technologies
    ↓
consumed by
one or more Divisions
    ↓
each Division has
its own Roadmap Position
```

---

# 9. Governance logic principles

Explicit and deterministic governance logic should be implemented as normal Python business logic rather than delegated to an LLM.

Examples:

```text
Technology not on the STL
    → technology exception
    → governance approval required
```

```text
Change not associated with managed portfolio
    → governance exception / review
```

```text
No approved architecture pattern applies
    → architecture engagement required
    → create / agree a pattern
```

These are illustrative POC rules.

Do not invent new governance rules without explicit direction from the user.

---

# 10. AI design principles

AI is a future assistance capability, not the source of truth.

The intended AI role includes:

- explaining requirements
- summarising architecture context
- finding relevant precedent
- suggesting design options
- challenging designs
- drafting ADRs
- drafting design documentation
- generating explanatory artefacts

AI should consume:

- authoritative enterprise facts
- deterministic governance results
- approved standards and patterns
- previous decisions
- relevant change context

AI should not:

- fabricate enterprise facts
- silently override explicit governance rules
- make final approval decisions
- become the system of record

The intended pattern is:

```text
Authoritative facts
      ↓
Context assembly
      ↓
Explicit deterministic rules
      ↓
AI assistance
      ↓
Human judgement / decision
```

---

# 11. Future integrations

The target integration landscape includes:

## LeanIX

Expected future authoritative source for:

- enterprise architecture facts
- Strategic Technology List
- application information
- capability information
- technology lifecycle information
- relationships between architecture objects

The Navigator should query / consume LeanIX rather than recreate it.

## ServiceNow / JIRA

Potential roles:

- workflow
- actions
- approvals
- exceptions
- work requests
- governance tickets

Use whichever enterprise product is approved for the specific workflow.

## Confluence

Potential source for:

- standards
- architecture patterns
- reference architectures
- architecture knowledge
- supporting ADR content

## Change / Portfolio sources

Provide:

- managed change initiatives
- portfolio membership
- delivery status
- business areas
- target dates

## Procurement / Commercial sources

Provide:

- supplier contracts
- renewal dates
- consumption
- commercial information

## Enterprise LLM

Future approved AI capability.

The application should not make direct uncontrolled calls to consumer/public AI APIs.

---

# 12. Presentation conventions

The application should feel like an internal enterprise product rather than a developer demo.

Design style:

- clean white background
- dark navy headings
- muted blue / grey palette
- restrained use of colour
- rounded cards / panels
- compact executive-friendly wording
- low visual noise
- consistent spacing
- clear state and status indicators

Avoid:

- excessive explanatory copy
- technical jargon in the user experience
- decorative icons with no information value
- unnecessary breadcrumbs
- duplicated headings
- exposing internal implementation details to users

---

# 13. Coding conventions

When changing existing code:

1. Inspect the existing implementation before editing.
2. Preserve the current modular architecture.
3. Prefer small changes over rewrites.
4. Keep Streamlit presentation logic in `views/`.
5. Keep source / data access logic in repositories.
6. Keep orchestration / navigation logic in services.
7. Keep domain concepts independent from Streamlit.
8. Centralise configuration and paths where practical.
9. Reuse existing helpers rather than creating duplicates.
10. Do not introduce dependencies unless clearly necessary.

Python conventions:

- use descriptive function and variable names
- favour explicit readable code over clever compact code
- keep functions focused
- preserve type hints where already used
- avoid hidden global state except intentional Streamlit session state
- use `st.session_state` consistently for navigation state
- use `st.rerun()` only when required by the interaction model

---

# 14. Streamlit-specific conventions

### Custom HTML

Use:

```python
render_html(...)
```

which ultimately uses:

```python
st.html(dedent(content))
```

### Session state

Taxonomy navigation state currently uses concepts equivalent to:

```python
st.session_state.taxonomy_selected_l1
st.session_state.taxonomy_selected_l2
st.session_state.taxonomy_selected_l3
```

Any new interaction that changes taxonomy navigation must keep these values consistent.

### Plotly wheel

The Level 1 wheel uses:

```python
from streamlit_plotly_events2 import plotly_events
```

Typical configuration includes:

```python
config={
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": False,
    "responsive": True,
}
```

Preserve click interaction when changing wheel styling.

---

# 15. Navigation rules

When navigating directly to a taxonomy result:

### Level 1 selection

Set:

- selected L1
- a valid/default L2 for that L1
- a valid/default L3 for that L2

Use existing service methods where possible.

### Level 2 selection

Set:

- parent L1
- selected L2
- a valid/default L3

### Level 3 selection

Set:

- parent L1
- parent L2
- selected L3

### Technology search selection

Resolve the technology into one or more full taxonomy paths.

If one path:

- navigate directly to that L3 category

If multiple paths:

- ask the user which category context they mean
- navigate to the chosen path

Never infer one context if the technology is genuinely associated with multiple categories.

---

# 16. Current product capability model

The product concept is organised around four capabilities.

## NAVIGATE

Question:

> What should I know?

Includes:

- Strategic Technology
- Standards
- Patterns
- Reference architectures
- Previous decisions

## ASSESS

Question:

> What does this change mean?

Includes:

- Change / portfolio
- Applications
- Capabilities
- Dependencies
- Technology estate
- Applicable requirements

## GOVERN

Question:

> What governance is required?

Includes:

- Managed change
- Strategic technology
- Pattern compliance
- Standards
- Exceptions
- Governance route

## ASSIST

Question:

> How can I design and explain it?

Includes:

- explain requirements
- challenge designs
- suggest options
- find precedent
- draft ADRs / designs
- generate artefacts

Human decision sits beneath all four capabilities.

Decisions should become reusable enterprise knowledge.

---

# 17. Delivery roadmap

Conceptual roadmap:

## V1.0 — Navigate

- offline / curated STL data
- taxonomy navigator
- technology lookup

## V2.0 — Connect

- live LeanIX integration
- repository adapter replacing CSV source

## V3.0 — Context

- managed change portfolios
- initiative context
- broader enterprise context

## V4.0 — Govern

- governance triage
- patterns
- exceptions
- ADRs
- commercial decision support

## V5.0 — Assist

- LLM-enabled explanation
- design challenge
- context retrieval
- draft generation

Ultimate direction:

**Architecture Intelligence Platform**

Enterprise-aware reasoning across:

- architecture facts
- standards
- previous decisions
- roadmaps
- dependencies
- governance requirements

---

# 18. What Copilot should do before making changes

Before proposing or generating code:

- inspect the file(s) directly involved
- identify which layer owns the requested behaviour
- look for existing helper functions and service methods
- avoid duplicating logic
- preserve existing user-visible behaviour unless the request explicitly changes it
- flag any change that would require modifying multiple files
- explain material architectural trade-offs briefly

When asked to implement a feature, prefer a complete working change rather than partial pseudocode.

When the user asks for a replacement file, provide the full file rather than fragments.

---

# 19. What Copilot should not assume

Do not assume:

- CSV is the permanent architecture
- each technology belongs to one category
- each shared contract has one roadmap
- every governance decision belongs in AI
- the application owns enterprise architecture facts
- a database is required for the current POC
- authentication / production hosting is already implemented
- sample data is production data
- current POC governance rules are a complete enterprise policy model

---

# 20. Repository safety

This repository may be made public for the POC.

Therefore:

- never add credentials
- never add API tokens
- never add passwords
- never add real corporate secrets
- never add `.env` files
- never add Streamlit secrets
- never add sensitive enterprise exports
- never commit `.venv/`
- never commit `__pycache__/`
- treat the current CSV files as synthetic demonstrator data only

If adding an enterprise integration later, credentials must be supplied through approved secret-management mechanisms rather than source code.

---

# 21. Local development

Expected local workflow:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The original development environment used Python 3.14 and Streamlit 1.64.

Do not assume the local virtual environment should be copied between machines.

Recreate it from `requirements.txt`.

---

# 22. Mental model to retain

When deciding where new functionality belongs, use this model:

```text
User interaction
    ↓
View
    ↓
Application service
    ↓
Domain / deterministic rules
    ↓
Repository abstraction
    ↓
Authoritative data source
```

AI sits alongside this flow as an **assistance capability**, consuming trusted facts and rule outcomes.

It does not replace them.

The final accountability remains with people.

---

# 23. Current development priority

The current priority is a credible, useful internal concept demonstrator.

Optimise for:

- clarity
- maintainability
- demonstrable value
- realistic enterprise architecture concepts
- easy future replacement of sample data with live enterprise integrations

Do not optimise prematurely for:

- massive scale
- distributed systems
- complex cloud infrastructure
- speculative abstractions
- production-grade workflow engines

Keep the application simple enough to evolve quickly while maintaining clean architectural boundaries.
