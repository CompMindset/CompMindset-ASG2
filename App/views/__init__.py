# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .shift_api import shift_api
from .attendance_api import attendance_api
from .report_api import report_api


views = [user_views, index_views, auth_views, shift_api, attendance_api, report_api] 
# blueprints must be added to this list