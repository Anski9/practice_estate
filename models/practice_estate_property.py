from odoo import api, models, fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class PracticeEstateProperty(models.Model):  # Creating a new model for the real estate properties
    _name = 'practice.estate.property'
    _description = 'Real estate property'
    _order = 'state asc, id desc'

    name = fields.Char(string='Property name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available from', copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(string='Active', default=True)
    state= fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'SOLD'), ('canceled', 'Canceled')])
    
    # Method to mark the property as sold
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled property cannot be marked as sold.')
            record.state = 'sold'

    # Method to mark the property as canceled
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property cannot be canceled.')
            record.state = 'canceled'
            
    # Many2one relation to the property type
    property_type_id = fields.Many2one(
        'practice.estate.property.type',
        string='Property type',
        required=True,
    )
    # Field to store the salesperson, defaulting to the current user
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )
    # Field to store the buyer
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
    )
    # Many2many relation to the tags
    tag_ids = fields.Many2many(
        'practice.estate.property.tag',
        string='Tags',
    )
    # One2many relation to the offers on this property
    offer_ids = fields.One2many(
        'practice.estate.property.offer', 
        'property_id', 
        string='Offers',
    )
    # Computed field to store the total area
    total_area = fields.Integer(
        string='Total area (sqm)', 
        compute='_compute_total_area',
    )
    # Compute the total area based on the living area and garden area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Computed field to store the best offer price
    best_price = fields.Float(
        string='Best offer',
        compute='_compute_best_price',
    )
    # Compute the best offer price based on the offer prices
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # Set default values for garden area and orientation when the garden field is changed
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # SQL constraints to ensure the expected price and selling price are positive
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.')
    ]

    # Ensure selling price is at least 90% of expected price
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError('The selling price cannot be less than 90% of the expected price.')
            
    # Ensure the property is not deleted if it is not in 'New' or 'Canceled' state        
    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties that are in 'New' or 'Canceled' state.")