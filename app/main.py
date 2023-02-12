from app import logger, Setting, injected_services
from gevent import monkey


if __name__ == "__main__":
    # todo initiate dynamically
    if Setting.CRAWLER_TYPE == 'website_links':
        # todo factory class and dependency injection
        # This makes the debugging very easy, if workers == 1, gevent monkey patch is not applied
        if Setting.WORKERS > 1:
            monkey.patch_all()
        # injecting store service
        injected_services.set_store_service(Setting.OUTPUT)
        from app.crawler import website_links
        wl = website_links.WebsiteLinks(Setting.CRAWLER_TYPE)
        wl.run()
    else:
        logger.info("Crawler not implemented")
