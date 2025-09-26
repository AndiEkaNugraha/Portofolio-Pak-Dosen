{
    'name': 'Remove Powered by Odoo from Website & Add Custom Text',
    'version': '19.0.1.0.0',
    'summary': 'FREE: Hide or customize the "Powered by Odoo" footer message with rich HTML.',
    'description': '''
        🆓 FREE MODULE - No Cost, No Limitations!

        This completely free module gives you complete control over the "Powered by Odoo" footer branding. Hide the default message entirely or replace it with your own custom HTML content.

        ✨ Key Features:
        • 🎯 Toggle "Powered by Odoo" visibility on/off
        • 🎨 Rich HTML editor for custom footer text (bold, colors, links, alignment)
        • 🔧 Easy configuration through Settings menu
        • 🌐 Seamless website footer integration
        • ⚡ Real-time changes without page refresh
        • 📱 Responsive design support

        💡 Perfect for:
        • White-label solutions
        • Brand customization
        • Professional website footers
        • Custom branding requirements

        🚀 100% Free - No hidden costs, no premium features!
    ''',
    'author': 'Waqas Mustafa',
    'website': 'https://www.linkedin.com/in/waqas-mustafa-ba5701209/',
    'support': 'mustafawaqas0@gmail.com',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'website'],
    'data': [
        'views/res_config_settings_view.xml',
        'views/brand_promotion_override.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
