{
    'name': 'Practice Estate',
    'summary': 'Practice module',
    'category': 'Practice Estate',
    'author': 'Anski9',
    'depends': ['base', 'sh_task_custom_fields', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/practice_estate_tab_views.xml',
        'views/practice_estate_actions.xml',
        'views/practice_estate_property_views.xml',
        'views/practice_estate_property_kanban_view.xml',
        'views/practice_estate_property_offer_views.xml',
        'views/practice_estate_property_type_views.xml',
        'views/practice_estate_property_tag_views.xml',
        'views/practice_estate_property_resusers_views.xml',
        'views/practice_estate_menus.xml',
    ],
    'assets': {
        'web.assets_common': [
            'practice_estate/static/src/js/view_mode_switch.js',
            'practice_estate/static/src/js/test_script.js',
        ],
        'web.assets_backend': [
            'practice_estate/static/src/js/filtering.js',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    #'post_init_hook': 'update_filter_criteria',
}