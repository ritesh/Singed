import unittest
import pytest
from app.Singed import app, build_remote_url, is_whitelisted
from colorama import init, Fore, Back, Style


class SingedTestCases(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["API_KEY"] = "FOOBAR"
        self.app = app.test_client()
        pass

    def tearDown(self):
        pass


    # def set_scan_to_state(self, scan_id, state):
    #     rv = self.app.get('/api/testing/' + scan_id, data=dict(
    #         scanstate=state), )


    # def test_index_page(self):
    #     rv = self.app.get('/')
    #     #
    #     a = json.loads(rv.data)
    #     # This should probably be better
    #     assert a['api'] == 'version 1'


    def test_buildURLS(self):
        good_urls = [
            "br.api.pvp.net",
            "eune.api.pvp.net",
            "euw.api.pvp.net",
            "jp.api.pvp.net",
            "kr.api.pvp.net",
            "lan.api.pvp.net",
            "las.api.pvp.net",
            "na.api.pvp.net",
            "oce.api.pvp.net",
            "tr.api.pvp.net",
            "ru.api.pvp.net",
            "pbe.api.pvp.net",
            "global.api.pvp.net",
            "na.api.pvp.net/",
            "na.api.pvp.net/foo/"
        ]
        bad_urls = [
            "google.com",
            "hexplo.it",
            "riotkit.xyz",
            "geo.api.pvp.net",
            "oce.api.pvp.net.geo.com",
            "oce.api.pvp.net.pvp.net",
            "pvp.net",
            "",
            "/",
            "%00"
        ]

        for url in good_urls:
            new_url = build_remote_url(url, "".encode('utf-8'))
            if url.endswith("/"):
                assert new_url == "https://%s?api_key=%s" % (url,
                                                          app.config['API_KEY']
                                                          )
            else:
                assert new_url == "https://%s/?api_key=%s" % (url,
                                                          app.config['API_KEY']
                                                          )

        for url in good_urls:
            query_string = "foobar=Task&elon=musk"
            new_url = build_remote_url(url, query_string.encode('utf-8'))

            if url.endswith("/"):
                assert new_url == "https://%s?%s&api_key=%s" % (url,
                                                               query_string,
                                                          app.config['API_KEY']
                                                          )
            else:
                assert new_url == "https://%s/?%s&api_key=%s" % (url,
                                                                 query_string,
                                                          app.config['API_KEY']
                                                          ), print(new_url)

        for url in bad_urls:
            with pytest.raises(Exception) as err:
                new_url = build_remote_url(url, "".encode('utf-8'))
            assert err


    def test_whitelist(self):
        good_urls = [
            "br.api.pvp.net",
            "eune.api.pvp.net",
            "euw.api.pvp.net",
            "jp.api.pvp.net",
            "kr.api.pvp.net",
            "lan.api.pvp.net",
            "las.api.pvp.net",
            "na.api.pvp.net",
            "oce.api.pvp.net",
            "tr.api.pvp.net",
            "ru.api.pvp.net",
            "pbe.api.pvp.net",
            "global.api.pvp.net",
            "br.api.pvp.net/",
            "eune.api.pvp.net/",
            "euw.api.pvp.net/",
            "jp.api.pvp.net/",
            "kr.api.pvp.net/",
            "lan.api.pvp.net/",
            "las.api.pvp.net/",
            "na.api.pvp.net/",
            "oce.api.pvp.net/",
            "tr.api.pvp.net/",
            "ru.api.pvp.net/",
            "pbe.api.pvp.net/",
            "global.api.pvp.net/"
        ]
        bad_urls = [
            "google.com",
            "hexplo.it",
            "riotkit.xyz",
            "geo.api.pvp.net",
            "oce.api.pvp.net.geo.com",
            "oce.api.pvp.net.pvp.net",
            "pvp.net",
            "",
            "/",
            "%00"
        ]

        print("\nVerifying good URLS...\n")
        # Verify that good URLS are allowed
        for url in good_urls:
            url = 'https://%s' % url
            trust_result = is_whitelisted(url)
            print("[is_whitelisted] \"%s\", \tResult: %s%s%s" %
                      (url,
                       Fore.GREEN,
                       str(trust_result),
                       Fore.RESET
                       )
                  )
            assert trust_result == True

        print("\nVerifying bad URLS...\n")
        # Verify that bad URLS are denied
        for url in bad_urls:
            url = 'https://%s' % url
            trust_result = is_whitelisted(url)
            print("[is_whitelisted] \"%s\", \tResult: %s%s%s" %
                      (url,
                       Fore.GREEN,
                       str(trust_result),
                       Fore.RESET
                       )
                  )
            assert trust_result == False

if __name__ == '__main__':
    unittest.main()
