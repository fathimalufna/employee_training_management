from odoo import models, fields, api

class TrainingTrainer(models.Model):
    _name = 'training.trainer'
    _description = 'Trainer'

    name = fields.Char(string="Name", required=True)
    expertise = fields.Char(string="Expertise")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    employee_id = fields.Many2one('hr.employee', string="Related Employee")

    # Smart button field
    course_count = fields.Integer(string="Courses", compute="_compute_course_count")

    # @api.depends('id')
    def _compute_course_count(self):
        for trainer in self:
            trainer.course_count = self.env['training.course'].search_count([('trainer_id', '=', trainer.id)])
