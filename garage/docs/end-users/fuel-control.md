# Fuel Control

![Fuel Control screenshot](../assets/screenshots/fuel-control.png)

The Fuel Control page lets you track and manage fuel consumption for your vehicles. Operations staff use this form to record fuel entries, monitor fuel efficiency, and calculate operating costs. Use this page regularly to maintain accurate fuel records and identify consumption patterns or anomalies.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance#Form:Fuel_Control`

## How to Use

1. Select your vehicle from the Vehicle dropdown at the top of the form.
2. Enter the Normal Consumption Rate for that vehicle (in liters per kilometer or your standard unit).
3. Click 'Add New' to create a new fuel entry record.
4. Fill in the fuel entry details: date, driver name, and fuel amounts in the provided fields.
5. The system automatically calculates Total Liters, Average Consumption, and Cost Per KM based on your entries.
6. Review the calculated values to verify they match your actual fuel usage.
7. Click 'Submit' to save the fuel entry.

## Page Sections

- Basic Info
- Fuel Calculations Layer

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Vehicle | Select the vehicle you are recording fuel for. Choose from your registered fleet. | text | No |
| Normal Consumption Rate | Enter the expected fuel consumption rate for this vehicle under normal operating conditions. This is used to identify unusual fuel usage patterns. | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| #######.## |  | text | No |
| Total Liters | Automatically calculated total fuel amount for this entry. This field is read-only. | text | No |
| Last Odometer | Enter the vehicle's odometer reading at the time of refueling. | text | No |
| Average Consumption | Automatically calculated average fuel consumption rate based on distance traveled and fuel used. This field is read-only. | text | No |
| Cost Per KM | Automatically calculated fuel cost per kilometer. Use this to monitor fuel expense efficiency. This field is read-only. | text | No |
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
- **Maintenance Sub Forms**
- **Spare Parts Sub Forms**
- **Support Forms**
- **Expand**
- **Add New**
- **Submit**
- **Submit Request**

## Tips

- Always record fuel entries immediately after refueling to ensure accurate odometer readings and prevent data entry errors.
- If your Average Consumption is significantly higher than the Normal Consumption Rate, the vehicle may need maintenance—check tire pressure, engine condition, and fuel filter.

## Related Pages

- [All Fuel Controls](all-fuel-controls.md)
- [Fuel Entries](fuel-entries.md)
- [All Fuel Entries](all-fuel-entries.md)
- [Fuel – Vehicle Performance Summary](fuel-vehicle-performance-summary.md)
- [Worst Vehicles Report](worst-vehicles-report.md)
- [Cost Per KM](cost-per-km.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
