from odoo import models, fields

class PracticeEstatePropertyTag(models.Model):  # Creating a new model for the real estate property tags
    _name = 'practice.estate.property.tag'
    _description = 'Real estate property tags'
    _order = 'name'

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color')
    
    # SQL constraint to ensure the uniqueness of the tag name
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.')
    ]