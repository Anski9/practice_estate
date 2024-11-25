from odoo import models, fields, api

class PracticeEstatePropertyType(models.Model):  # Creating a new model for the real estate property types
    _name = 'practice.estate.property.type'
    _description = 'Real estate property type'
    _order = 'sequence, name'

    name = fields.Char(string='Type', required=True)
    sequence = fields.Integer('Sequence', default=10)
    
    # One2many relation to the properties of this type
    property_ids = fields.One2many(
        'practice.estate.property', 
        'property_type_id'
    )
    # One2many relation to the offers on properties of this type
    offer_ids = fields.One2many(
        'practice.estate.property.offer', 
        'property_type_id',
        string='Offers'
    )
    # Computed field to store the number of offers on properties of this type
    offer_count = fields.Integer(
        string='Number of offers',
        compute='_compute_offer_count',
        store=True
    )

    # Filtered properties with fixed logic
    filtered_property_ids = fields.One2many(
        'practice.estate.property',
        'property_type_id',
        compute='_compute_filtered_property_ids',
        store=False,
        string='Filtered Questions',
    )

    @api.depends('property_ids')
    def _compute_filtered_property_ids(self):
        for record in self:
            record.filtered_property_ids = record.property_ids.filtered(
                lambda p: p.expected_price >= 100
            )


    custom_view_mode = fields.Selection(
        [('questions', 'Questions'), ('info', 'Info')],
        string='View mode',
        default='questions'
    )

    # @api.model
    # def view_init(self, fields_list):
    #     self.custom_view_mode = 'questions'
    #     return super(PracticeEstatePropertyType, self).view_init(fields_list)

    

    # @api.onchange('custom_view_mode')
    # def _onchange_custom_view_mode(self):
    #     self.action_switch_view()

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(PracticeEstatePropertyType, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

    #     if view_type =='form':

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     self.action_switch_view()

    # def action_switch_view(self):
    #     if self.custom_view_mode == 'info':
    #         print('info')
    #         action = self.env.ref('practice_estate.practice_estate_property_type_action_info').read()[0]
    #     else:
    #         action = self.env.ref('practice_estate.practice_estate_property_type_action').read()[0]
    
    #     view_id = action.get('view_id') and action['view_id'][0] if action.get('view_id') else False

    #     if self.custom_view_mode == 'questions':
    #         view_id = self.env.ref('practice_estate.practice_estate_property_type_form_view').id
    #     print('view_id', view_id)
    #     print(id)
    #     return({
    #     'type': 'ir.actions.act_window',
    #     'res_model': action['res_model'],
    #     'view_mode': 'form',
    #     'views': [(view_id, 'form')] if view_id else [],
    #     'res_id': self.id,
    #     'target': 'current',
    #     })

    #     return res



    # Compute the number of offers based on the offer_ids
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # SQL constraint to ensure the uniqueness of the type name
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The type name must be unique.')
    ]