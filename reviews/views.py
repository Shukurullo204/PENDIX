from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from .services import ReviewService
from users.models import User

class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        seller = User.objects.get(id=self.kwargs['seller_id'])
        ReviewService.add_review(author=self.request.user, seller=seller, data=form.cleaned_data)
        return redirect('profile_detail', pk=seller.id)
