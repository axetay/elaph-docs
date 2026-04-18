# Vehicles

![Vehicles screenshot](../assets/screenshots/vehicles.png)

This page lets you register and manage individual vehicles in your fleet. You enter vehicle details like license plate, make, model, fuel type, and GPS tracking status. Operations staff use this when adding new vehicles to the system or updating existing vehicle information.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance#Form:Vehicles`

## How to Use

1. Enter the vehicle's license plate in both the Letters and Digits fields to match your actual plate format.
2. Select the vehicle type using the radio buttons (for example, van, truck, or car).
3. Enter the vehicle's make, model, and year of manufacture.
4. Provide the chassis number, engine number, and date of purchase for record-keeping.
5. Select your fuel type and enter the normal fuel consumption rate in km/L so the system can track fuel efficiency.
6. Indicate whether the vehicle has a GPS tracker installed.
7. Upload a photo of the vehicle, then click Submit to save the vehicle record.

## Page Sections

- Plates
- Type
- Data
- Status

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| License Plate ( Digits )* |  | text | No |
| Full License Plate |  | text | No |
| License plate ( Letters )* |  | text | No |
| Vehicles_Type | Choose the category of this vehicle: van, truck, car, or other. | radio | No |
| Vehicles_Type | Choose the category of this vehicle: van, truck, car, or other. | radio | No |
| Vehicles_Type | Choose the category of this vehicle: van, truck, car, or other. | radio | No |
| Vehicles_Type | Choose the category of this vehicle: van, truck, car, or other. | radio | No |
| Normal Fuel Consumption (Km/L) | Enter the typical fuel efficiency for this vehicle model (kilometers per liter). This helps monitor fuel costs and performance. | text | No |
| zc-sel2-foc-Fuel_Type |  | text | No |
| zc-sel2-inp-Fuel_Type |  | text | No |
| Fuel_Type | Select the fuel this vehicle uses: petrol, diesel, or alternative fuel. | text | No |
| Latest Fuel Price | Enter the current price per liter for this vehicle's fuel type. | text | No |
| Fuel_Vehicle | Confirm whether this vehicle uses fuel-based propulsion. | radio | No |
| Fuel_Vehicle | Confirm whether this vehicle uses fuel-based propulsion. | radio | No |
| Octain ID | The octane rating or fuel specification identifier for this vehicle. | text | No |
| UGO ID | Your company's internal identifier for this vehicle (if assigned). | text | No |
| Date_of_Purchase |  | text | No |
| zc-sel2-foc-Make |  | text | No |
| zc-sel2-inp-Make |  | text | No |
| Make | The manufacturer of the vehicle (for example, Ford, Mercedes, Volvo). | text | No |
| Chassis Number | The unique chassis or VIN number of the vehicle. | text | No |
| GPS_Tracker | Indicate whether this vehicle has an active GPS tracking device installed. | radio | No |
| GPS_Tracker | Indicate whether this vehicle has an active GPS tracking device installed. | radio | No |
| Year of Manufacture | The year the vehicle was built. | text | No |
| Model | The specific model name or number from the manufacturer. | text | No |
| Engine Number | The serial number of the engine. | text | No |
| Upload_Vehicle_Photo |  | hidden | No |
| uploadFile | Attach a clear photograph of the vehicle for identification and record purposes. | file | No |
| License_Expiry_Date | The date when the vehicle's license or registration expires. | text | No |
| Current Mileage ( Km ) |  | text | No |
| zc-sel2-foc-Vehicle_Status |  | text | No |
| zc-sel2-inp-Vehicle_Status |  | text | No |
| Vehicle_Status |  | text | No |
| Upload_License_Photo |  | hidden | No |
| uploadFile | Attach a clear photograph of the vehicle for identification and record purposes. | file | No |
| Notes |  | textarea | No |
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
- **Submit**
- **Submit Request**

## Tips

- Always separate your license plate into letters and digits exactly as shown on your vehicle registration—do not mix them in one field.
- Keep fuel consumption records accurate; incorrect data will give misleading cost reports and maintenance alerts. Update the fuel price field when your supplier's rates change.

## Related Pages

- [All Vehicles](all-vehicles.md)
- [Vehicles Summary Report](vehicles-summary-report.md)
- [All Drivers](all-drivers.md)
- [Driver KPI Evaluation](driver-kpi-evaluation.md)
- [All Driver Kpi Evaluations](all-driver-kpi-evaluations.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
