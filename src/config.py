import os

CREATE_VNET_PASSWORD = os.getenv("CREATE_VNET_PASSWORD")
if not CREATE_VNET_PASSWORD:
    raise Exception("CREATE_VNET_PASSWORD not set in .env")


TENDERLY_ACCESS_TOKEN = os.getenv("TENDERLY_ACCESS_TOKEN")
if not TENDERLY_ACCESS_TOKEN:
    raise Exception("TENDERLY_ACCESS_TOKEN not set in .env")

HEADERS = {
    "Content-Type": "application/json",
    "X-Access-Key": TENDERLY_ACCESS_TOKEN,
}

ACCOUNT_SLUG = os.getenv("ACCOUNT_SLUG")
if not ACCOUNT_SLUG:
    raise Exception("ACCOUNT_SLUG not set in .env")

PROJECT_SLUG = os.getenv("PROJECT_SLUG")
if not PROJECT_SLUG:
    raise Exception("PROJECT_SLUG not set in .env")

VNET_FILE = "vnet_mapping.json"
