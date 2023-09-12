import pbr.version

KLY_QUOTA_API_VENDOR = "Troila Kunlun Cloud"
KLY_QUOTA_AP_PRODUCT = "Troila Kunlun Kly-quota-api"

version_info = pbr.version.VersionInfo('kly-quota-api')


def vendor_string():
    return KLY_QUOTA_API_VENDOR


def product_string():
    return KLY_QUOTA_API_VENDOR


def version_string_with_package():
    return version_info.version_string()

