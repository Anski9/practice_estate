from odoo import models, fields, api, _
from odoo.exceptions import UserError
import xml.etree.ElementTree as xee

class PracticeEstateTab(models.Model):
    _name = "practice.estate.tab"
    _description = "Tabs for practice estate"
    
    name = fields.Char(string="Eläintarhat", required=True)
    #tab_name = fields.Char(string="Tab name", help="Define the name of the tab shown in the interface")
    animal_data_ids = fields.One2many("practice.estate.animal.data", "zoo_id", string="Animals data")
    #dynamic_tab_name = fields.Char(compute="_compute_dynamic_tab_name", store=True)
    label = fields.Char("New tab", required=True, help="The name of the tab shown in the interface")
    view_id = fields.Many2one("ir.ui.view", string="View")
    sh_position = fields.Selection([('before', 'Before'), ('after', 'After')], string="Position", default="after")
    #groups = fields.Many2many("res.groups", string="User Groups")

    tab_list = fields.Selection(selection="get_tab_list", string="Tab list")
    invisible_tab = fields.Boolean("Invisible tab", compute="check_invisible_tab")

    @api.model
    def get_tab_list(self):
        """Palauttaa olemassa olevien välilehtien listan"""
        view_id = self.env.ref('practice_estate.view_practice_estate_tab_form')
        #if not view_id:
        #    return []
        
        view_ids = self.env['ir.ui.view'].search([('inherit_id', '=', view_id.id)])
        data1 = str(view_id.arch_base)
        doc = xee.fromstring(data1)
        tab_list = []
        
        for tag in doc.findall('.//page'):
            if 'name' in tag.attrib:
                tab_list.insert(
                    len(tab_list), (tag.attrib['name'], tag.attrib['string']))
        if view_ids:
            for view in view_ids:
                if view != self.view_id:
                    data1 = str(view.arch_base)
                    doc = xee.fromstring(data1)
                    for tag in doc.findall('.//page'):
                        if 'name' in tag.attrib:
                            tab_list.insert(
                                len(tab_list), (tag.attrib['name'], tag.attrib['string']))
        
        return tab_list

    @api.depends('tab_list')
    def check_invisible_tab(self):
        for rec in self:
            if len(rec.get_tab_list()) > 0:
                rec.invisible_tab = False
            else:
                rec.invisible_tab = True

    # @api.depends("tab_name")
    # def _compute_dynamic_tab_name(self):
    #     for record in self:
    #         record.dynamic_tab_name = record.tab_name or "Animals"

    #@api.model
    #def create(self, vals):
    #     """Override the create method to include dynamic tab creation."""
    #     new_tab = super().create(vals)
    #     new_tab.create_tab()
    #    return super().create(vals)

    def create_tab(self):
        """Creates a dynamic tab in the view."""
        inherit_id = self.env.ref('practice_estate.view_practice_estate_tab_form')
        print("Peritty näkymä ID:", inherit_id.id)

        if not self.sh_position:
            raise UserError(_("Please select a position for the tab."))


        if self.sh_position == "before":
            print("Luodaan välilehti ennen muita välilehtiä")
            arch_base = _('''<?xml version="1.0"?>
                            <data>
                            <xpath expr="//form/sheet/notebook" position="before">
                            <notebook>
                            <page name="%s" string="%s" invisible="[('id', '!=', 83)]">
                            <group>
                            <field name="animal_data_ids"/>
                            </group>
                            </page>
                            </notebook>
                            </xpath>
                            </data>''') % (self.name, self.label)
            
        elif self.sh_position == 'after':
            print("Luodaan välilehti muiden jälkeen")
            arch_base = _('''<?xml version="1.0"?>
                            <data>
                            <xpath expr="//form/sheet/notebook" position="after">
                            <notebook>
                            <page name="%s" string="%s" invisible="[('id', '!=', 83)]">
                            <group>
                            <field name="animal_data_ids"/>
                            </group>
                            </page>
                            </notebook>
                            </xpath>
                            </data>''') % (self.name, self.label)
            
        else:
            print("Virhe: Sijaintia ei ole määritelty oikein")
            arch_base = None

        if not arch_base:
            raise UserError(_("Could not create the tab layout. Check tab position."))

        print("Luodaan uusi näkymä dynaamiselle välilehdelle")
        view = self.env['ir.ui.view'].create({
            'name': "practice_estate.dynamic.tab",
            'type': 'form',
            'model': 'practice.estate.tab',
            'inherit_id': inherit_id.id,
            'arch_base': arch_base,
            'active': True,
            'mode': 'extension',
        })
        print("Uusi näkymä luotu ID: ", view.id)
        self.write({'view_id': view.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def write(self, vals):
        """Override the write method to include dynamic tab creation."""
        inherit_id = self.env.ref('practice_estate.view_practice_estate_tab_form')
        res = super(PracticeEstateTab, self).write(vals)

        for rec in self:
            if rec.view_id:
                arch_base = _('''<?xml version="1.0"?>
                                <data>
                                <xpath expr="//form/sheet/notebook" position="inside">
                                <notebook>
                                <page name="%s" string="%s">
                                <group>
                                <field name="animal_data_ids" domain="[('zoo_id', '=', id)]"/>
                                </group>
                                </page>
                                </notebook>
                                </xpath>
                                </data>''') % (rec.name, rec.label)
                
                rec.view_id.write({
                    'name': "practice_estate.dynamic.tab",
                    'type': 'form',
                    'model': 'practice.estate.tab',
                    'mode': 'extension',
                    'inherit_id': inherit_id.id,
                    'arch_base': arch_base,
                    'active': True,
                })
        return res
    
    def unlink(self):
        """Override the unlink method to delete the dynamic tab."""
        if self.view_id:
            self.view_id.unlink()
        return super().unlink()




