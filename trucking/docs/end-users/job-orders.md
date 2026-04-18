# Job Orders

![Job Orders screenshot](../assets/screenshots/job-orders.png)

The Job Orders page lets you create and manage trucking jobs in the U-Go system. Operations staff use this form to record shipment details, assign contractors, and track routes. You'll fill this out each time you need to log a new transportation job or update an existing one.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system#Form:Job_Orders`

## How to Use

1. Click Add New or open an existing job order to begin
2. Enter the Job Order ID and select the Job Date when the work will occur
3. Choose the Work Type from the dropdown (for example: full container load, less-than-container load, or breakbulk)
4. Fill in shipping details: MBL No., Shipping Order No., and Number of Containers
5. Select the Client, Subcontractor, and Port Representative from their respective dropdowns
6. Enter the Origin and Destination locations, then specify the Border Crossing point if applicable
7. Upload any required supporting documents (commercial invoices, bills of lading, permits), then click Submit

## Page Sections

- Identification
- Parties
- Route & locations
- Scheduling
- Commercials
- Status

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Job Order ID |  | text | No |
| Job_Date |  | text | No |
| Work_Type | The type of freight service for this job (such as full container load, partial load, or special handling). Select from the dropdown list. | text | No |
| uploadFile |  | file | No |
| MBL No. | Master Bill of Lading number—the unique tracking number for the entire shipment from the shipping company. | text | No |
| Shipping Order No. | Your internal purchase order or shipping reference number for this job. | text | No |
| Number of Containers | The count of shipping containers (20ft or 40ft boxes) included in this job order. | text | No |
| Client | The company or customer requesting the trucking service. Select from the dropdown. | text | No |
| Subcontractor | The trucking company or driver assigned to perform this job. Select from approved subcontractors. | text | No |
| Port_Representative | The contact person or agent at the port or warehouse handling this shipment. | text | No |
| Origin1 | The starting location or pickup point for the shipment (warehouse, port, or facility name). | text | No |
| Route | The planned route or corridor for this shipment (optional but helpful for tracking and planning). | text | No |
| Border_Crossing | If this shipment crosses an international border, specify which crossing point will be used. | text | No |
| Destination1 | The final delivery location or destination for this shipment. | text | No |
| Distance (km) |  | text | No |
| Planned_Pickup_Date_Time |  | text | No |
| Planned_Delivery_Date_Time |  | text | No |
| Sell Rate In Price List |  | text | No |
| Special Sell Rate |  | text | No |
| Subcontractor Rate |  | text | No |
| Actual Sell Rate |  | text | No |
| Currency |  | text | No |
| Approved_By |  | text | No |
| Status |  | text | No |
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

- Always verify the Client and Subcontractor names are spelled correctly before submitting—these link to billing and contractor records.
- If you're working with multiple containers, confirm the container count matches your shipping documents to avoid discrepancies during customs clearance or delivery.

## Related Pages

- [All Job Orders](all-job-orders.md)
- [Import / Export Job Orders](import-export-job-orders.md)
- [Domestic Job Orders](domestic-job-orders.md)
- [Subcontractor Job Orders](subcontractor-job-orders.md)
- [Cross Border Job Orders](cross-border-job-orders.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
