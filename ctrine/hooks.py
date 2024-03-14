app_name = "ctrine"
app_title = "Ctrine"
app_publisher = "Grawish Sachdeva"
app_description = "Ctrine Customisations"
app_email = "grawish@outlook.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ctrine/css/ctrine.css"
# app_include_js = "/assets/ctrine/js/ctrine.js"

# include js, css files in header of web template
# web_include_css = "/assets/ctrine/css/ctrine.css"
# web_include_js = "/assets/ctrine/js/ctrine.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ctrine/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"Story": "ctrine/doctype/story/story_calender.js",
                   "Project Milestone": "ctrine/doctype/project_milestone/project_milestone_calender.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
#fixtures
fixtures = [{
                "doctype": "Workflow"
        },
			{
				"doctype": "Workflow State"
			},
            {
                "doctype":"Client Script"
            }
        
	]
# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ctrine/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ctrine.utils.jinja_methods",
# 	"filters": "ctrine.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ctrine.install.before_install"
# after_install = "ctrine.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ctrine.uninstall.before_uninstall"
# after_uninstall = "ctrine.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ctrine.utils.before_app_install"
# after_app_install = "ctrine.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ctrine.utils.before_app_uninstall"
# after_app_uninstall = "ctrine.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ctrine.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------


scheduler_events = {
   "cron": {
        "40 14 * * *": [
            'ctrine.ctrine.server_scripts.timesheet.submit_overdue_timesheets'

        ]
   }
}



# scheduler_events = {
# 	"all": [
# 		"ctrine.tasks.all"
# 	],
# 	"daily": [
# 		"ctrine.tasks.daily"
# 	],
# 	"hourly": [
# 		"ctrine.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ctrine.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ctrine.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ctrine.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ctrine.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ctrine.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ctrine.utils.before_request"]
# after_request = ["ctrine.utils.after_request"]

# Job Events
# ----------
# before_job = ["ctrine.utils.before_job"]
# after_job = ["ctrine.utils.after_job"]
# Import necessary modules

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ctrine.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
