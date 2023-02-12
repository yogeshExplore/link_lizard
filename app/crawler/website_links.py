from app import logger, Setting, injected_services
from app.crawler import Crawler
from gevent import pool
import gevent
from urllib.parse import urlparse
import queue
import validators
from app.scraper.html_parser import parse_response
from app.services.lrequest.lizard_requests import LizardRequests


# todo add return types
# todo auth make sure right people are accessing it
# todo use session in request


class WebsiteLinks(Crawler):
    def __init__(self, name):
        super().__init__(name)
        self.base_url = Setting.BASE_URL
        self.host_name = urlparse(self.base_url).hostname
        self.q = queue.Queue()  # thread safe
        self.processed_urls = set()  # not thread safe
        self.origin_target_db = []  # not thread safe
        self.workers = pool.Pool(Setting.WORKERS)
        # todo should be passed by user
        self.canonical_host_name = {'bbc.com'}
        # todo ignore files
        self.ignore_file = {'.mp3', '.pdf'}

        # services ( todo Factory methods and dependency injection )
        self.lrequest = LizardRequests()
        self.store = injected_services.get_store_service()

    def link_to_url(self, url: str) -> str:
        if not url:
            return ''
        if url.startswith('http') or url.startswith('www'):
            url = url.replace('www.', '')
            url_details = urlparse(url)
            url_details = url_details._replace(scheme='http')
            if url_details.hostname != self.host_name:
                return ''
            else:
                url = url_details._replace(fragment='').geturl()
        else:
            url = f'{self.base_url}{url}' if url.startswith('/') else f'{self.base_url}/{url}'
            return self.link_to_url(url)  # to avoid links like #content

        is_valid = validators.url(url)
        if not is_valid:
            return ''

        return url.strip('/')

    """
    Just make get_links use gevent, because this is only I/O , Rest of the code mainly uses processing
    If we want to make rest of the part faster, we should use multiprocessing
    """
    def get_links(self, url):
        links = []
        is_response, response = self.lrequest.send_request(method='GET', url=url, s_codes=(200, 201))
        if is_response:
            html_response = parse_response(response)
            if html_response:
                links = [link.get('href') for link in html_response.find_all('a')]

        return url, links

    def run(self):
        logger.info(f"Running Crawler for base url {Setting.BASE_URL} with {Setting.WORKERS} workers")
        request_pool = pool.Pool(Setting.WORKERS)
        self.q.put(Setting.BASE_URL)
        self.processed_urls.add(Setting.BASE_URL)
        tasks = []
        tid = 0
        while not self.q.empty() or len(tasks) > 0:
            logger.info(f"QueueSize={self.q.qsize()}, PendingTasks={len(tasks)}, TasksSoFar={tid} "
                        f"UniqueSoFar={len(self.processed_urls)}, Requests={self.lrequest.total_count}")
            while len(tasks) <= Setting.WORKERS:
                try:
                    url = self.q.get(block=False)
                    tid += 1
                    tasks.append(request_pool.spawn(self.get_links, url))
                except queue.Empty:
                    logger.info(f"Queue is empty for now but tasks might be running, "
                                f"QueueSize={self.q.qsize()}, PendingTasks={len(tasks)}, TasksSoFar={tid}")
                    break
            completed_tasks = gevent.wait(tasks, count=1, timeout=None)
            if completed_tasks:
                completed_task = completed_tasks[0]
                completed_task.join()
                input_url, target_links = completed_task.value
                tasks.remove(completed_task)  # todo optimise this
                for link in target_links:
                    target_url = self.link_to_url(link)
                    if target_url:
                        if target_url not in self.processed_urls:
                            self.processed_urls.add(target_url)
                            self.q.put(target_url)
                            self.origin_target_db.append([input_url, target_url])
                            if len(self.origin_target_db) > Setting.BATCH_SIZE_DB_WRITE:
                                self.store.write(self.origin_target_db)
                                self.origin_target_db = []
        self.store.write(self.origin_target_db)
        logger.info(f"[ANALYSIS] Total unique urls = {len(self.processed_urls)}, "
                    f"Total task run = {tid}, "
                    f"Total requests made = {self.lrequest.total_count}"
                    )

        logger.info(f"[FINISH] Queue is empty and no more task pending. "
                    f"QueueSize={self.q.qsize()}, PendingTasks={len(tasks)}, TasksSoFar={tid}")

        try:
            assert self.q.qsize() == 0
            assert len(tasks) == 0
            assert len(request_pool.greenlets) == 0
        except AssertionError as ae:
            logger.error(f'Crawler does not finish as expected, error= {ae}')
            raise Exception(f"Queue={self.q.qsize()}, Tasks={len(tasks)}, Greenlets={len(request_pool.greenlets)}")


if __name__ == "__name__":
    WebsiteLinks("Links").run()
