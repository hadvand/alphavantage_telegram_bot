from site_api.utils.api_handler import SiteApiInterface
from settings import SiteSettings

site = SiteSettings()
url = "https://" + site.api_host
querystring = {
    "symbol": 'IBM',
    "function": 'GLOBAL_QUOTE',
}
headers = {
    "X-RapidAPI-Key": site.api_key.get_secret_value(),
    "X-RapidAPI-Host": site.api_host
}
site_api = SiteApiInterface()
