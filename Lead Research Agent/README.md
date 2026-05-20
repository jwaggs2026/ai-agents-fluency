# Lead Research Agent

An n8n workflow that automates B2B lead validation, research, scoring, and CRM delivery — from form submission to a categorized Gmail alert.

## Overview

A lead is submitted via form, validated, researched, scored, formatted for CRM, and routed to a categorized email alert — all without manual intervention.

## Workflow Pipeline

### 1. Lead Submission Form
**Input fields:**
- Company Name
- Company URL
- LinkedIn URL
- Additional Context *(optional)*

### 2. Validation Agent
Uses **Claude + Tavily** to assess whether the submitted lead is legitimate, usable, and ready for downstream research. Filters out incomplete, duplicate, or low-quality submissions before any research is performed.

### 3. Research Agent
Uses **Tavily** to search the company website and LinkedIn profile, then uses **Claude** to extract and structure the data in preparation for scoring.

### 4. Scoring Agent
Uses **Claude** to evaluate the researched lead across four dimensions:
- **Business opportunity quality** — market fit, size, revenue potential
- **Operational fit** — alignment with internal capabilities and ICP
- **Outreach readiness** — contact clarity, timing, engagement signals
- **Enrichment completeness** — data coverage and confidence level

Produces a numeric or categorical score used for downstream routing.

### 5. CRM Formatting Agent
Uses **Claude** to convert the researched and scored lead data into a clean, standardized, CRM-ready record.

### 6. Google Sheets Append
The formatted CRM record is appended as a new row to a connected Google Sheet for record-keeping and review.

### 7. Email Routing (Switch)
The Google Sheet data is passed through a score-based Switch node that routes the lead to one of four Gmail alert templates:

| Score Category | Output |
|---|---|
| Hot Lead | Hot Lead Alert email |
| Warm Lead | Warm Lead Alert email |
| Needs Enrichment | Needs Enrichment Alert email |
| Cold Lead | Cold Lead Alert email |

## Tech Stack

| Tool | Role |
|---|---|
| n8n | Workflow orchestration |
| Claude | Validation, research formatting, scoring, CRM formatting |
| Tavily | Web and LinkedIn search |
| Google Sheets | CRM record storage |
| Gmail | Lead alert delivery |

## Input / Output Summary

**Input:** Lead submission form (Company Name, Company URL, LinkedIn URL, Additional Context)

**Output:** Categorized Gmail alert (Hot, Warm, Needs Enrichment, or Cold) + CRM row in Google Sheets
