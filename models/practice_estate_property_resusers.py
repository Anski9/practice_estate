from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'  # Inheriting from the 'res.users' model to extend its functionality

    # Adding a new field to the 'res.users' model to store the properties assigned to a salesperson
    property_ids = fields.One2many(
        'practice.estate.property',
        'salesperson_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )