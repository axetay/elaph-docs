# Repair Details

![Repair Details screenshot](../assets/screenshots/repair-details.png)

The Repair Details page is where you record information about vehicle repairs performed at your service centers. You'll use this form after a repair is completed to document what was fixed, who did the work, and how much it cost. This creates a maintenance record for your fleet management and invoicing.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance#Form:Repair_Details`

## How to Use

1. Select the type of repair from the Repair_Type dropdown (for example: engine repair, brake service, or tire replacement).
2. Enter a clear description of the problem in the Problem Description field so future technicians understand what was wrong.
3. Choose the repair category that best matches the work performed using the Repair_Category dropdown.
4. Enter the mechanic's name and the service center name where the repair was completed.
5. Record the invoice amount from your service center bill or receipt.
6. Upload any supporting documents such as invoices or work orders using the file upload field.
7. Check the acknowledgment checkbox at the bottom and click Submit to save the repair record.

## Page Sections

- Repair Basic Info
- Repair Execution
- In-house Garage
- External Service Center

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Repair_Type | Select the main type of repair performed (examples: engine, transmission, suspension, electrical, brakes). This helps you track which systems need the most maintenance. | text | No |
| Problem Description | Write a brief explanation of what was wrong with the vehicle and what symptoms it showed. Be specific so mechanics can reference this in the future. | textarea | No |
| Repair_Category | Choose a category that groups similar repairs together (examples: preventive maintenance, emergency repair, routine service). This helps you analyze maintenance patterns. | text | No |
| Repair_Done_By | Specify whether the work was completed by your in-house mechanic or an external service center. | text | No |
| Mechanic Name | Enter the full name of the person who performed the repair. | text | No |
| Service Center Name | Enter the name of the garage or service facility where the work was done. | text | No |
| Invoice Amount | Enter the total cost of the repair including labor and parts, as shown on the invoice. | text | No |
| uploadFile | Attach a scan or photo of the invoice, receipt, or work order as proof of the repair and expense. | file | No |
| submit |  | submit | No |
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
| reachusChatDescription | If you need support or have questions about the repair, describe your issue here and a support specialist will contact you. | textarea | No |
| reachUsStartChat |  | button | No |

## Actions

- **Done**
- **Main Forms**
- **Master Data**
- **Maintenance Sub Forms**
- **Spare Parts Sub Forms**
- **Support Forms**
- **Submit**
- **Submit Request**

## Tips

- Always keep your invoice or receipt handy when filling out this form so you enter the correct amount and can upload the document immediately.
- Be detailed in the Problem Description field—vague descriptions like 'car broken' make it hard for future reference and can cause confusion about warranty claims or repeat issues.

## Related Pages

- [Maintenance Order](maintenance-order.md)
- [All Maintenance Orders](all-maintenance-orders.md)
- [Repair Maintenance This Month](repair-maintenance-this-month.md)
- [All Repair Details](all-repair-details.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
