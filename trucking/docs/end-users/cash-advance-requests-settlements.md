# Cash Advance Requests & Settlements

![Cash Advance Requests & Settlements screenshot](../assets/screenshots/cash-advance-requests-settlements.png)

Use this page to request and track cash advances for trucking jobs before final payment is received. Finance staff and drivers submit requests here, and managers approve them. This is typically used when you need money upfront to cover port fees, fuel, or other job costs.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system#Form:Cash_Advance_Requests_Settlements`

## How to Use

1. Enter the Cash Advance ID if you're updating an existing request, or leave blank to create a new one.
2. Fill in the shipping order details: client name, route, shipping order number, and container information.
3. Select or search for the Job Order and Port Representative using the dropdown fields.
4. Enter the advance amount needed and select the currency (USD, PHP, etc.) and payment method (bank transfer, check, etc.).
5. Add purpose notes explaining why you need the advance and what costs it covers.
6. Enter the name of who is requesting the advance in the 'Requested By' field.
7. Click 'Submit Request' to send for approval, or 'Submit' to save the draft.

## Page Sections

- Data From Job Order
- Requests Info
- Requests & Approvals
- Summary
- Finance Audit

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Cash Advance ID | Auto-generated number that tracks your request. Leave blank for new requests. | text | No |
| Client Name |  | text | No |
| Route |  | text | No |
| Shipping Order No. |  | text | No |
| Port Representative |  | text | No |
| zc-sel2-foc-Job_Order |  | text | No |
| zc-sel2-inp-Job_Order |  | text | No |
| Job_Order | Select the specific job order from the dropdown. Search by order number if you don't see it in the list. | text | No |
| zc-sel2-foc-Port_Representative |  | text | No |
| zc-sel2-inp-Port_Representative |  | text | No |
| Port_Representative | The person at the port or client company who authorizes or confirms this advance. Use the dropdown to find their name. | text | No |
| Selling Price | The total contract value for this shipping job. | text | No |
| MBL No. | Master Bill of Lading number—identifies the shipment at the port. | text | No |
| Work Type | Category of work, such as 'hauling,' 'drayage,' or 'warehouse service.' | text | No |
| Number of Containers | How many containers are being moved in this job. | text | No |
| Size of Containers | Container dimensions, typically 20ft or 40ft. | text | No |
| Requested_Date | The date you are requesting this advance. | text | No |
| Purpose Notes | Explain what the advance covers: fuel, tolls, port documentation fees, labor, etc. | textarea | No |
| Advance Amount | The cash amount you need upfront. | text | No |
| zc-sel2-foc-Currency |  | text | No |
| zc-sel2-inp-Currency |  | text | No |
| Currency | The currency for payment: PHP, USD, etc. | text | No |
| zc-sel2-foc-Payment_Method |  | text | No |
| zc-sel2-inp-Payment_Method |  | text | No |
| Payment_Method | How you want to receive the money: bank transfer, check, cash pickup, etc. | text | No |
| Requested By |  | text | No |
| zc-sel2-foc-Approved_By |  | text | No |
| zc-sel2-inp-Approved_By |  | text | No |
| Approved_By | The manager or finance person who has authority to approve this request. | text | No |
| Payment_Date |  | text | No |
| zc-sel2-foc-Status |  | text | No |
| zc-sel2-inp-Status |  | text | No |
| Status |  | text | No |
| Approved Amount |  | text | No |
| Total Expenses |  | text | No |
| Balance |  | text | No |
| zc-sel2-foc-Settlement_Balance_Status |  | text | No |
| zc-sel2-inp-Settlement_Balance_Status |  | text | No |
| Settlement_Balance_Status |  | text | No |
| zc-sel2-foc-New_Settlement |  | text | No |
| zc-sel2-inp-New_Settlement |  | text | No |
| New_Settlement |  | text | No |
| zc-sel2-foc-Finance_Reviewed_By |  | text | No |
| zc-sel2-inp-Finance_Reviewed_By |  | text | No |
| Finance_Reviewed_By |  | text | No |
| zc-sel2-foc-Finance_Audit_Status |  | text | No |
| zc-sel2-inp-Finance_Audit_Status |  | text | No |
| Finance_Audit_Status |  | text | No |
| Finance_Review_Date |  | text | No |
| Finance Notes |  | textarea | No |
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
- **Expand**
- **Add New**
- **Submit**
- **Submit Request**

## Tips

- Always include clear purpose notes so finance staff understand the advance is legitimate and job-related. Vague requests may be delayed.
- Make sure the advance amount does not exceed the selling price of the job. If it does, your request will likely be rejected.

## Related Pages

- [All Cash Advance Requests & Settlements](all-cash-advance-requests-settlements.md)
- [Open Cash Advances](open-cash-advances.md)
- [Unsettled Cash Advances](unsettled-cash-advances.md)
- [Driver Expenses & Wages Form](driver-expenses-wages-form.md)
- [Driver Expenses & Wages Form Report](driver-expenses-wages-form-report.md)
- [Driver Unpaid Summary](driver-unpaid-summary.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
