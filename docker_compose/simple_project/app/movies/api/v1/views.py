from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        movies = self.model.objects.prefetch_related('genre', 'person').values().annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', distinct=True,
                            filter=Q(personfilmwork__role='actor')),
            directors=ArrayAgg('persons__full_name', distinct=True,
                               filter=Q(personfilmwork__role='director')),
            writers=ArrayAgg('persons__full_name', distinct=True,
                             filter=Q(personfilmwork__role='writer')))
        return movies

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return MoviesApiMixin.get_queryset(self, **kwargs)

    def get_context_data(self, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        page_num = self.request.GET.get('page', '')
        if not page_num:
            page_num = 1
        if page_num == 'last':
            page_num = paginator.num_pages
        return {
            'count': paginator.count,
            'total pages': paginator.num_pages,
            'previous_page': page.has_previous() and page.previous_page_number() or None,
            'next_page': page.has_next() and page.next_page_number() or None,
            'results': list(paginator.page(page_num)),
        }

    def render_to_response(self, context, **response_kwargs):
        return MoviesApiMixin.render_to_response(self, context, **response_kwargs)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self, **kwargs):
        return MoviesApiMixin.get_queryset(self, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        movie = [obj for obj in list(self.get_queryset()) if obj.get('id') == pk]
        if movie:
            return movie[0]
        else:
            return HttpResponseNotFound

    def render_to_response(self, context, **response_kwargs):
        return MoviesApiMixin.render_to_response(self, context, **response_kwargs)
