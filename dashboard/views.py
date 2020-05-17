from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, ListView

from pages.models import PagesModel, page_meta_type, page_firstline_type
from pages.models import PagesModel
from research.models import ResearchPagesModel


class DashBoardIndex(TemplateView):
    template_name = 'dashboard/index.html'


class PageListView(ListView):
    template_name = 'dashboard/pages_list.html'
    model = PagesModel

    def get_queryset(self):
        return PagesModel.objects.filter()[:10]


class PageEditView(PermissionRequiredMixin, TemplateView):
    template_name = 'dashboard/pages_edit.html'
    permission_required = 'profile.can_edit_page'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        try:
            ctx['obj'] = PagesModel.objects.get(url=kwargs.get('name').lower())
        except PagesModel.DoesNotExist:
            raise Http404
        return ctx

    def post(self, request, *args, **kwargs):
        non_list_keys = ['custom_footer', 'custom_header', 'page_references']
        obj = PagesModel.objects.get(url=kwargs.get('name').lower())

        page_meta = page_meta_type()
        firstline = page_firstline_type()

        for k in request.POST.keys():
            if k in non_list_keys:
                setattr(obj, k, request.POST.get(k))
            elif 'firstline' in k:
                key = k.replace("firstline_","")
                if key == "categories" or key == "apps":
                    try:
                        firstline[key] = eval(request.POST.get(k))
                    except Exception as e:
                        pass
                else:
                    try:
                        firstline[key] = request.POST.get(k)
                    except Exception as e:
                        pass

            elif 'page_meta' in k:
                key = k.replace("page_meta_","")
                if key == "meta_keywords" or key == "other_languages":
                    try:
                        page_meta[key] = eval(request.POST.get(k))
                    except Exception as e:
                        pass
                else:
                    try:
                        page_meta[key] = request.POST.get(k)
                    except Exception as e:
                        pass
            else:
                key = k.split("_")
                if len(key) == 3:
                    if key[1] == 'context':
                        try:
                            setattr(getattr(obj, key[0])[int(key[2]) - 1], "w{}".format(key[1]), eval(request.POST.get(k)))
                        except Exception as e:
                            pass
                    else:
                        try:
                            setattr(getattr(obj, key[0])[int(key[2])-1], "w{}".format(key[1]), request.POST.get(k))
                        except Exception as e:
                            pass
        obj.page_meta = page_meta
        obj.firstline = firstline
        obj.save()

        return HttpResponseRedirect(self.request.path)


class ResearchPageListView(ListView):
    template_name = 'dashboard/research_pages_list.html'
    model = ResearchPagesModel

    def get_queryset(self):
        return ResearchPagesModel.objects.filter()[:10]


class ResearchPageEditView(PermissionRequiredMixin, TemplateView):
    template_name = 'dashboard/research_pages_edit.html'
    permission_required = 'profile.can_edit_research_page'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        try:
            ctx['obj'] = ResearchPagesModel.objects.get(url=kwargs.get('name').lower())
        except ResearchPagesModel.DoesNotExist:
            raise Http404
        return ctx

    def post(self, request, *args, **kwargs):
        non_list_keys = ['custom_footer', 'custom_header']
        obj = ResearchPagesModel.objects.get(url=kwargs.get('name').lower())
        for k in request.POST.keys():
            if k in non_list_keys:
                setattr(obj, k, request.POST.get(k))
            else:
                key = k.split("_")
                if len(key) == 3:
                    if key[1] == 'context':
                        try:
                            setattr(getattr(obj, key[0])[int(key[2]) - 1], "w{}".format(key[1]), eval(request.POST.get(k)))
                        except Exception as e:
                            pass
                    else:
                        try:
                            setattr(getattr(obj, key[0])[int(key[2])-1], "w{}".format(key[1]), request.POST.get(k))
                        except Exception as e:
                            pass
        obj.save()

        return HttpResponseRedirect(self.request.path)
