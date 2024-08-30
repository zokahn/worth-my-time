from src.rag_agent.config import config

NOTIFICATION_CHANNELS = config.get('NOTIFICATION_CHANNELS', {
    'email': {
        'enabled': True,
        'recipients': ['admin@example.com'],
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_username': 'your_email@gmail.com',
        'smtp_password': 'your_password'
    },
    'slack': {
        'enabled': False,
        'webhook_url': 'https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK'
    },
    'sms': {
        'enabled': False,
        'twilio_account_sid': 'YOUR_TWILIO_ACCOUNT_SID',
        'twilio_auth_token': 'YOUR_TWILIO_AUTH_TOKEN',
        'twilio_phone_number': '+1234567890',
        'recipient_phone_number': '+0987654321'
    }
})

NOTIFICATION_TYPES = {
    'critical_error': ['email', 'slack', 'sms'],
    'activity_pattern_change': ['email', 'slack'],
    'report_completion': ['email'],
    'system_event': ['email', 'slack']
}
