# ClinicalTrials.gov Usage Guide

## Table of Contents

1. [Search by Condition/Disease](#1-search-by-conditiondisease)
2. [Search by Intervention/Drug](#2-search-by-interventiondrug)
3. [Geographic Search](#3-geographic-search)
4. [Search by Sponsor/Organization](#4-search-by-sponsororganization)
5. [Filter by Study Status](#5-filter-by-study-status)
6. [Retrieve Detailed Study Information](#6-retrieve-detailed-study-information)
7. [Pagination and Bulk Data Retrieval](#7-pagination-and-bulk-data-retrieval)
8. [Data Export to CSV](#8-data-export-to-csv)
9. [Extract and Summarize Study Information](#9-extract-and-summarize-study-information)
10. [Combined Query Strategies](#10-combined-query-strategies)

---

## 1. Search by Condition/Disease

Find trials studying specific medical conditions using the `query.cond` parameter.

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="type 2 diabetes",
    status="RECRUITING",
    page_size=20,
    sort="LastUpdatePostDate:desc"
)

print(f"Found {results['totalCount']} recruiting diabetes trials")
for study in results['studies']:
    protocol = study['protocolSection']
    nct_id = protocol['identificationModule']['nctId']
    title = protocol['identificationModule']['briefTitle']
    print(f"{nct_id}: {title}")
```

Use cases: rare diseases, comorbid conditions, tracking trial availability for specific diagnoses.

---

## 2. Search by Intervention/Drug

Search for trials testing specific interventions using the `query.intr` parameter.

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    intervention="Pembrolizumab",
    status=["RECRUITING", "ACTIVE_NOT_RECRUITING"],
    page_size=50
)

# Filter by phase in results
phase3_trials = [
    study for study in results['studies']
    if 'PHASE3' in study['protocolSection'].get('designModule', {}).get('phases', [])
]
print(f"Found {len(phase3_trials)} Phase 3 trials")
```

Use cases: drug development tracking, competitive intelligence, treatment option research.

---

## 3. Geographic Search

Find trials in specific locations using the `query.locn` parameter.

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="cancer",
    location="New York",
    status="RECRUITING",
    page_size=100
)

# Extract location details
for study in results['studies']:
    locations_module = study['protocolSection'].get('contactsLocationsModule', {})
    locations = locations_module.get('locations', [])
    for loc in locations:
        if 'New York' in loc.get('city', ''):
            print(f"{loc['facility']}: {loc['city']}, {loc.get('state', '')}")
```

Use cases: patient referrals to local trials, geographic distribution analysis, site selection.

---

## 4. Search by Sponsor/Organization

Find trials conducted by specific organizations using the `query.spons` parameter.

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    sponsor="National Cancer Institute",
    page_size=100
)

for study in results['studies']:
    sponsor_module = study['protocolSection']['sponsorCollaboratorsModule']
    lead_sponsor = sponsor_module['leadSponsor']['name']
    collaborators = sponsor_module.get('collaborators', [])
    print(f"Lead: {lead_sponsor}")
    if collaborators:
        print(f"  Collaborators: {', '.join([c['name'] for c in collaborators])}")
```

Use cases: institutional research portfolios, funding organization priorities, collaboration opportunities.

---

## 5. Filter by Study Status

Filter trials by recruitment or completion status.

```python
from scripts.query_clinicaltrials import search_studies

# Find recently completed trials with results
results = search_studies(
    condition="alzheimer disease",
    status="COMPLETED",
    sort="LastUpdatePostDate:desc",
    page_size=50
)

trials_with_results = [
    study for study in results['studies']
    if study.get('hasResults', False)
]

print(f"Found {len(trials_with_results)} completed trials with results")
```

---

## 6. Retrieve Detailed Study Information

Get comprehensive information about specific trials.

### Extract Eligibility Criteria

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
eligibility = study['protocolSection']['eligibilityModule']

print(f"Eligible Ages: {eligibility.get('minimumAge')} - {eligibility.get('maximumAge')}")
print(f"Eligible Sex: {eligibility.get('sex')}")
print(f"\nInclusion Criteria:")
print(eligibility.get('eligibilityCriteria'))
```

### Extract Contact Information

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
contacts_module = study['protocolSection']['contactsLocationsModule']

if 'centralContacts' in contacts_module:
    for contact in contacts_module['centralContacts']:
        print(f"Contact: {contact.get('name')}")
        print(f"Phone: {contact.get('phone')}")
        print(f"Email: {contact.get('email')}")

if 'locations' in contacts_module:
    for location in contacts_module['locations']:
        print(f"\nFacility: {location.get('facility')}")
        print(f"City: {location.get('city')}, {location.get('state')}")
        if location.get('status'):
            print(f"Status: {location['status']}")
```

---

## 7. Pagination and Bulk Data Retrieval

### Automatic Pagination

```python
from scripts.query_clinicaltrials import search_with_all_results

all_trials = search_with_all_results(
    condition="rare disease",
    status="RECRUITING"
)
print(f"Retrieved {len(all_trials)} total trials")
```

### Manual Pagination with Control

```python
from scripts.query_clinicaltrials import search_studies

all_studies = []
page_token = None
max_pages = 10

for page in range(max_pages):
    results = search_studies(
        condition="cancer",
        page_size=1000,
        page_token=page_token
    )
    all_studies.extend(results['studies'])

    page_token = results.get('pageToken')
    if not page_token:
        break

print(f"Retrieved {len(all_studies)} studies across {page + 1} pages")
```

---

## 8. Data Export to CSV

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="heart disease",
    status="RECRUITING",
    format="csv",
    page_size=1000
)

with open("heart_disease_trials.csv", "w") as f:
    f.write(results)

print("Data exported to heart_disease_trials.csv")
```

Note: CSV format returns a string instead of a JSON dictionary.

---

## 9. Extract and Summarize Study Information

```python
from scripts.query_clinicaltrials import get_study_details, extract_study_summary

study = get_study_details("NCT04852770")
summary = extract_study_summary(study)

print(f"NCT ID: {summary['nct_id']}")
print(f"Title: {summary['title']}")
print(f"Status: {summary['status']}")
print(f"Phase: {', '.join(summary['phase'])}")
print(f"Enrollment: {summary['enrollment']}")
print(f"Last Update: {summary['last_update']}")
print(f"\nBrief Summary:\n{summary['brief_summary']}")
```

---

## 10. Combined Query Strategies

Combine multiple filters for targeted searches.

```python
from scripts.query_clinicaltrials import search_studies

# Phase 2/3 immunotherapy trials for lung cancer in California
results = search_studies(
    condition="lung cancer",
    intervention="immunotherapy",
    location="California",
    status=["RECRUITING", "NOT_YET_RECRUITING"],
    page_size=100
)

phase2_3_trials = [
    study for study in results['studies']
    if any(phase in ['PHASE2', 'PHASE3']
           for phase in study['protocolSection'].get('designModule', {}).get('phases', []))
]

print(f"Found {len(phase2_3_trials)} Phase 2/3 immunotherapy trials")
```

---

## Helper Script Functions

`scripts/query_clinicaltrials.py` provides:

| Function | Description |
|----------|-------------|
| `search_studies()` | Search for trials with various filters |
| `get_study_details()` | Retrieve full information for a specific trial |
| `search_with_all_results()` | Automatically paginate through all results |
| `extract_study_summary()` | Extract key information for quick overview |

Run directly for example usage:

```bash
python3 scripts/query_clinicaltrials.py
```
