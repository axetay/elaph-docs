# User Manual Generation — Design Document

**Date:** 2026-04-18  
**Author:** Abdo Hassan

---

## Overview

Automatically generate a comprehensive HTML documentation site for two U-Go logistics modules by using a Playwright agent to browse each app, capture screenshots, and extract UI structure. Output is a MkDocs + Material theme site per module, both hosted in the same git repository.

---

## Modules

| Module | App Name | URL |
|--------|----------|-----|
| `garage/` | U-Go Garage Maintenance | https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance?frameorigin=https://one.zoho.com#Page:Fleet_Management_Dashboard |
| `trucking/` | U-Go Trucking Management System | https://creatorapp.zoho.com/m.fahwy_ugologistics/u-go-trucking-management-system?frameorigin=https://one.zoho.com |

---

## Target Audience

- **End users** — staff operating the app day-to-day
- **Admins** — users managing system configuration and settings

Both audiences are covered in every module, with dedicated sections for each.

---

## Browsing & Discovery Strategy

The Playwright agent will:

1. Start at the module's entry URL (Fleet Management Dashboard for Garage; root for Trucking)
2. For each page visited:
   - Take a full-page screenshot → saved to `<module>/docs/assets/screenshots/`
   - Extract: page title, section headings, form fields (label, type, required), buttons, table columns, navigation links
3. Follow every navigation link/menu item to discover sub-pages
4. Repeat for admin-only sections if accessible
5. Produce a structured JSON manifest of all discovered pages, fields, and actions

---

## Documentation Structure (per module)

```
<module>/
├── docs/
│   ├── index.md                    # Overview & getting started
│   ├── end-users/
│   │   ├── dashboard.md            # Entry page
│   │   └── [page-per-screen].md    # One file per discovered page
│   ├── admin/
│   │   ├── overview.md
│   │   └── [page-per-screen].md
│   └── assets/
│       └── screenshots/            # Playwright-captured PNGs
└── mkdocs.yml                      # Module-specific site config
```

Each page doc covers:
- Purpose of the page
- How to navigate to it
- Every field, button, and column with description
- Step-by-step workflows for common tasks

---

## Repository Structure

```
/
├── garage/                     # Module 1: U-Go Garage Maintenance
│   ├── docs/
│   └── mkdocs.yml
├── trucking/                   # Module 2: U-Go Trucking Management
│   ├── docs/
│   └── mkdocs.yml
├── requirements.txt            # Shared: mkdocs-material + dependencies
└── .github/
    └── workflows/
        └── deploy.yml          # Deploys both sites (GitHub Pages)
```

---

## Toolchain

- **Playwright** — browser automation for page discovery and screenshot capture
- **MkDocs** + **Material theme** — static site generator
- **Python** — scripting for manifest processing and doc generation
- **GitHub Pages** — deployment target (via `mkdocs gh-deploy`)

---

## Language

English only.

---

## Success Criteria

- Every page, form, field, button, and table in both apps is documented
- Every major screen has at least one screenshot
- Both MkDocs sites build without errors (`mkdocs build`)
- Navigation sidebar reflects the actual app structure
- End-user and admin sections are clearly separated
