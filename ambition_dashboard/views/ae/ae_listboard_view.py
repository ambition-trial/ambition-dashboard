import arrow

from ambition_ae.action_items import AE_INITIAL_ACTION
from ambition_ae.models import AeInitial
from ambition_ae.reports import AEReport
from ambition_dashboard.model_wrappers import DeathReportModelWrapper
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.model_wrappers import (
    ActionItemModelWrapper as BaseActionItemModelWrapper,
)
from edc_dashboard.view_mixins import (
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
)
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin


class ActionItemModelWrapper(BaseActionItemModelWrapper):
    next_url_name = "ae_listboard_url"
    death_report_model = "ambition_prn.deathreport"

    def __init__(self, model_obj=None, **kwargs):
        self._death_report = None
        super().__init__(model_obj=model_obj, **kwargs)

    @property
    def death_report(self):
        if not self._death_report:
            model_cls = django_apps.get_model(self.death_report_model)
            try:
                self._death_report = DeathReportModelWrapper(
                    model_obj=model_cls.objects.get(
                        subject_identifier=self.subject_identifier
                    )
                )
            except ObjectDoesNotExist:
                self._death_report = None
        return self._death_report


class AeListboardView(
    NavbarViewMixin,
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):

    listboard_template = "ae_listboard_template"
    listboard_url = "ae_listboard_url"
    listboard_panel_style = "warning"
    listboard_fa_icon = None
    listboard_model = "edc_action_item.actionitem"
    listboard_panel_title = "AE Initial and Follow-up Reports"
    listboard_view_permission_codename = "edc_dashboard.view_ae_listboard"

    model_wrapper_cls = ActionItemModelWrapper
    navbar_name = "ambition_dashboard"
    navbar_selected_item = "ae_home"
    ordering = "-report_datetime"
    paginate_by = 25
    search_form_url = "ae_listboard_url"
    action_type_names = [AE_INITIAL_ACTION]

    search_fields = [
        "subject_identifier",
        "action_identifier",
        "parent_action_item__action_identifier",
        "related_action_item__action_identifier",
        "user_created",
        "user_modified",
    ]

    def get(self, request, *args, **kwargs):
        if request.GET.get("pdf"):
            response = self.print_pdf_report(
                action_identifier=self.request.GET.get("pdf"), request=request
            )
            return response or super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def print_pdf_report(self, action_identifier=None, request=None):
        try:
            ae_initial = AeInitial.objects.get(action_identifier=action_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            report = AEReport(
                ae_initial=ae_initial,
                subject_identifier=ae_initial.subject_identifier,
                user=self.request.user,
                request=request,
            )
            return report.render()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["AE_INITIAL_ACTION"] = AE_INITIAL_ACTION
        context["utc_date"] = arrow.now().date()
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update(action_type__name__in=self.action_type_names)
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return options

    def get_updated_queryset(self, queryset):
        pks = []
        for obj in queryset:
            try:
                obj.reference_obj
            except ObjectDoesNotExist:
                pks.append(obj.pk)
        return queryset.exclude(pk__in=pks)
