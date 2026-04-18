# Maintenance Order

![Maintenance Order screenshot](../assets/screenshots/maintenance-order.png)

The Maintenance Order page lets you create and manage vehicle maintenance records in the U-Go garage system. Operations staff use this page to log maintenance work, assign it to specific vehicles and drivers, and request spare parts needed for the job. You'll use this whenever a vehicle comes in for routine service or repairs.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance#Form:Maintenance_Order`

## How to Use

1. Select your preferred language using the dropdown at the top if needed.
2. Choose the vehicle that needs maintenance from the Vehicles dropdown.
3. Enter or select the driver's name associated with the vehicle.
4. Select the type of maintenance being performed (for example: oil change, tire rotation, inspection).
5. Enter today's date in the Maintenance Date field and record the current odometer reading in kilometers.
6. If spare parts are needed, click 'Add New' in the spare parts section and enter each part's details (model, part name, and quantity needed).
7. Click 'Submit' to save the maintenance order, or 'Submit Request' if you need manager approval for spare parts.

## Page Sections

- Vehicles Data
- Total Spare Parts Cost & Status

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Maintenance ID |  | text | No |
| zc-sel2-foc-Vehicles |  | text | No |
| zc-sel2-inp-Vehicles |  | text | No |
| Vehicles | Select the specific vehicle ID or plate number that requires maintenance. Use the dropdown to search if you have many vehicles. | text | No |
| zc-sel2-foc-Driver_Name |  | text | No |
| zc-sel2-inp-Driver_Name |  | text | No |
| Driver_Name | Enter or select the driver currently assigned to this vehicle. | text | No |
| zc-sel2-foc-Type_of_Maintenance |  | text | No |
| zc-sel2-inp-Type_of_Maintenance |  | text | No |
| Type_of_Maintenance | Choose from preset options like preventive maintenance, repairs, inspections, or emergency service. | text | No |
| Maintenance_Date |  | text | No |
| zc-sel2-foc-Type_of_Vehicle |  | text | No |
| zc-sel2-inp-Type_of_Vehicle |  | text | No |
| Type_of_Vehicle | Select the vehicle category (truck, van, car, etc.) — this may auto-fill based on your vehicle selection. | text | No |
| Current Odometer ( Km ) | Record the odometer reading in kilometers at the time of maintenance. This helps track service intervals. | text | No |
| zc-sel2-foc-Type_of_Scheduled_Maintenance |  | text | No |
| zc-sel2-inp-Type_of_Scheduled_Maintenance |  | text | No |
| Type_of_Scheduled_Maintenance | Indicate if this is routine scheduled service or unplanned maintenance. | text | No |
| SF(Request_Spare_Parts).FD(t::row_0_0).SV(record::status) |  | hidden | No |
| SF(Request_Spare_Parts).FD(t::row_0_0).SV(ID) |  | hidden | No |
| Request_Spare_Parts.t::row_0.Vehicle_Model |  | text | No |
| Request_Spare_Parts.t::row_0.Spare_Part_Needed |  | text | No |
| ####### |  | text | No |
| Request_Spare_Parts.t::row_0.Stock_Quantity |  | text | No |
| Request_Spare_Parts.t::row_0.Stock_Status |  | text | No |
| #######.## |  | text | No |
| ####### |  | text | No |
| Request_Spare_Parts.t::row_0.Notes |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| ####### |  | text | No |
| Request_Spare_Parts.t::row_0.Old_Spare_Part_Needed |  | text | No |
| #######.## |  | text | No |
| Request_Spare_Parts.t::row_0.Batch_1_Stock_ID |  | text | No |
| Request_Spare_Parts.t::row_0.Batch_2_Stock_ID |  | text | No |
| Request_Spare_Parts.t::row_0.Batch_3_Stock_ID |  | text | No |
| Request_Spare_Parts.t::row_0.Stock_Consumed |  | text | No |
| zc-sel2-foc-Maintenance_Status |  | text | No |
| zc-sel2-inp-Maintenance_Status |  | text | No |
| Maintenance_Status |  | text | No |
| Total Spare Parts Cost |  | text | No |
| Total Invoices Amount |  | text | No |
| Maintenance_End_Date |  | text | No |
| Maintenance Labor Hours |  | text | No |
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
| reachusChatDescription |  | textarea | No |
| reachUsStartChat |  | button | No |
| zc-reachus-editaccess-enable-button |  | button | No |
| zc-reachus-editaccess-revoke-button |  | button | No |
| zc-reachus-screenrecord-button |  | button | No |

## Actions

- **Done**
- **Main Forms**
- **Master Data**
- **Maintenance Sub Forms**
- **Spare Parts Sub Forms**
- **Support Forms**
- **Expand**
- **Add New**
- **Submit**
- **Submit Request**

## Tips

- Always record the odometer reading before submitting — this is critical for maintenance scheduling and warranty tracking.
- If you need spare parts that aren't in stock, use 'Submit Request' instead of 'Submit' so the approval workflow can process the order before work begins.

## Related Pages

- [All Maintenance Orders](all-maintenance-orders.md)
- [Repair Maintenance This Month](repair-maintenance-this-month.md)
- [Repair Details](repair-details.md)
- [All Repair Details](all-repair-details.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
