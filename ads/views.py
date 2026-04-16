from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from categories.models import Category
from users.models import User

from .forms import AdForm
from .models import Ad, AdImage
from .services import AdService


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Ad.objects.filter(status='active')
            .select_related('category', 'author')
            .prefetch_related('images')
        )

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(parent__isnull=True)
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_queryset(self):
        return (
            Ad.objects.filter(status='active')
            .select_related('category', 'author')
            .prefetch_related('images')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_ads'] = (
            Ad.objects.filter(category=self.object.category, status='active')
            .exclude(id=self.object.id)
            .prefetch_related('images')[:10]
        )
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_invalid_step(self, form):
        if form.errors.get('gallery'):
            return 1

        if (
            form.errors.get('title')
            or form.errors.get('category')
            or form.errors.get('description')
        ):
            return 2

        if (
            form.errors.get('price')
            or form.errors.get('currency')
            or form.errors.get('phone')
        ):
            return 3

        return 4

    def form_invalid(self, form):
        print('FORM ERRORS:', form.errors)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                initial_step=self.get_invalid_step(form),
            )
        )

    def form_valid(self, form):
        images = self.request.FILES.getlist('gallery')
        data = form.cleaned_data.copy()
        data.pop('gallery', None)

        AdService.create_ad(
            author=self.request.user,
            data=data,
            images=images,
        )
        return redirect('ad_list')


class UserAdListView(ListView):
    model = Ad
    template_name = 'ads/user_ads.html'
    context_object_name = 'ads'
    paginate_by = 12

    def get_queryset(self):
        self.author = get_object_or_404(User, id=self.kwargs['user_id'])
        return (
            Ad.objects.filter(author=self.author, status='active')
            .select_related('category')
            .prefetch_related('images')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_author'] = self.author
        return context


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_invalid_step(self, form):
        # Проверяем только текстовые поля
        if (
                form.errors.get('title')
                or form.errors.get('category')
                or form.errors.get('description')
        ):
            return 2  # Шаг с описанием

        if (
                form.errors.get('price')
                or form.errors.get('currency')
                or form.errors.get('phone')
        ):
            return 3  # Шаг с контактами

        return 4  # Все остальное (включая карту и фото)

    def form_invalid(self, form):
        print('FORM ERRORS:', form.errors)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                initial_step=self.get_invalid_step(form),
            )
        )

    def form_valid(self, form):
        self.object = form.save()

        images = self.request.FILES.getlist('gallery')
        if images:
            for image in images:
                AdImage.objects.create(ad=self.object, image=image)

        return redirect('ad_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})