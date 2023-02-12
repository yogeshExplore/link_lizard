from app import logger
import requests
import time
from app.services.lrequest import Lrequest
from app.services.proxy.fake import Fake
from app.services.proxy.free import Free
from app.services.proxy.oxylabs import Oxylabs


# todo check Adapter retry, pass kwargs
# todo make it class to implement different kind of request structure for different scraper may be
# todo push error url into error files
class LizardRequests(Lrequest):
    def __init__(self):
        super().__init__()
        self.total_count = 0
        self.proxy_services = [Fake(), Free(), Oxylabs()]

    def send_request(self, method, url, s_codes: tuple, count=0, sleep=False):
        response = None
        if count < len(self.proxy_services):
            try:
                self.total_count += 1
                logger.info(f'[REQUEST][{count}] {url}')
                response = requests.request(
                    method, url=url, headers=self.headers, cookies=self.cookies,
                    proxies=self.proxy_services[count].get_proxy())
                logger.info(f'[RESPONSE][{count}] {url} {response}')
                if response.status_code in s_codes:
                    return True, response
                else:
                    logger.warning(f'[REQUEST][{count}] {url}, e=HTTP code not in s_codes, r={response}')
                    count += 1
                    if sleep:
                        time.sleep(2 ** count)
                    return self.send_request(method, url, s_codes, count, sleep)

            except Exception as e:
                logger.warning(f'[REQUEST][{count}] {url}, e={e}, r={response}', exc_info=True)
                count += 1
                if sleep:
                    time.sleep(2 ** count)
                return self.send_request(method, url, s_codes, count, sleep)

        logger.error(f'[REQUEST] Failed to get proper response for {url}')
        return False, response
