# models/training_course.py
# -*- coding: utf-8 -*-
from datetime import datetime, date
from odoo import models, fields, api

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Training Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Course Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    trainer_id = fields.Many2one('training.trainer', string='Trainer', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Datetime(string='End Date', tracking=True)
    duration_days = fields.Integer(string='Duration (days)', compute='_compute_duration_days', store=True)
    attendee_ids = fields.One2many('training.attendance', 'training_id', string='Attendees')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    # Archive flag (Condition 11)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        """Compute difference in days between start_date (date) and end_date (datetime/date)."""
        for rec in self:
            rec.duration_days = 0
            if not rec.start_date or not rec.end_date:
                continue
            try:
                # Normalize start -> date
                if isinstance(rec.start_date, str):
                    # try ISO date first
                    try:
                        start_date = datetime.strptime(rec.start_date, '%Y-%m-%d').date()
                    except Exception:
                        # fallback: try parsing full datetime
                        start_date = datetime.fromisoformat(rec.start_date).date()
                elif isinstance(rec.start_date, date) and not isinstance(rec.start_date, datetime):
                    start_date = rec.start_date
                elif hasattr(rec.start_date, 'date'):
                    start_date = rec.start_date.date()
                else:
                    # fallback
                    start_date = date.today()

                # Normalize end -> date
                if isinstance(rec.end_date, str):
                    try:
                        # prefer full datetime string
                        end_dt = datetime.strptime(rec.end_date, '%Y-%m-%d %H:%M:%S')
                    except Exception:
                        end_dt = datetime.fromisoformat(rec.end_date)
                    end_date = end_dt.date()
                elif isinstance(rec.end_date, date) and not isinstance(rec.end_date, datetime):
                    end_date = rec.end_date
                elif hasattr(rec.end_date, 'date'):
                    end_date = rec.end_date.date()
                else:
                    end_date = start_date

                # compute difference
                rec.duration_days = max(0, (end_date - start_date).days)
            except Exception:
                rec.duration_days = 0

    # Archive / Unarchive methods (for form header buttons)
    def action_archive(self):
        """Archive selected records (set active = False)."""
        return self.write({'active': False})

    def action_unarchive(self):
        """Unarchive selected records (set active = True)."""
        return self.write({'active': True})

    # Optional: default_get to map current user -> employee -> training.trainer
    @api.model
    def default_get(self, fields_list):
        """Set default trainer_id from current user's employee -> training.trainer (if found)."""
        res = super(TrainingCourse, self).default_get(fields_list)
        # only attempt mapping if trainer_id not already provided
        if 'trainer_id' in fields_list and not res.get('trainer_id'):
            user = self.env.user
            # common setups expose user.employee_id
            employee = getattr(user, 'employee_id', False)
            if employee:
                # try to find a training.trainer linked to this employee
                trainer = self.env['training.trainer'].search([('employee_id', '=', employee.id)], limit=1)
                if trainer:
                    res['trainer_id'] = trainer.id
                else:
                    # If your trainer model is hr.employee itself, uncomment the following:
                    # res['trainer_id'] = employee.id
                    pass
        return res

    @api.onchange('trainer_id')
    def _onchange_trainer_id(self):
        if self.trainer_id:
            self.description = self.trainer_id.expertise or ""
        else:
            self.description = ""

