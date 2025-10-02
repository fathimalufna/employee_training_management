from odoo import models, fields

class TrainingAttendance(models.Model):
    _name = "training.attendance"
    _description = "Training Attendance"
    _order = "training_id, employee_id"

    training_id = fields.Many2one('training.course', string="Course", required=True, ondelete="cascade")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    status = fields.Selection([('attended', 'Attended'), ('absent', 'Absent')], string="Status", default="absent")
    notes = fields.Text(string="Notes")
