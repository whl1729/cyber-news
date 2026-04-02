from news.crawler.ai import addy_osmani_blog_crawler
from news.crawler.ai import antirez_blog_crawler
from news.crawler.ai import armin_ronacher_blog_crawler
from news.crawler.ai import baoyu_blog_crawler
from news.crawler.ai import bassim_eledath_blog_crawler
from news.crawler.ai import chip_huyen_blog_crawler
from news.crawler.ai import chris_gregori_blog_crawler
from news.crawler.ai import claude_code_blog_crawler
from news.crawler.ai import deepmind_blog_crawler
from news.crawler.ai import dhh_blog_crawler
from news.crawler.ai import han_not_solo_blog_crawler
from news.crawler.ai import harrison_chase_blog_crawler
from news.crawler.ai import huggingface_blog_crawler
from news.crawler.ai import karpathy_blog_crawler
from news.crawler.ai import mario_zechner_blog_crawler
from news.crawler.ai import matt_shumer_blog_crawler
from news.crawler.ai import one_useful_thing_blog_crawler
from news.crawler.ai import openai_news_crawler
from news.crawler.ai import philipp_schmid_blog_crawler
from news.crawler.ai import pragmatic_engineer_blog_crawler
from news.crawler.ai import rob_zolkos_blog_crawler
from news.crawler.ai import ryan_dahl_blog_crawler
from news.crawler.ai import sam_altman_blog_crawler
from news.crawler.ai import sean_goedecke_blog_crawler
from news.crawler.ai import sebastian_raschka_blog_crawler
from news.crawler.ai import simon_willison_blog_crawler
from news.crawler.ai import uwe_friedrichsen_blog_crawler
from news.crawler.ai import yohei_nakajima_blog_crawler
from news.util.configer import get_enabled_topics
from news.util.logger import logger


def crawl():
    crawlers = {
        "claude_code_blog": claude_code_blog_crawler,
        "openai_news": openai_news_crawler,
        "karpathy_blog": karpathy_blog_crawler,
        "chip_huyen_blog": chip_huyen_blog_crawler,
        "sebastian_raschka_blog": sebastian_raschka_blog_crawler,
        "simon_willison_blog": simon_willison_blog_crawler,
        "harrison_chase_blog": harrison_chase_blog_crawler,
        "yohei_nakajima_blog": yohei_nakajima_blog_crawler,
        "deepmind_blog": deepmind_blog_crawler,
        "huggingface_blog": huggingface_blog_crawler,
        "baoyu_blog": baoyu_blog_crawler,
        "sam_altman_blog": sam_altman_blog_crawler,
        "mario_zechner_blog": mario_zechner_blog_crawler,
        "dhh_blog": dhh_blog_crawler,
        "armin_ronacher_blog": armin_ronacher_blog_crawler,
        "antirez_blog": antirez_blog_crawler,
        "ryan_dahl_blog": ryan_dahl_blog_crawler,
        "pragmatic_engineer_blog": pragmatic_engineer_blog_crawler,
        "sean_goedecke_blog": sean_goedecke_blog_crawler,
        "philipp_schmid_blog": philipp_schmid_blog_crawler,
        "matt_shumer_blog": matt_shumer_blog_crawler,
        "bassim_eledath_blog": bassim_eledath_blog_crawler,
        "rob_zolkos_blog": rob_zolkos_blog_crawler,
        "chris_gregori_blog": chris_gregori_blog_crawler,
        "addy_osmani_blog": addy_osmani_blog_crawler,
        "uwe_friedrichsen_blog": uwe_friedrichsen_blog_crawler,
        "one_useful_thing_blog": one_useful_thing_blog_crawler,
        "han_not_solo_blog": han_not_solo_blog_crawler,
    }

    enabled_topics = get_enabled_topics()
    for topic, crawler in crawlers.items():
        if enabled_topics is None or topic in enabled_topics:
            crawler.crawl()
        else:
            logger.info(f"Skipping {topic} (not in enabled_topics)")


if __name__ == "__main__":
    crawl()
