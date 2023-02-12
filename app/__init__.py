from app.config import Config
from app.setting import Setting
from app_logging import logger
from gevent import monkey
from app.services import Service

injected_services = Service()
# todo may be pass crawler type and call the class dynamically if it is going to scale to make different kind of scraper

if __name__ == "__main__":
    logger.info(f"[START]: {Config.APP_NAME} running in {Config.ENVIRONMENT} mode in {Setting.PROJECT_BASE_DIR}")
    # todo initiate dynamically
    if Setting.CRAWLER_TYPE == 'website_links':
        # todo factory class and dependency injection
        if Setting.WORKERS > 1:
            monkey.patch_all()
        # inject store service
        injected_services.set_store_service(Setting.OUTPUT)
        from crawler import website_links
        wl = website_links.WebsiteLinks(Setting.CRAWLER_TYPE)
        wl.run()
    else:
        logger.info("Crawler not implemented")
