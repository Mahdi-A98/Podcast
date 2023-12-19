# In the name of GOD
from .authenticate_service import AuthenticateService
from .notification_service import NotificationService
from .account_service import AccountService

SERVICE_CLASSES = {
    "authentication":AuthenticateService,
    "notification": NotificationService,
    "account": AccountService
    }
