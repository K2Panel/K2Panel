# coding: utf-8
# -------------------------------------------------------------------
# K2Panel
# -------------------------------------------------------------------
# Copyright (c) 2015-2019 K2Panel(binarjoinanalyticnl.nl) All rights reserved.
# -------------------------------------------------------------------
# Author: hwliang <hwl@binarjoinanalyticnl.nl>
# -------------------------------------------------------------------

# ------------------------------
# AUTH STUB - License System Removed
# نظام المصادقة - تم إزالة نظام الترخيص القديم
# ------------------------------

import public, time, json, os

try:
    from BTPanel import cache, session
except:
    pass


class panelAuth:
    """
    نظام المصادقة - تم استبداله بـ Stubs
    نظام الترخيص القديم تم إزالته، هذه الوظائف تُرجع قيماً افتراضية محلية
    """
    
    __product_list_path = "data/product_list.pl"
    __product_bay_path = "data/product_bay.pl"
    __product_id = "100000011"
    __official_url = ""  # تم تعطيل الاتصال بالخادم الخارجي

    def create_serverid(self, get):
        """
        STUB: Returns local server ID without cloud verification
        إرجاع معرف الخادم المحلي بدون التحقق من السحابة
        """
        try:
            # إنشاء معرف خادم محلي بسيط
            s1 = public.get_mac_address() + public.get_hostname()
            s2 = public.ExecShell("cat /proc/cpuinfo|grep 'model name'|cut -d : -f2")[0].strip()
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
        return public.return_msg_gettext(
            False, 
            public.lang("Plugin ordering system has been disabled. This will be replaced with new system.")
        )

    def get_order_stat(self, get):
        """STUB: Order status disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Order system has been disabled.")
        )

    def check_serverid(self, get):
        """STUB: Always returns True (no verification)"""
        return True

    def get_plugin_price(self, get):
        """STUB: Returns empty price list"""
        return public.return_msg_gettext(
            False,
            public.lang("Plugin pricing system has been disabled. All plugins are now free to install.")
        )

    def get_plugin_info(self, pluginName):
        """STUB: Returns None"""
        return None

    def get_plugin_list(self, get):
        """STUB: Returns empty list"""
        return []

    def get_buy_code(self, get):
        """STUB: Purchase system disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Purchase system has been disabled.")
        )

    def get_stripe_session_id(self, get):
        """STUB: Payment disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Payment system has been disabled.")
        )

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
        return public.return_msg_gettext(
            False,
            public.lang("Payment verification has been disabled.")
        )

    def flush_pay_status(self, get):
        """STUB: No-op"""
        return public.return_msg_gettext(
            True,
            public.lang("Status flushed (local only)")
        )

    def get_renew_code(self):
        """STUB: No-op"""
        pass

    def check_renew_code(self):
        """STUB: No-op"""
        pass

    def get_business_plugin(self, get):
        """STUB: Returns empty plugin list"""
        return []

    def get_ad_list(self):
        """STUB: No-op"""
        pass

    def check_plugin_end(self):
        """STUB: No-op"""
        pass

    def get_re_order_status_plugin(self, get):
        """STUB: Order status disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Order system has been disabled.")
        )

    def get_voucher_plugin(self, get):
        """STUB: Voucher system disabled"""
        return []

    def create_order_voucher_plugin(self, get):
        """STUB: Voucher activation disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Voucher system has been disabled.")
        )

    def send_cloud(self, cloudURL, params):
        """
        STUB: Cloud communication disabled
        تم تعطيل الاتصال بالخوادم الخارجية
        """
        return None

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
        return public.return_msg_gettext(
            False,
            public.lang("Authorization system has been disabled.")
        )

    def renew_product_auth(self, get):
        """STUB: Product renewal disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Renewal system has been disabled.")
        )

    def free_trial(self, get):
        """STUB: Free trial disabled"""
        return public.return_msg_gettext(
            False,
            public.lang("Trial system has been disabled.")
        )

    def get_plugin_remarks(self, get):
        """STUB: Plugin remarks disabled"""
        return public.returnMsg(
            False,
            public.lang("Plugin information system has been disabled.")
        )
