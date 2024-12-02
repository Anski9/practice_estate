from odoo import models, fields

class PropertyFilterCriteria(models.Model):
    _name = "property.filter.criteria"
    _description = "Property Filter Criteria"

    name = fields.Char(string="Filter name", required=True)
    property_type_id = fields.Many2one("practice.estate.property.type", string="Property type", required=True)
    field_name = fields.Char(string="Field name", required=True)
    operator = fields.Selection([('=', '='), ('!=', '!='), ('>', '>'), ('<', '<'), ('>=', '>='), ('<=', '<=')], string="Operator", required=True)
    value = fields.Char(string="Value", required=True)