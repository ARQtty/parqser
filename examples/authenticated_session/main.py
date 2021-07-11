from parqser.scrapper import BatchParallelScrapper
from parqser.parser import HTMLParser
from parqser.saver import CSVSaver
import web_components
from grouple_session import GroupleSession, read_spaceproxy_file


def make_sessions(username, password, n_sessions):
    sessions = [GroupleSession() for _ in range(n_sessions)]
    for sess in sessions:
        sess.auth(username, password)
    return sessions


if __name__ == '__main__':
    N_JOBS = 2

    proxies = read_spaceproxy_file('./expired_proxies.txt')

    urls = ['https://readmanga.live/alice_in_murderland',
            'https://readmanga.live/buntar_liudvig',
            'https://readmanga.live/nocturnal_lover_specialty_store__bloodhound',
            'https://readmanga.live/count_cain_saga',
            'https://readmanga.live/chernaia_roza_alisy',
            'https://readmanga.live/x_day',
            'https://readmanga.live/puberty_bitter_change']

    username, password = open('secret.txt').readline().split()
    sessions = make_sessions(username, password, N_JOBS)

    saver = CSVSaver('./parsed_info.csv')
    parser = HTMLParser.from_module(web_components)
    crawler = BatchParallelScrapper(n_jobs=N_JOBS, interval_ms=1000)
    for url_batch in crawler.batch_urls(urls):
        loaded = crawler.load_pages(url_batch)

        print(' '.join([page.status.name for page in loaded]))
        parsed = [parser.parse(page) for page in loaded]
        parsed = [page.to_dict() for page in parsed]
        saver.save_batch(parsed)
        crawler.wait()
