from odoo import api, SUPERUSER_ID

def update_filter_criteria(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    criteria_data = {
        "eläintarha1": [
            {"field_name": "expected_price", "operator": ">=", "value": "100"}
        ],
        "eläintarha2": [
            {"field_name": "expected_price", "operator": ">=", "value": "200"}
        ]
    }

    for property_type_name, filters in criteria_data.items():
        property_type = env['practice.estate.property.type'].search([('name', '=', property_type_name)], limit=1)
        if not property_type:
            continue

        for filter_data in filters:
            existing_filter = env['property.filter.criteria'].search([
                ('property_type_id', '=', property_type.id),
                ('name', '=', filter_data['name'])
            ], limit=1)

            if existing_filter:
                existing_filter.write(filter_data)
            else:
                filter_data['property_type_id'] = property_type.id
                env['property.filter.criteria'].create(filter_data)