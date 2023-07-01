from fake_useragent import UserAgent

class Config:
    HEADERS = {
            "User-Agent": UserAgent().random,
            }
    EXCLUDE_SCRIPTS = ["vue", "jquery"]
