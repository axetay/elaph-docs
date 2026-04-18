# Driver Expenses & Wages Form

![Driver Expenses & Wages Form screenshot](../assets/screenshots/driver-expenses-wages-form.png)

The Driver Expenses & Wages Form records fuel costs, vehicle usage, and route details for individual driver assignments. Operations staff use this form to document job expenses and calculate driver compensation based on work type, distance, and fuel consumption. Complete this form after each job or delivery to maintain accurate payroll and cost records.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system#Form:Driver_Expenses_Wages_Form`

## How to Use

1. Select your language using the dropdown at the top if needed.
2. Enter or search for the Job Order number using the search field to auto-populate route and vehicle information.
3. Select the Work Type (domestic, subcontractor, or cross-border delivery) from the corresponding dropdown.
4. Enter the vehicle number, container number if applicable, and the destination type that matches your work type.
5. Input the distance traveled in kilometers and fuel consumption rate, and the system will calculate total fuel cost automatically.
6. Verify the driver name, truck source, and route name are correct.
7. Click Submit to save the expense record for payroll processing.

## Page Sections

- Identification
- Data From Job Order
- Balance Status
- Wages Calculation
- Subcontracted Vehicle Settlement
- Pay to Driver
- Pay to Subcontractor
- Cross Border Wages Calculation
- Domestic Wages Calculation
- Pay to Domestic Driver
- Cross Border Subcontracted Vehicle Settlement
- Driver Payment Status
- Approvals
- For Pivot Report

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Driver Expenses & Wages ID |  | text | No |
| Work_Type | Select whether this job is a domestic delivery, subcontractor assignment, or cross-border transport. This determines wage rates and expense categories. | text | No |
| Container_No | Enter the container or load number if this delivery involves a specific container. Leave blank if not applicable. | text | No |
| Domestic_Destination_Type | Select the destination category (city, port, warehouse, etc.) for domestic jobs only. | text | No |
| Subcontractor_Destination_Type | Select the destination category for work assigned through subcontractors. | text | No |
| Cross_Border_Destination_Type | Select the destination category for deliveries crossing national borders. | text | No |
| Job_Order | Search for and select the job order number. This links the expense to the correct billing and route record. | text | No |
| Job_Order_Date |  | text | No |
| Vehicle No. |  | text | No |
| Distance (km) | Enter the total distance traveled for this job. Measure from pickup to final drop-off point. | text | No |
| Fuel Consumption ( L / Km ) | Enter the truck's fuel consumption rate. This is typically provided by your fleet manager or calculated from recent tank fills. | text | No |
| Truck Source |  | text | No |
| Driver Name |  | text | No |
| Consumption Rate | This is the standard fuel cost per liter. The system uses this to calculate total fuel expenses. | text | No |
| Fuel Cost ( EGP ) | The system calculates this automatically based on distance, consumption rate, and fuel price. Verify the amount before submitting. | text | No |
| Route_Name | The route name auto-populates when you select a Job Order. Do not edit unless correcting an error. | text | No |
| Advance Amount |  | text | No |
| Fuel Price |  | text | No |
| #,###,###.## |  | text | No |
| uploadFile |  | file | No |
| All Driver Expenses |  | text | No |
| Balance |  | text | No |
| Yes |  | checkbox | No |
| Shipment_Container |  | text | No |
| Driver_Assistant |  | radio | No |
| Driver_Assistant |  | radio | No |
| Detention |  | radio | No |
| Detention |  | radio | No |
| Overnight_Fee |  | radio | No |
| Overnight_Fee |  | radio | No |
| Number of Overnights |  | text | No |
| Driver Fee |  | text | No |
| Driver Assistant Fee |  | text | No |
| Overnight Fees |  | text | No |
| Total Driver Wages |  | text | No |
| Destination |  | text | No |
| Driver Assistant Name |  | text | No |
| Rerouting |  | radio | No |
| Rerouting |  | radio | No |
| Rerouting Fee |  | text | No |
| Agreed Subcontracted Amount |  | text | No |
| Amount To Pay |  | text | No |
| Subcontractor Amount To Pay |  | text | No |
| Cross Border Driver Fee |  | text | No |
| Cross Border Driver Amount to Pay |  | text | No |
| Domestic_Driver_Assistant |  | radio | No |
| Domestic_Driver_Assistant |  | radio | No |
| Domestic Driver Assistant Name |  | text | No |
| Domestic Sell Rate |  | text | No |
| Domestic Driver Fee |  | text | No |
| Domestic Driver Assistant Fee |  | text | No |
| Domestic Total Driver Fees |  | text | No |
| Driver Wage % |  | text | No |
| Assistant Wage % |  | text | No |
| Domestic Driver Amount to Pay |  | text | No |
| Agreed Cross Border Subcontracted Amount |  | text | No |
| Cross Border Subcontractor Amount to Pay |  | text | No |
| Paid_Status |  | radio | No |
| Paid_Status |  | radio | No |
| Date_of_Payment |  | text | No |
| Garage_Supervisor_Approval |  | text | No |
| Finance_Audit_Approval |  | text | No |
| Final Driver Payable Amount |  | text | No |
| Driver Amount to Pay |  | text | No |
| Currency |  | text | No |
| submit |  | submit | No |
| reset |  | reset | No |
| searchmap |  | text | No |
| useIconSwitch |  | checkbox | No |
| toggleIconSwitch |  | checkbox | No |
| saveIcons |  | button | No |
| resetIcons |  | button | No |
| Search... |  | text | No |
| I have read the above conditions. |  | checkbox | No |
| reqEmailId |  | text | No |
| s2id_autogen2 |  | text | No |
| s2id_autogen2_search |  | text | No |
| supportType |  | dropdown | No |
| Please enable edit permission to help with troubleshooting |  | checkbox | No |
| reachusChatDescription |  | textarea | No |
| reachUsStartChat |  | button | No |

## Actions

- **Done**
- **Main Forms**
- **Master Data**
- **Expand**
- **Add New**
- **Submit**
- **Submit Request**

## Tips

- Always search for the Job Order first—this auto-fills most fields and reduces entry errors. Do not manually enter job details unless the order is not yet in the system.
- Double-check the Work Type and destination type match your actual assignment; selecting the wrong type will assign incorrect wage rates and may delay payment.

## Related Pages

- [Cash Advance Requests & Settlements](cash-advance-requests-settlements.md)
- [All Cash Advance Requests & Settlements](all-cash-advance-requests-settlements.md)
- [Open Cash Advances](open-cash-advances.md)
- [Unsettled Cash Advances](unsettled-cash-advances.md)
- [Driver Expenses & Wages Form Report](driver-expenses-wages-form-report.md)
- [Driver Unpaid Summary](driver-unpaid-summary.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
