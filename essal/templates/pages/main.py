# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
# import hashlib, os, json
# import datetime
# import random
import frappe
from frappe import _
# from frappe.commands.scheduler import _is_scheduler_enabled
# from frappe.model.db_schema import DbManager
# from frappe.utils.password import create_auth_table

__version__ = '0.0.1'

import re

max_communications_per_hour = 1000
no_cache = True


def get_page_meta_data(context, page):
    try:
        page = frappe.get_doc("Web Page", page).as_dict()
        context["title"] = "" if page.show_title is 0 else page.title

        meta = re.search(re.compile("(<!--%s-->)([\s\S]*?)(<!---->)" % context.current_lang), page.header)
        if meta:
            context["meta"] = meta.group(2).replace("/*", "/>").replace("*", "<")
    except Exception as e:
        pass
    frappe.local.lang = "ar"
    return context


@frappe.whitelist(allow_guest=True)
def signup_new_user(email="", company_name=""):
    if not email:
        frappe.response["message"] = _('Email is Required', "ar"),
        return
    try:
        frappe.validate_email_add(email_str=email, throw=True)
    except:
        frappe.response["message"] = _('{0} is not a valid Email address!', "ar").format(email),
        return

    if not company_name:
        frappe.response["message"] = _('Company Name is Required', "ar"),
        return

    # Check for duplication
    if frappe.db.exists(
            "Site",
            {
                "email": email
            }
    ):
        frappe.response["message"] = _('This email is already used!', "ar"),
        return
    default_server = frappe.db.get_single_value("General Settings", "default_server")
    domain = company_name.replace(" ", "").lower()

    if not domain.isalnum():
        frappe.response["message"] = _('Company name should consists of Alphabetic and numbers only.', "ar"),
        return
    domain = "{0}.{1}".format(domain, default_server)
    if frappe.db.exists(
            "Site",
            {
                "domain": domain
            }
    ):
        frappe.response["message"] = _('This Company Name is already used!', "ar"),
        return
    # Create site
    from random import choice
    import string
    admin_pass = ''.join([choice(string.digits) for i in range(6)])
    frappe.get_doc(dict(
        doctype='Site',
        domain=domain,
        server=default_server,
        company_name=company_name,
        company_email=email,
        is_ready=0,
        status="New",
    )).insert(ignore_permissions=True)

    # Send them a welcome email
    msg = """<div dir="rtl"><br><h4>
    أهلا بكم في نماء.. {}
</h4><br> </div>
<div dir="rtl"><h5>
   يسرنا إعلامكم أن الخطوة الأولى لتسجيل شركتكم في نماء قد تمت بنجاح..
<br>
     سوف نقوم بمراسلتكم قريبا مرة أخرى ونرسل لكم كافة بيانات تسجيل الدخول إلى نظام نماء المحاسبي.
    نتمنى أن يكون نماء خطوة نحو التقدم لكم.
<br></h5></div><div dir="ltr"><h4>
    فريق عمل نماء
</h4> </div>""".format(company_name)
    try:
        frappe.sendmail(
        message=msg,
        recipients=[email],
        subject="مرحبا في نماء",
        sender="hudhud.co.sa@gmail.com",
        delayed=False,
        as_markdown=True
    )
    except:
        frappe.response["message"] = _('{0} is not a valid Email address!', "ar").format(email),
        return
    from frappe.utils.background_jobs import enqueue
    enqueue(
        send_create_site,
        domain=domain,
        admin_pass=admin_pass
    )

    return "okay", _("You will Receive an email with full details soon", "ar")


def send_create_site(domain, admin_pass):
    link = "http://xxx.erp.altqniah.sa:8001/create_site?domain={0}&admin_pass={1}".format(domain, admin_pass)
    from urllib2 import Request, urlopen
    urlopen(Request(link))


@frappe.whitelist(allow_guest=True)
def send_site_details_email():

    domain = frappe.form_dict.get('domain')
    admin_pass = frappe.form_dict.get('admin_pass')

    company = frappe.get_value(
        "Site",
        dict(domain=domain),
        ["company_name", "company_email", "name"],
        as_dict=1
    )
    # Send them a welcome email
    msg = """<div dir="rtl"><br><h4>
        أهلا بكم مجددا في نماء..
</h4><br></div><div dir="rtl"><h5>
       يسعدنا أن نبلغكم بأن موقعكم الخاص بنظام نماء المحاسبي جاهز الآن للإستخدام..
<br>
     للدخول إلي موقعكم.. يرجى الضغط على الرابط التالي:
</h5></div><div dir="rtl"><h3>
{domain}
<br></h3></div><div dir="rtl">
بيانات الدخول:<br>
</div><div dir="rtl"><h4>
اسم المستخدم: <b>Administrator</b><br>
</h4></div><div dir="rtl"><h4>
كلمة المرور: <b>{admin_pass}</b><br>
</h4></div>
<div dir="rtl"><h5>
<br>نتمنى لكم محاسبة أكثر دقة مع نماء<br>
<br></h5></div><div dir="ltr"><h4>
        فريق عمل نماء
</h4> </div>""".format(domain=domain, admin_pass=admin_pass)

    frappe.sendmail(
        message=msg,
        recipients=[company.company_email],
        subject="تفعيل حسابك في نماء",
        sender="hudhud.co.sa@gmail.com",
        delayed=False,
        as_markdown=True
    )

    site = frappe.get_doc("Site", company.name)
    site.status = "Active"
    site.save(ignore_permissions=1)

# #############################################################################3
#
# @frappe.whitelist(allow_guest=True)
# def user_account(id, user_name, users_number, expiry_date):
#     # code for run script new sites
#     print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Start$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
#     ''' variables local '''
#     # current_site = 'subscripe'
#     # mariadb_root_username = 'root'
#     # mariadb_root_password = 'root'
#
#     ''' variables server '''
#     current_site = 's1.essal.co'
#     mariadb_root_username = 'root'
#     mariadb_root_password = 'kulkul'
#
#     db_name = ''
#     site = user_name + '.s1.essal.co'
#     admin_password = user_name + 'Admin'
#     ''' If you want to install another Apps, add to install_apps variable'''
#     install_apps = ('erpnext',)
#     force = True
#     verbose = True
#
#     ''' If site exist, change the site name '''
#     while site in frappe.utils.get_sites():
#         site = user_name + str(random.randint(0, 99999999999)) + '.s1.essal.co'
#
#     try:
#         db = frappe.local.db
#         conf = frappe.local.conf
#         request = frappe.local.request
#         response = frappe.local.response
#         session = frappe.local.session
#         user = frappe.local.user
#         flags = frappe.local.flags
#         error_log = frappe.local.error_log
#         debug_log = frappe.local.debug_log
#         message_log = frappe.local.message_log
#         lang = frappe.local.lang
#
#         frappe.init(site=site, new_site=True)
#
#         _new_site(current_site, db_name, site, mariadb_root_username, mariadb_root_password, admin_password, verbose,
#                   install_apps, None,
#                   force)
#
#         _set_limits({}, site, (("expiry", str(expiry_date)), ("users", str(users_number)),))
#
#         # essal_subscriptions_insert_or_update(id, user_name, site, expiry_date)
#         print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Finish$$$$$$$$$$$$$$$$$$$$$$$$$$$"
#
#         frappe.init(current_site, sites_path='.')
#         frappe.connect(db_name=hashlib.sha1(current_site).hexdigest()[:16])
#
#         frappe.local.db = db
#         frappe.local.conf = conf
#         frappe.local.request = request
#         frappe.local.response = response
#         frappe.local.session = session
#         frappe.local.user = user
#         frappe.local.flags = flags
#         frappe.local.error_log = error_log
#         frappe.local.debug_log = debug_log
#         frappe.local.message_log = message_log
#         frappe.local.lang = lang
#
#         return site
#     except Exception, e:
#         frappe.throw(_("Error"))
#
#
# def essal_subscriptions_insert_or_update(zoho_id, zoho_user_name, site_name, zoho_expiry_date):
#     date = datetime.datetime.strptime(zoho_expiry_date, '%Y-%m-%d')
#
#     # essal_subscriptions = frappe.new_doc("Essal Subscriptions")
#     # essal_subscriptions.zoho_id = str(zoho_id)
#     # essal_subscriptions.zoho_user_name = str(zoho_user_name)
#     # essal_subscriptions.site_name = str(site_name)
#     # essal_subscriptions.zoho_expiry_date = date
#     # essal_subscriptions.insert()
#
#     frappe.db.sql("""INSERT INTO `tabEssal Subscriptions` (zoho_id, zoho_user_name, site_name, zoho_expiry_date)
#                 VALUES (%s, %s, %s, %s) """, (str(zoho_id), str(zoho_user_name), str(site_name), date))
#
#
# def _set_limits(context, site, limits):
#     site_config_path = get_site_config_path(site)
#
#     with frappe.init_site(site):
#         frappe.connect()
#         new_limits = {}
#         for limit, value in limits:
#             if limit not in ('emails', 'space', 'users', 'email_group',
#                              'expiry', 'support_email', 'support_chat', 'upgrade_url'):
#                 frappe.throw('Invalid limit {0}'.format(limit))
#
#             if limit == 'expiry' and value:
#                 try:
#                     datetime.datetime.strptime(value, '%Y-%m-%d')
#                 except ValueError:
#                     raise ValueError("Incorrect data format, should be YYYY-MM-DD")
#
#             elif limit == 'space':
#                 value = float(value)
#
#             elif limit in ('users', 'emails', 'email_group'):
#                 value = int(value)
#
#             new_limits[limit] = value
#
#     update_site_config("limits", new_limits, validate=False, site_config_path=site_config_path)
#
#
# def update_site_config(key, value, validate=True, site_config_path=None):
#     """Update a value in site_config"""
#     if not site_config_path:
#         site_config_path = get_site_config_path()
#
#     with open(site_config_path, "r") as f:
#         site_config = json.loads(f.read())
#
#     # In case of non-int value
#     if value in ('0', '1'):
#         value = int(value)
#
#     # boolean
#     if value in ("false", "true"):
#         value = eval(value.title())
#
#     # remove key if value is None
#     if value == "None":
#         if key in site_config:
#             del site_config[key]
#     else:
#         site_config[key] = value
#
#     with open(site_config_path, "w") as f:
#         f.write(json.dumps(site_config, indent=1, sort_keys=True))
#
#
# def _new_site(current_site, db_name, site, mariadb_root_username=None, mariadb_root_password=None, admin_password=None,
#               verbose=False, install_apps=None, source_sql=None, force=False, reinstall=False):
#     """Install a new Frappe site"""
#     if not db_name:
#         db_name = hashlib.sha1(site).hexdigest()[:16]
#
#     from frappe.installer import install_app as _install_app
#     import frappe.utils.scheduler
#
#     frappe.init(site=site)
#
#     try:
#         # enable scheduler post install?
#         enable_scheduler = _is_scheduler_enabled()
#     except:
#         enable_scheduler = False
#
#     make_site_dirs(site)
#     try:
#         installing = touch_file(get_site_path(site, 'locks', 'installing.lock'))
#
#         install_db(root_login=mariadb_root_username, root_password=mariadb_root_password, db_name=db_name,
#                    admin_password=admin_password, verbose=verbose, source_sql=source_sql, force=force,
#                    reinstall=reinstall, site=site)
#
#         apps_to_install = ['frappe'] + (frappe.conf.get("install_apps") or []) + (list(install_apps) or [])
#         for app in apps_to_install:
#             _install_app(app, verbose=verbose, set_as_patched=not source_sql)
#
#         frappe.utils.scheduler.toggle_scheduler(enable_scheduler)
#         frappe.db.commit()
#
#         scheduler_status = "disabled" if frappe.utils.scheduler.is_scheduler_disabled() else "enabled"
#         print "*** Scheduler is", scheduler_status, "***"
#
#     finally:
#         if os.path.exists(installing):
#             os.remove(installing)
#
#         frappe.destroy()
#
#
# def get_site_path(site, *path):
#     path = os.path.join(site, *path)
#     return './' + path
#
#
# def touch_file(path):
#     with open(path, 'a'):
#         os.utime(path, None)
#     return path
#
#
# def make_site_dirs(site):
#     site_path = './' + site
#     site_public_path = os.path.join(site_path, 'public')
#     site_private_path = os.path.join(site_path, 'private')
#     for dir_path in (
#             os.path.join(site_private_path, 'backups'),
#             os.path.join(site_public_path, 'files'),
#             os.path.join(site_private_path, 'files'),
#             os.path.join(site_path, 'task-logs')):
#         if not os.path.exists(dir_path):
#             os.makedirs(dir_path)
#         os.chmod(dir_path, 0777)
#     locks_dir = site_path + "/locks"
#     if not os.path.exists(locks_dir):
#         os.makedirs(locks_dir)
#
#     os.chmod(locks_dir, 0777)
#     os.chmod(site_path, 0777)
#     os.chmod(site_public_path, 0777)
#     os.chmod(site_private_path, 0777)
#
#
# def install_db(root_login="root", root_password=None, db_name=None, source_sql=None,
#                admin_password=None, verbose=True, force=0, site_config=None, reinstall=False, site=None):
#     from frappe.installer import check_if_ready_for_barracuda, remove_missing_apps, \
#         create_list_settings_table, get_root_connection
#
#     make_conf(db_name, site_config=site_config, site=site)
#     frappe.flags.in_install_db = True
#     if reinstall:
#         frappe.connect(db_name=db_name)
#         dbman = DbManager(frappe.local.db)
#         dbman.create_database(db_name)
#
#     else:
#         frappe.local.db = get_root_connection(root_login, root_password)
#         frappe.local.session = frappe._dict({'user': 'Administrator'})
#         create_database_and_user(force, verbose, db_name)
#
#     frappe.conf.admin_password = frappe.conf.admin_password or admin_password
#
#     frappe.connect(db_name=db_name)
#     check_if_ready_for_barracuda()
#     import_db_from_sql(source_sql, verbose, db_name)
#     remove_missing_apps()
#
#     create_auth_table()
#     create_list_settings_table()
#
#     frappe.flags.in_install_db = False
#
#
# def make_conf(db_name=None, db_password=None, site_config=None, site=None):
#     make_site_config(db_name, db_password, site_config, site)
#     sites_path = '.'
#     frappe.destroy()
#     frappe.init(site, sites_path=sites_path)
#
#
# def make_site_config(db_name=None, db_password=None, site_config=None, site=None):
#     from frappe.installer import get_conf_params
#     frappe.create_folder(os.path.join('./' + site))
#     site_file = get_site_config_path(site)
#
#     if not os.path.exists(site_file):
#         if not (site_config and isinstance(site_config, dict)):
#             site_config = get_conf_params(db_name, db_password)
#
#         with open(site_file, "w") as f:
#             f.write(json.dumps(site_config, indent=1, sort_keys=True))
#
#     os.chmod(site_file, 0777)
#
#
# def get_site_config_path(site=None):
#     return os.path.join('./' + site, "site_config.json")
#
#
# def create_database_and_user(force, verbose, db_name):
#     dbman = DbManager(frappe.local.db)
#     if force or (db_name not in dbman.get_database_list()):
#         dbman.delete_user(db_name)
#         dbman.drop_database(db_name)
#     else:
#         raise Exception("Database %s already exists" % (db_name,))
#
#     dbman.create_user(db_name, frappe.conf.db_password)
#     if verbose: print "Created user %s" % db_name
#
#     dbman.create_database(db_name)
#     if verbose: print "Created database %s" % db_name
#
#     dbman.grant_all_privileges(db_name, db_name)
#     dbman.flush_privileges()
#     if verbose: print "Granted privileges to user %s and database %s" % (db_name, db_name)
#
#     # close root connection
#     frappe.db.close()
#
#
# def import_db_from_sql(source_sql, verbose, db_name):
#     if verbose: print "Starting database import..."
#     if not source_sql:
#         source_sql = os.path.join(os.path.dirname(frappe.__file__), 'data', 'Framework.sql')
#     DbManager(frappe.local.db).restore_database(db_name, source_sql, db_name, frappe.conf.db_password)
#     if verbose: print "Imported from database %s" % source_sql
