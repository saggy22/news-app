from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import ResearchPagesModel


class ContentResearchPage(TemplateView):
    template_name = 'research/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        name = kwargs.get('name')

        if name and '_' in name or any(x.isupper() for x in name):
            name = name.replace('_', '-')
            ctx['redirect'] = name.lower()
        else:
            try:
                ctx['m'] = ResearchPagesModel.objects.get(url=kwargs.get('name').lower())
            except ResearchPagesModel.DoesNotExist:
                raise Http404
        ctx['colorsarray'] = ['primary', 'info', 'danger', 'success', 'warning']
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if context.get('redirect', None):
            return redirect('page', name=context.get('redirect'), permanent=True)
        return super().render_to_response(context, **response_kwargs)

