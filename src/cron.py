import threading

from flask_crontab import Crontab
import logging
import datetime
from app import app, instagram
from modules import get_hashtags_to_check, get_or_create_hashtag_check

crontab = Crontab(app)


@crontab.job(minute="0", hour="12")
def refresh_hashtags_to_check():
    logging.info(f"Starting refresh job at {datetime.datetime.now()}")
    if not instagram.status():
        logging.error("Not logged in")
        return 1
    hashtags_to_check = get_hashtags_to_check()
    requests = [threading.Thread(target=get_or_create_hashtag_check, kwargs={"name": h.name, "refresh": True}) for h in
                hashtags_to_check]
    for r in requests:
        r.start()
    for r in requests:
        r.join()
    logging.info("End of refresh job.")
    logging.info(f"Refreshed {len(requests)} hashtags : {', '.join([h.name for h in hashtags_to_check])}.")
