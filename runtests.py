#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname


app_name = 'ambition_dashboard'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    EDC_BOOTSTRAP=3,
    SUBJECT_VISIT_MODEL="ambition_subject.subjectvisit",
    SUBJECT_REQUISITION_MODEL="ambition_subject.subjectrequisition",
    SUBJECT_CONSENT_MODEL='ambition_subject.subjectconsent',
    RANDOMIZATION_LIST_PATH=os.path.join(
        base_dir, app_name, "tests", "test_randomization_list.csv"),
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_adverse_event.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_metadata_rules.apps.AppConfig",
        "edc_model_wrapper.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        "edc_pharmacy_dashboard.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_review_dashboard.apps.AppConfig",
        "edc_subject_dashboard.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "ambition_ae.apps.AppConfig",
        "ambition_labs.apps.AppConfig",
        "ambition_lists.apps.AppConfig",
        "ambition_prn.apps.AppConfig",
        "ambition_rando.apps.AppConfig",
        "ambition_reference.apps.AppConfig",
        "ambition_screening.apps.AppConfig",
        "ambition_subject.apps.AppConfig",
        "ambition_visit_schedule.apps.AppConfig",
        "ambition_dashboard.apps.EdcProtocolAppConfig",
        "ambition_dashboard.apps.EdcAppointmentAppConfig",
        "ambition_dashboard.apps.EdcFacilityAppConfig",
        "ambition_dashboard.apps.EdcIdentifierAppConfig",
        "ambition_dashboard.apps.EdcMetadataAppConfig",
        "ambition_dashboard.apps.EdcVisitTrackingAppConfig",
        "ambition_dashboard.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=True, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
