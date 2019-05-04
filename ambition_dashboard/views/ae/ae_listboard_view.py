import arrow

from ambition_ae.action_items import AE_INITIAL_ACTION
from edc_dashboard.view_mixins import EdcViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import ActionItemModelWrapper
from ambition_ae.reports.ae_report import AEReport
from ambition_ae.models.ae_initial import AeInitial


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
    listboard_fa_icon = "fa-heartbeat"
    listboard_model = "edc_action_item.actionitem"
    listboard_panel_title = "AE Initial Reports"
    listboard_view_permission_codename = "edc_dashboard.view_ae_listboard"

    model_wrapper_cls = ActionItemModelWrapper
    navbar_name = "ambition_dashboard"
    navbar_selected_item = "ae"
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
            response = self.print_ae_report(
                action_identifier=self.request.GET.get("pdf"))
            return response
        return super().get(request, *args, **kwargs)

    def print_ae_report(self, action_identifier):
        ae_initial = AeInitial.objects.get(action_identifier=action_identifier)
        report = AEReport(ae_initial=ae_initial, user=self.request.user)
        return report.render()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["AE_INITIAL_ACTION"] = AE_INITIAL_ACTION
        context["utc_date"] = arrow.now().date()
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update(action_type__name__in=self.action_type_names)
        if kwargs.get("subject_identifier"):
            options.update(
                {"subject_identifier": kwargs.get("subject_identifier")})
        return options
