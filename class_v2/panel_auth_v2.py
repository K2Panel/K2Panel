# coding: utf-8
# -------------------------------------------------------------------
# K2Panel
# -------------------------------------------------------------------
# Copyright (c) 2015-2019 K2Panel(binarjoinanalyticnl.nl) All rights reserved.
# -------------------------------------------------------------------
# Author: hwliang <hwl@binarjoinanalyticnl.nl>
# -------------------------------------------------------------------

# ------------------------------
# AUTH STUB V2 - License System Removed
# نظام المصادقة V2 - تم إزالة نظام الترخيص القديم
# ------------------------------

import public, time, json, os
from BTPanel import session, cache
from public.validate import Param


class panelAuth:
    """
    نظام المصادقة V2 - تم استبداله بـ Stubs
    نظام الترخيص القديم تم إزالته، هذه الوظائف تُرجع قيماً افتراضية محلية
    """
    
    __request_url = None
    __product_list_path = 'data/product_list.pl'
    __product_bay_path = 'data/product_bay.pl'
    __product_id = '100000011'
    __official_url = ""  # تم تعطيل الاتصال بالخادم الخارجي
    __failed_connect_server = 'Failed to connect to the server!'

    def create_serverid(self, get):
        """
        STUB: Returns local server ID without cloud verification
        إرجاع معرف الخادم المحلي بدون التحقق من السحابة
        """
        try:
            # إنشاء معرف خادم محلي بسيط
            s1 = public.get_mac_address() + public.get_hostname()
            s2 = self.get_cpuname()
            serverid = public.md5(s1) + public.md5(s2)
            
            # إرجاع بيانات محلية بسيطة
            return {
                'id': 0,
                'uid': 0,
                'server_id': serverid,
                'token': 'local_token_' + serverid[:16],
                'username': 'local_user'
            }
        except:
            return {
                'id': 0,
                'uid': 0,
                'server_id': 'local_server',
                'token': 'local_token',
                'username': 'local_user'
            }

    def create_plugin_other_order(self, get):
        """STUB: Plugin ordering disabled"""
        return public.return_message(-1, 0, public.lang("Plugin ordering system has been disabled."))

    def get_order_stat(self, get):
        """STUB: Order status disabled"""
        return public.return_message(-1, 0, public.lang("Order system has been disabled."))

    def check_serverid(self, get):
        """STUB: Always returns True (no verification)"""
        return public.return_message(0, 0, True)

    def get_plugin_price(self, get):
        """STUB: Returns empty price list"""
        return public.return_message(-1, 0, public.lang("Plugin pricing system has been disabled. All plugins are now free."))

    def get_plugin_info(self, pluginName):
        """STUB: Returns None"""
        return None

    def get_plugin_list(self, get):
        """STUB: Returns empty list"""
        return public.return_message(0, 0, [])

    def get_buy_code(self, get):
        """STUB: Purchase system disabled"""
        return public.return_message(-1, 0, public.lang("Purchase system has been disabled."))

    def get_stripe_session_id(self, get):
        """STUB: Payment disabled"""
        return public.return_message(-1, 0, public.lang("Payment system has been disabled."))

    def get_paypal_session_id(self, get):
        """STUB: PayPal disabled"""
        return {
            "status": False,
            "res": "Payment system disabled",
            "nonce": 0,
        }

    def check_paypal_status(self, get):
        """STUB: PayPal status disabled"""
        return {
            "status": False,
            "res": "Payment system disabled",
            "nonce": 0,
        }

    def check_pay_status(self, get):
        """STUB: Payment status always false"""
        return public.return_message(-1, 0, public.lang("Payment verification has been disabled."))

    def flush_pay_status(self, get):
        """STUB: No-op"""
        return public.return_message(0, 0, public.lang("Status flushed (local only)"))

    def get_renew_code(self):
        """STUB: No-op"""
        pass

    def check_renew_code(self):
        """STUB: No-op"""
        pass

    def get_business_plugin(self, get):
        """STUB: Returns empty plugin list"""
        return public.return_message(0, 0, [])

    def get_ad_list(self):
        """STUB: No-op"""
        pass

    def check_plugin_end(self):
        """STUB: No-op"""
        pass

    def get_re_order_status_plugin(self, get):
        """STUB: Order status disabled"""
        return public.return_message(-1, 0, public.lang("Order system has been disabled."))

    def get_voucher_plugin(self, get):
        """STUB: Voucher system disabled"""
        return []

    def create_order_voucher_plugin(self, get):
        """STUB: Voucher activation disabled"""
        return public.return_message(-1, 0, public.lang("Voucher system has been disabled."))

    def send_cloud(self, cloudURL, params):
        """
        STUB: Cloud communication disabled
        تم تعطيل الاتصال بالخوادم الخارجية
        """
        return public.return_message(-1, 0, "Cloud communication has been disabled")

    def send_cloud_pro(self, module, params):
        """
        STUB: Cloud communication disabled
        تم تعطيل الاتصال بالخوادم الخارجية
        """
        return None

    def get_voucher(self, get):
        """STUB: Voucher disabled"""
        return None

    def get_order_status(self, get):
        """STUB: Order status disabled"""
        return None

    def get_product_discount_by(self, get):
        """STUB: Discount system disabled"""
        return None

    def get_re_order_status(self, get):
        """STUB: Reorder disabled"""
        return None

    def create_order_voucher(self, get):
        """STUB: Voucher creation disabled"""
        return None

    def create_order(self, get):
        """STUB: Order creation disabled"""
        return None

    def get_cpuname(self):
        """Helper: Returns CPU name (kept for compatibility)"""
        try:
            return public.ExecShell("cat /proc/cpuinfo|grep 'model name'|cut -d : -f2")[0].strip()
        except:
            return "Unknown CPU"

    def get_product_auth(self, get):
        """STUB: Product authorization disabled"""
        return []

    def auth_activate(self, get):
        """STUB: Authorization activation disabled"""
        return public.return_message(-1, 0, public.lang("Authorization system has been disabled."))

    def renew_product_auth(self, get):
        """STUB: Product renewal disabled"""
        return public.return_message(-1, 0, public.lang("Renewal system has been disabled."))

    def free_trial(self, get):
        """STUB: Free trial disabled"""
        return public.return_message(-1, 0, public.lang("Trial system has been disabled."))

    def get_plugin_remarks(self, get):
        """STUB: Plugin remarks disabled"""
        return public.returnMsg(False, public.lang("Plugin information system has been disabled."))

    def get_serverid(self):
        """
        STUB: Returns local server ID
        إرجاع معرف الخادم المحلي
        """
        try:
            s1 = public.get_mac_address() + public.get_hostname()
            s2 = self.get_cpuname()
            serverid = public.md5(s1) + public.md5(s2)
            return serverid
        except:
            return 'local_server_id'

    def get_stripe_checkout_session(self, get):
        """STUB: Stripe checkout disabled"""
        return public.return_message(-1, 0, public.lang("Stripe checkout has been disabled."))

    def get_order_list(self, get):
        """STUB: Order list disabled"""
        return public.return_message(0, 0, {"list": [], "total": 0})

    def cancel_order(self, get):
        """STUB: Order cancellation disabled"""
        return public.return_message(-1, 0, public.lang("Order cancellation has been disabled."))

    def get_user_info(self, get):
        """STUB: User info - returns local info"""
        return public.return_message(0, 0, self.create_serverid(get))

    def logout_account(self, get):
        """STUB: Logout - local only"""
        return public.return_message(0, 0, "Logged out locally")

    def check_product_discount_list(self, get):
        """STUB: Discount list disabled"""
        return public.return_message(0, 0, [])

    def get_recommend_product(self, get):
        """STUB: Product recommendations disabled"""
        return public.return_message(0, 0, [])
