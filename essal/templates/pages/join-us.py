from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = True


def get_context(context):
    # context.no_cache = 1

    # context.email = 'eyad@gmail.com'  # frappe.form_dict['email']
    form_data = dict()

    context["token"] = 'eyad test'
    form_data['association_name'] = 'test association_name'
    form_data['email'] = 'eyad.farra@exa.com.sa'
    form_data['name'] = 'Eyad Farra'
    form_data['mobile_number'] = '0597333268'

    context['form_data'] = form_data
    return context


@frappe.whitelist(allow_guest=True)
def join_us(association_name, email, name, mobile_number, state=None, city=None, activity=None, employee_count=None):
    try:
        frappe.validate_email_add(email_str=email, throw=True)
    except:
        frappe.response["message"] = _('{0} is not a valid Email address!', "ar").format(email),
        return

    return "okay", _("You will Receive an email with full details soon", "ar")
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
    domain = association_name.replace(" ", "").lower()

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
        company_name=association_name,
        company_email=email,
        is_ready=0,
        status="New",
    )).insert(ignore_permissions=True)

    # Send them a welcome email
    msg = """<div dir="rtl"><br><h4>
    أهلا بكم في هُدهُد.. {}
</h4><br> </div>
<div dir="rtl"><h5>
   يسرنا إعلامكم أن الخطوة الأولى لتسجيل شركتكم في هُدهُد قد تمت بنجاح..
<br>
     سوف نقوم بمراسلتكم قريبا مرة أخرى ونرسل لكم كافة بيانات تسجيل الدخول إلى نظام هُدهُد المحاسبي.
    نتمنى أن يكون هُدهُد خطوة نحو التقدم لكم.
<br></h5></div><div dir="ltr"><h4>
    فريق عمل هُدهُد
</h4> </div>""".format(association_name)
    try:
        frappe.sendmail(
            message=msg,
            recipients=[email],
            subject="مرحبا في هُدهُد",
            sender="hudhud.co.sa@gmail.com",
            delayed=False,
            as_markdown=True
        )
    except:
        frappe.response["message"] = _('{0} is not a valid Email address!', "ar").format(email),
        return

    return "okay", _("You will Receive an email with full details soon", "ar")
