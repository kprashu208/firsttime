from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import (
								LoginRequiredMixin,
								UserPassesTestMixin
								)
from django.contrib.auth.models import User

from django.views.generic import (
								ListView, 
								DetailView,
								CreateView,
								UpdateView,
								DeleteView)

from .models import Post, PostComments
from django.db import models
 


def home(request):
	context =  {
		'posts' : Post.objects.all()
	}
	return render(request, 'blog/home.html', context)



class PostListView(ListView):
	model = Post	 	
	template_name = 'blog/home.html'
	# <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4

	def get_queryset(self):
		first = Post.objects.filter(privacy="public").order_by('-date_posted')
		if self.request.user.is_authenticated :
			second = Post.objects.filter(privacy="private", author=self.request.user).order_by('-date_posted')
			return first | second
		else :
			return first



class UserPostListView(ListView):
	model = Post	 	
	template_name = 'blog/user_posts.html'
	# <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'


	def get_context_data(self, **kwargs):          
	    context = super().get_context_data(**kwargs) 
	    context['comments'] = PostComments.objects.filter(post=self.kwargs.get('pk')).order_by('-date_posted')
	    return context

	def post(self, request, *args, **kwargs):
		data = request.POST.get('comment')
		post = Post.objects.filter(id=self.kwargs.get('pk')).first()
		new = PostComments(content=data, post=post, authors=request.user)
		new.save(*args, **kwargs)
		return redirect('post-detail', self.kwargs.get('pk'))



# class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView)
		
def del_comment(request, pk):

	template = 'blog/comment_confirm_delete.html'
	comment = get_object_or_404(PostComments, pk=pk)
	post = comment.post
	comment.delete()
	return redirect('post-detail', post.id)






class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'privacy']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post	 	
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False







class CommentCreateView(LoginRequiredMixin, CreateView):
	model = PostComments	 	
	fields = ['content']

	def form_valid(self, form):
		post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
		form.instance.post = post
		return super().form_valid(form)





def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})












# Create your views here.
 