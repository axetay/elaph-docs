"""
Defines the logical section groupings for each app's pages.
Used by enrich_manifest.py and generate_docs.py.
"""

GARAGE_HIERARCHY = [
    {
        "section": "Overview",
        "pages": ["Fleet Management Dashboard"],
    },
    {
        "section": "Maintenance Management",
        "description": "Create and track vehicle maintenance orders, repairs, and service history.",
        "pages": [
            "Maintenance Order",
            "All Maintenance Orders",
            "Repair Maintenance This Month",
            "Repair Details",
            "All Repair Details",
        ],
    },
    {
        "section": "Spare Parts",
        "description": "Manage spare parts inventory, stock levels, transactions, and requests.",
        "pages": [
            "All Spare Parts",
            "Spare Part Stock",
            "All Spare Part Stocks",
            "Spare Part Transactions",
            "All Spare Part Transactions",
            "Request Spare Parts",
            "Request Spare Parts Report",
        ],
    },
    {
        "section": "Procurement",
        "description": "Raise and track purchase orders for parts and supplies.",
        "pages": [
            "Purchase Orders",
            "All Purchase Orders",
            "Auto PO Items",
            "All Auto PO Items",
        ],
    },
    {
        "section": "Fuel Management",
        "description": "Record fuel consumption, analyse vehicle fuel efficiency, and track costs.",
        "pages": [
            "Fuel Control",
            "All Fuel Controls",
            "Fuel Entries",
            "All Fuel Entries",
            "Fuel \u2013 Vehicle Performance Summary",
            "Worst Vehicles Report",
            "Cost Per KM",
        ],
    },
    {
        "section": "Fleet & Drivers",
        "description": "Manage vehicle records, driver profiles, and driver KPI evaluations.",
        "pages": [
            "Vehicles",
            "All Vehicles",
            "Vehicles Summary Report",
            "All Drivers",
            "Driver KPI Evaluation",
            "All Driver Kpi Evaluations",
        ],
    },
    {
        "section": "Vehicle Fleet Reports",
        "description": "Per-vehicle detailed reports grouped by fleet category (M1–M4).",
        "pages": [
            "M1 Truck Report",
            "M1 Flat Bed Trailer Report",
            "M1 Boxed Trailer Report",
            "M1 Reefer Trailer Report",
            "M2 Truck Report",
            "M2 Flat Bed Trailer Report",
            "M2 Boxed Trailer Report",
            "M2 Reefer Trailer Report",
            "M3 Truck Report",
            "M3 Flat Bed Trailer Report",
            "M3 Boxed Trailer Report",
            "M3 Reefer Trailer Report",
            "M4 Truck Report",
            "M4 Flat Bed Trailer Report",
            "M4 Boxed Trailer Report",
            "M4 Reefer Trailer Report",
        ],
    },
    {
        "section": "Automation",
        "description": "Configure automation rules that trigger actions based on system events.",
        "pages": [
            "Automation Control",
            "All Automation Controls",
        ],
    },
]

TRUCKING_HIERARCHY = [
    {
        "section": "Overview",
        "pages": ["UGO Trucking Dashboard"],
    },
    {
        "section": "Job Orders",
        "description": "Create and manage trucking job orders across all transport types.",
        "pages": [
            "Job Orders",
            "All Job Orders",
            "Import / Export Job Orders",
            "Domestic Job Orders",
            "Subcontractor Job Orders",
            "Cross Border Job Orders",
        ],
    },
    {
        "section": "Shipments",
        "description": "Record shipment details linked to job orders for each transport type.",
        "pages": [
            "Shipment Details",
            "All Shipment Details",
            "Domestic Shipment Details",
            "All Domestic Shipment Details",
            "Subcontractor Shipment Details",
            "All Subcontractor Shipment Details",
            "Cross Border Shipment Details",
            "All Cross Border Shipment Details",
        ],
    },
    {
        "section": "Finance",
        "description": "Manage driver cash advances, expense settlements, and wage records.",
        "pages": [
            "Cash Advance Requests & Settlements",
            "All Cash Advance Requests & Settlements",
            "Open Cash Advances",
            "Unsettled Cash Advances",
            "Driver Expenses & Wages Form",
            "Driver Expenses & Wages Form Report",
            "Driver Unpaid Summary",
        ],
    },
    {
        "section": "Master Data",
        "description": "Reference data for clients, vendors, locations, routes, and port representatives.",
        "pages": [
            "Port Representatives Master Data Report",
            "Clients Master Data Report",
            "Vendors Master Data Report",
            "All Locations Master Data",
            "Routes Master Data",
            "Routes Master Data Report",
            "Driver Trip Allowances Master Data",
            "Driver Trip Allowances Master Data Report",
        ],
    },
]

HIERARCHIES = {
    "garage": GARAGE_HIERARCHY,
    "trucking": TRUCKING_HIERARCHY,
}
