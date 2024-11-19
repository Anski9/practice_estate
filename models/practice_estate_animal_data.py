from odoo import models, fields

class PracticeEstateAnimalData(models.Model):
    _name = "practice.estate.animal.data"
    _description = "Animal data for practice estate"

    question = fields.Char("Question")
    zoo_id = fields.Many2one("practice.estate.tab", string="Zoo", ondelete="cascade")