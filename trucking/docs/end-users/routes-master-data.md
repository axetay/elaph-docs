# Routes Master Data

![Routes Master Data screenshot](../assets/screenshots/routes-master-data.png)

The Routes Master Data page lets you create and manage trucking routes in the U-Go system. Operations managers and dispatchers use this page to set up new routes, define their physical characteristics (distance, transit time), and establish pricing and truck requirements. You'll work here whenever you need to add a route to your network or update route details.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system#Form:Routes_Master_Data`

## How to Use

1. Select your language from the language dropdown if needed.
2. Enter the starting point in the Origin field and the endpoint in the Destination field. The system will auto-populate the origin and destination types (city, port, warehouse, etc.).
3. Fill in the Origin Country and Destination Country to ensure the route is properly classified.
4. Enter the physical route details: Distance in kilometers, Average Speed in km/h, and Standard Transit Hours or Days.
5. Select Allowed Truck Types and enter Max Gross Weight in tons for this route.
6. Add the Base Rate and select the Rate Basis (per km, per ton, per load, etc.) and Currency for pricing.
7. Click Submit to save the route to your system.

## Page Sections

- A. Identification
- C. Read-only info pulled from Locations
- D. Cross-border & border point
- E. Distance & time
- F. Equipment & limits
- G. Pricing baseline
- H. Admin

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| Origin | The starting location for the route. Type the city or facility name and select from the dropdown list. | text | No |
| Route Name | A clear, short name for this route (for example, 'London to Manchester Hub'). Use consistent naming so dispatchers can quickly find routes. | text | No |
| Destination | The ending location for the route. Type the city or facility name and select from the dropdown list. | text | No |
| Origin Type | The category of the origin location (for example, warehouse, port, distribution center). This auto-populates based on your Origin entry. | text | No |
| Destination Type | The category of the destination location. This auto-populates based on your Destination entry. | text | No |
| Origin Country |  | text | No |
| Destination Country |  | text | No |
| Distance (km) | The total distance of the route in kilometers. Enter the actual road distance, not as the crow flies. | text | No |
| Avg Speed (km/h) | The average expected speed for trucks on this route, accounting for traffic, road conditions, and speed limits. | text | No |

## Actions

- **Done**
- **Main Forms**
- **Master Data**
- **Submit**
- **Submit Request**

## Tips

- Before submitting a new route, verify the distance and transit time with your actual dispatch records or GPS data. Inaccurate estimates will lead to poor schedule planning.
- If you see 'Yes' checkbox in your form, check it only if this route requires special permits or border documentation. This flags the route for compliance review.

## Related Pages

- [Port Representatives Master Data Report](port-representatives-master-data-report.md)
- [Clients Master Data Report](clients-master-data-report.md)
- [Vendors Master Data Report](vendors-master-data-report.md)
- [All Locations Master Data](all-locations-master-data.md)
- [Routes Master Data Report](routes-master-data-report.md)
- [Driver Trip Allowances Master Data](driver-trip-allowances-master-data.md)
- [Driver Trip Allowances Master Data Report](driver-trip-allowances-master-data-report.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
