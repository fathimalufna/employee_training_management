{
    'name': 'Employee Training',
    'version': '1.0.0',
    'license': 'LGPL-3',
    'summary': 'Manage employee training courses, trainers and attendance',
    'description': 'Employee Training module - courses, trainers and attendance with chatter and analytics.',
    'category': 'Human Resources',
    'author': 'Fathima Lufna',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/employee_training_actions.xml',
        'views/employee_training_menus.xml',
        'views/training_course_views.xml',
        'views/training_trainer_views.xml',
        'views/training_attendance_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/css/training_course_kanban.css',
        ],
    },
    'sequence': 1,
    'application': True,
    'installable': True,
    'auto_install': False,
}
