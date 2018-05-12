from django.apps import apps as django_apps
from django.conf import settings
from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_rando.view_mixins import RandomizationListViewMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_model_wrapper import ModelWrapper
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import SubjectVisitModelWrapper
from ....model_wrappers import SubjectConsentModelWrapper
from ....model_wrappers import SubjectLocatorModelWrapper


class ActionItemModelWrapper(ModelWrapper):

    model = 'edc_action_item.actionitem'
    next_url_attrs = ['subject_identifier', 'ae_initial']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def ae_initial(self):
        if self.object.parent_reference_model == 'ambition_ae.aeinitial':
            mdl_cls = django_apps.get_model('ambition_ae', 'aeinitial')
            try:
                ae_initial = mdl_cls.objects.get(
                    subject_identifier=self.subject_identifier,
                    tracking_identifier=self.object.parent_reference_identifier)
                return ae_initial.pk
            except mdl_cls.DoesNotExist:
                pass
        elif self.object.parent_reference_model == 'ambition_ae.aefollowup':
            mdl_cls = django_apps.get_model('ambition_ae', 'aefollowup')
            try:
                ae_followup = mdl_cls.objects.get(
                        subject_identifier=self.subject_identifier,
                        tracking_identifier=self.object.parent_reference_identifier)
                return ae_followup.ae_initial.pk
            except mdl_cls.DoesNotExist:
                pass
        else:
            return None

class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        RandomizationListViewMixin,
        NavbarViewMixin, BaseDashboardView):

    action_item_model_wrapper_cls = ActionItemModelWrapper
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'ambition_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
