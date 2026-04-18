# Domestic Shipment Details

![Domestic Shipment Details screenshot](../assets/screenshots/domestic-shipment-details.png)

The Domestic Shipment Details page lets you record and manage all information for a domestic trucking shipment in U-Go's system. Dispatchers and operations staff use this page to log shipment cargo, assign vehicles and drivers, and track costs. Complete this form when you receive a new domestic job order or need to update an existing shipment.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system#Form:Domestic_Shipment_Details`

## How to Use

1. Select or enter the Job Order number to link this shipment to an existing order.
2. Choose the Destination Type (such as single location, multiple stops, or hub delivery) to specify where the cargo is going.
3. Select the Domestic Shipment Type to classify the shipment (for example, full truck load, less than truck load, or partial load).
4. Enter the goods description and total weight so the team knows what is being shipped and can verify vehicle capacity.
5. Assign a company Vehicle, Trailer, and Driver from the dropdown menus, or enter subcontractor details if using an outside carrier.
6. Enter the Buy Rate and Driver Advance Amount if using a subcontracted vehicle.
7. Click Submit to save the shipment details to the system.

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Job_Order | The reference number for this shipment. Enter the existing job order number or leave blank if creating a new one. | text | No |
| Destination_Type | Choose the delivery pattern: single destination, multiple delivery points, or hub-based delivery. This helps plan the route. | text | No |
| Domestic_Shipment_Type | Select the cargo category (full load, partial load, less than truck load, etc.) to determine pricing and vehicle assignment. | text | No |
| Domestic Goods Description | Describe what is being shipped (for example, packaged goods, machinery, pallets, etc.). Include any special handling needs. | textarea | No |
| Domestic Total Weight | Enter the total weight of the shipment in the unit your company uses (pounds or kilograms). Verify this matches the vehicle capacity. | text | No |
| Domestic_Truck_Source | Specify where the vehicle comes from: company fleet, subcontracted carrier, or partner company. | text | No |
| Domestic_Assigned_Vehicle | Select the company truck assigned to haul this shipment. Only appears if using a company vehicle. | text | No |
| Domestic_Assigned_Trailer | Select the trailer attached to the vehicle. Match trailers to the goods type and weight. | text | No |
| Domestic_Assigned_Driver | Select the company driver assigned to this shipment. Only appears if using a company driver. | text | No |
| Buy Rate of Subcontracted Vehicle | Enter the cost per mile or fixed rate you will pay the subcontractor for this shipment. | text | No |
| Domestic Subcontracted Vehicle | Enter the subcontractor's vehicle details (company name and truck number) if not using a company vehicle. | text | No |
| Domestic Subcontracted Driver | Enter the subcontractor's driver name and contact information. | textarea | No |
| Domestic Driver Advance Amount | Enter any cash advance given to the driver before the trip. This reduces their final payment after the shipment completes. | text | No |
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

## Actions

- **Done**
- **Main Forms**
- **Master Data**
- **Submit**
- **Submit Request**

## Tips

- Do not leave Total Weight blank—this is critical for vehicle assignment and billing accuracy. Always confirm weight matches the bill of lading.
- If you assign a company vehicle, you must also assign a trailer and driver. If using a subcontractor, fill in the subcontractor fields instead, not both.

## Related Pages

- [Shipment Details](shipment-details.md)
- [All Shipment Details](all-shipment-details.md)
- [All Domestic Shipment Details](all-domestic-shipment-details.md)
- [Subcontractor Shipment Details](subcontractor-shipment-details.md)
- [All Subcontractor Shipment Details](all-subcontractor-shipment-details.md)
- [Cross Border Shipment Details](cross-border-shipment-details.md)
- [All Cross Border Shipment Details](all-cross-border-shipment-details.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
