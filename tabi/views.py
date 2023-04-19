from django.shortcuts import render
from django.views import generic
from .models import Tabi,Comment,TabiDate,Connection
from accounts.models import CustomUser
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404, redirect,HttpResponse
from .forms import TabiCreateForm,TabiDateFormset,SearchForm,CommentCreateForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.managers import TaggableManager, TaggedItem
from django.contrib.auth.decorators import login_required
from .helpers import get_current_user

# Create your views here.


def sample(request):
    return render(request, 'sample.html')

def tabi_ot(request):
    return render(request, 'ot.html')

class TopListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'top_list.html'

    def get_queryset(self):
        tabi = Tabi.objects.order_by('looked').reverse().filter()[:2]
        return tabi


class MypageList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'my_list.html'
    pagenate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_list'] = Tabi.objects.filter(writer=self.request.user).order_by('created_at')
        return context

class MysaveList(generic.ListView):
    template_name = 'mysave.html'
    model = Tabi,CustomUser
    paginate_by = 10
    def get_queryset(self):
        user=self.request.user
        queryset = user.favorite.all()
        return queryset
    
class UserDetail(generic.DetailView):
    template_name = 'user_detail.html'
    model = Tabi,CustomUser
    paginate_by = 10
    def get_queryset(self):
        queryset = Tabi.objects.filter(field='writer').order_by('created_at')
        return queryset


def FavoritePost(request, pk):
    """記事を保存"""
    favorite_post = get_object_or_404(Tabi, pk=pk)
    request.user.favorite.add(favorite_post)
    return redirect('tabi:top_list')


class CommentCreate(generic.ListView):
    pass

class TabiDelete(generic.DeleteView):
    model = Tabi
    template_name = 'delete.html'
    success_url = reverse_lazy('tabi:top_list')


class TabiDetail(generic.DetailView):
    model = Tabi
    template_name = 'detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_items"] = self.object.tags.similar_objects()[:5]
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.daylooked += 1
        self.object.weeklylooked += 1
        self.object.looked += 1
        self.object.save() 
        context=self.get_context_data(object=self.object)
        return self.render_to_response(context)

class TabiCreateView(generic.CreateView):
    form_class = TabiCreateForm
    template_name = 'create.html'
    success_url = reverse_lazy('tabi:top_list')


    def get_context_data(self, **kwargs):
        ctx = super(TabiCreateView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            ctx["formset"] = TabiDateFormset(self.request.POST, self.request.FILES)
        else:
            ctx["formset"] = TabiDateFormset()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.writer = self.request.user
            self.object.save()

            # FormSet の内容を保存
            formset.instance = self.object
            formset.save()

            return redirect(self.get_success_url())
        else:
            ctx["form"] = form
            return self.render_to_response(ctx)
    


class TabiUpdateView(generic.UpdateView):
    model = Tabi
    form_class = TabiCreateForm
    template_name = 'update.html'

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('tabi:tabi_detail', kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        ctx = super(TabiUpdateView, self).get_context_data(**kwargs)

        ctx.update(dict(formset=TabiDateFormset(self.request.POST or None, instance=self.object)))

        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()

        formset = ctx['formset']

        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            formset.save()

            return redirect(self.get_success_url())
        else:
            ctx['form'] = form
            return self.render_to_response(ctx)


class PopListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'pop_list.html'
    paginate_by = 10

    def get_queryset(self):
        tabi = Tabi.objects.order_by('like').reverse()
        return tabi

class DayListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'day_list.html'
    paginate_by = 10

    def get_queryset(self):
        tabi = Tabi.objects.order_by('daylooked').reverse()
        return tabi

class WeekListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'week_list.html'
    paginate_by = 10

    def get_queryset(self):
        tabi = Tabi.objects.order_by('weeklylooked').reverse()
        return tabi

class NewListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'new_list.html'
    paginate_by = 10

    def get_queryset(self):
        tabi = Tabi.objects.order_by('created_at').reverse()
        return tabi

class FamListView(generic.ListView):
    model = Tabi,TabiDate
    template_name = 'fam_list.html'
    paginate_by = 10

    def get_queryset(self):
        tabi = Tabi.objects.order_by('looked').reverse()
        return tabi


class SearchView(generic.ListView):
    context_object_name = 'post_list'
    paginate_by = 10
    template_name = 'search.html'
    model = Tabi

    def get_queryset(self): # 検索機能のために追加
        queryset = Tabi.objects.order_by('created_at')
        query = self.request.GET.get('query')

        if query:
            queryset = queryset.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
            )
        messages.add_message(self.request, messages.INFO, query)
        return queryset

class LikeBase(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        related_post = Tabi.objects.get(pk=pk)
       
        if self.request.user in related_post.like.all(): 
            obj = related_post.like.remove(self.request.user)
        else:                         
            obj = related_post.like.add(self.request.user)
        return obj


class LikeHome(LikeBase):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('tabi:top_list')

class LikeDetail(LikeBase,generic.View):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('tabi:tabi_detail', pk)






"""フォロー"""
@login_required
def follow_view(request, *args, **kwargs):
    try:

        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = CustomUser.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = CustomUser.objects.get(username=kwargs['username'])
    #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username'])) #（※1）（※2）
        return HttpResponseRedirect(reverse_lazy('pento_app:index'))
        #フォローしようとしている対象が自分の場合、警告文を表示させる。
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        #フォロー対象をまだフォローしていなければ、DBにフォロワー(自分)×フォロー(相手)という組み合わせで登録する。
        #createdにはTrueが入る
        _, created = Connection.objects.get_or_create(follower=follower, following=following) #（※3）

#もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
        if (created):
            messages.success(request, '{}をフォローしました'.format(following.username))
        #既にフォロー相手をフォローしていた場合、createdにはFalseが入る。
        #フォロー済みのメッセージを表示させる。
        else:
            messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('tabi:profile', kwargs={'username': following.username}))

"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):

    try:
        follower = CustomUser.objects.get(username=request.user.username)
        following = CustomUser.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(following.user))
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('tabi:top_list'))
    except Connection.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('tabi:profile', kwargs={'username': following.username}))




class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = Connection
    template_name = 'profile.html'

    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs): # ※(1)
        context = super(ProfileDetail,self).get_context_data(**kwargs)
        username=self.kwargs['username']
        context['username'] = username
        context['user'] = get_current_user(self.request) # ※(2)
        context['tabi'] = Tabi.objects.filter(list=self.writer)
        context['following'] = Connection.objects.filter(follower__username=username).count()
        context['follower'] = Connection.objects.filter(following__username=username).count()

        if username is not context['user'].writer:
            result = Connection.objects.filter(follower__username=context['user'].writer).filter(following__username=username)
            context['connected'] = True if result else False

        return context


class FollowBase(LoginRequiredMixin, generic.View):
       """フォローのベース。リダイレクト先を以降で継承先で設定"""
       def get(self, request, *args, **kwargs):
           #ユーザーの特定
           pk = self.kwargs['pk']
           target_user = Tabi.objects.get(pk=pk).writer
       
           #ユーザー情報よりコネクション情報を取得。存在しなければ作成
           my_connection = Connection.objects.get_or_create(user=self.request.user)
           #フォローテーブル内にすでにユーザーが存在する場合
           if target_user in my_connection[0].following.all():
               #テーブルからユーザーを削除
               obj = my_connection[0].following.remove(target_user)
               #フォローテーブル内にすでにユーザーが存在しない場合
           else:
               #テーブルにユーザーを追加
               obj = my_connection[0].following.add(target_user)
           return obj

class FollowHome(FollowBase):
   """HOMEページでフォローした場合"""
   def get(self, request, *args, **kwargs):
       #FollowBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       #homeにリダイレクト
       return redirect('tabi:top_list')

class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        #FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        #detailにリダイレクト
        return redirect('tabi:tabi_detail', pk)

class FollowList(LoginRequiredMixin, generic.ListView):
      """フォローしたユーザーの投稿をリスト表示"""
      model = Connection
      template_name = 'follow_list.html'
      
      def get_queryset(self):
          """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
          my_connection = Connection.objects.get_or_create(user=self.request.user)
          all_follow = my_connection[0].following.all()
          #投稿ユーザーがフォローしているユーザーに含まれている場合オブジェクトを返す。
          return Tabi.objects.filter(writer__in=all_follow)
      def get_context_data(self, *args, **kwargs):
          """コネクションに関するオブジェクト情報をコンテクストに追加"""
          context = super().get_context_data(*args, **kwargs)
          #コンテクストに追加
          context['connection'] = Connection.objects.get_or_create(user=self.request.user)
          return context
      
      
class CommentCreate(generic.CreateView):
    """
    記事へのコメント作成ビュー
    ページは表示されないが、コメントを作成するために使用
    """
    template_name='comment_form.html'
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Tabi, pk=post_pk)

        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        return redirect('tabi:tabi_detail', pk=post_pk)