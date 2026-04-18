# Auto PO Items

![Auto PO Items screenshot](../assets/screenshots/auto-po-items.png)

The Auto PO Items page allows you to create and manage automatic purchase orders for spare parts needed in garage maintenance. Maintenance planners and procurement staff use this page to link spare parts to maintenance orders, set quantities and pricing, and track the procurement status. This is typically used when setting up reusable maintenance templates or processing bulk spare part requests.

**URL:** `https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance#Form:Auto_PO_Items`

## How to Use

1. Select the Maintenance Order Source from the dropdown to link this spare part to a specific maintenance job or template.
2. Choose the Spare Part you need to order using the search dropdown—the system will show all available parts in your inventory.
3. Enter the Required Quantity for this spare part.
4. Fill in Supplier Name and Brand Name to specify where and what brand you want to order.
5. Enter the Estimated Unit Price so the system can calculate the Total cost automatically.
6. Set the Status to 'Pending' or 'Approved' depending on whether this order is ready to process.
7. Click Submit to save the auto PO item and add it to your procurement queue.

## Form Fields

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| lang-select-dropdown |  | dropdown | No |
| Auto PO Items ID |  | text | No |
| zc-sel2-foc-Maintenance_Order_Source |  | text | No |
| zc-sel2-inp-Maintenance_Order_Source |  | text | No |
| Maintenance_Order_Source | Select the maintenance order or job template that requires this spare part. This links the purchase order to a specific maintenance task. | text | No |
| zc-sel2-foc-Spare_Part |  | text | No |
| zc-sel2-inp-Spare_Part |  | text | No |
| Spare_Part | Search for and select the spare part you need to order. Use the search box to find parts by name or code. | text | No |
| Required Quantity | Enter the number of units needed for this maintenance order. | text | No |
| Supplier Name | Enter the name of the supplier or vendor you want to order from. | text | No |
| Brand Name | Enter the brand or manufacturer name of the spare part to ensure correct ordering. | text | No |
| Estimated Unit Price | Enter the cost per unit. The Total will calculate automatically by multiplying this by the Required Quantity. | text | No |
| Total |  | text | No |
| zc-sel2-foc-Status |  | text | No |
| zc-sel2-inp-Status |  | text | No |
| Status | Set to 'Pending' if the order is still being prepared, or 'Approved' if it is ready for procurement to process. | text | No |
| submit |  | submit | No |
| searchmap |  | text | No |
| useIconSwitch |  | checkbox | No |
| toggleIconSwitch |  | checkbox | No |
| saveIcons |  | button | No |
| resetIcons |  | button | No |
| Search... |  | text | No |
| I have read the above conditions. |  | checkbox | No |
| reqEmailId | Enter the email address of the person requesting this spare part (usually the maintenance manager). | text | No |
| s2id_autogen2 |  | text | No |
| s2id_autogen2_search |  | text | No |
| supportType | Select the type of support needed if you encounter issues—choose 'Procurement Support' for ordering questions. | dropdown | No |
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

- The Total field auto-calculates—do not manually edit it. If the total looks wrong, check your Estimated Unit Price and Required Quantity.
- Always link an Auto PO Item to a Maintenance Order Source before submitting. Orders without a source will be rejected during approval.

## Related Pages

- [Purchase Orders](purchase-orders.md)
- [All Purchase Orders](all-purchase-orders.md)
- [All Auto PO Items](all-auto-po-items.md)

## Common Workflows

_Add step-by-step workflows specific to your organisation here._
