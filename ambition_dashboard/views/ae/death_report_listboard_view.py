import arrow

from ambition_prn.constants import DEATH_REPORT_ACTION
from ambition_prn.models import DeathReport as DeathReportModel
from ambition_prn.reports import DeathReport
from edc_action_item.model_wrappers import (
    ActionItemModelWrapper as BaseActionItemModelWrapper,
)
from edc_dashboard.view_mixins import EdcViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from django.core.exceptions import ObjectDoesNotExist


class ActionItemModelWrapper(BaseActionItemModelWrapper):
    next_url_name = "death_report_listboard_url"
    death_report_model = "ambition_prn.deathreport"

    def __init__(self, model_obj=None, **kwargs):
        self._death_report = None
        super().__init__(model_obj=model_obj, **kwargs)


class DeathReportListboardView(
    NavbarViewMixin,
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):

    listboard_template = "death_report_listboard_template"
    listboard_url = "death_report_listboard_url"
    listboard_panel_style = "warning"
    # listboard_fa_icon = "fa-heartbeat"
    listboard_model = "edc_action_item.actionitem"
    listboard_panel_title = "Death Reports"
    listboard_view_permission_codename = "edc_dashboard.view_ae_listboard"
    listboard_fa_icon = None

    model_wrapper_cls = ActionItemModelWrapper
    navbar_name = "ambition_dashboard"
    navbar_selected_item = "ae_home"
    ordering = "-report_datetime"
    paginate_by = 25
    search_form_url = "death_report_listboard_url"
    action_type_names = [DEATH_REPORT_ACTION]

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
            return response
        return super().get(request, *args, **kwargs)

    def print_pdf_report(self, action_identifier=None, request=None):
        try:
            death_report = DeathReportModel.objects.get(
                action_identifier=action_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            report = DeathReport(
                death_report=death_report,
                subject_identifier=death_report.subject_identifier,
                user=self.request.user,
                request=request,
            )
            return report.render()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["DEATH_REPORT_ACTION"] = DEATH_REPORT_ACTION
        context["utc_date"] = arrow.now().date()
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update(action_type__name__in=self.action_type_names)
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return options
