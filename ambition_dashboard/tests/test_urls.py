import sys

from ambition_sites import ambition_sites
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin
from selenium.webdriver.firefox.webdriver import WebDriver

style = color_style()


@override_settings(DEBUG=True)
class MySeleniumTests(SiteTestCaseMixin, SeleniumLoginMixin, SeleniumModelFormMixin,
                      StaticLiveServerTestCase):

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    extra_url_names = ['home_url', 'administration_url']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        url_names = (self.extra_url_names
                     + list(settings.DASHBOARD_URL_NAMES.values()))
        self.url_names = list(set(url_names))

    def test_follow_urls(self):
        """Follows any url that can be reversed without kwargs.
        """
        self.login()
        sys.stdout.write(
            'Following any url that can be reversed without kwargs.')
        for url_name in self.url_names:
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                sys.stdout.write(style.ERROR(f'NoReverseMatch: {url_name}\n'))
            else:
                sys.stdout.write(style.SUCCESS(f'{url_name} {url}\n'))
                self.selenium.get('%s%s' % (self.live_server_url, url))
                self.selenium.implicitly_wait(2)
