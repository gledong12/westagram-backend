import json

from django.views           import View
from django.http            import JsonResponse
from django.core            import serializers
from django.core.exceptions import ObjectDoesNotExist

from User.models import User
from User.utils  import validate_token
from .models     import Post, Comment

class PostView(View):
    @validate_token
    def post(self, request):
        data = json.loads(request.body)

        if 'img_url' in data and 'content' in data:
            img_url = data['img_url']
            content = data['content']
        else:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        Post(
            user    = request.user,
            img_url = img_url,
            content = content
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class GetView(View):
    @validate_token
    def get(self, request):
        post = Post.objects.all()

        return JsonResponse(serializers.serialize('json', post),safe = False, status = 200)

class CommentPost(View):
    @validate_token
    def post(self, request):
        data = json.loads(request.body)

        if 'post' in data and 'comment' in data:
            post    = data['post']
            comment = data['comment']
        else:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if not Post.objects.filter(id = post):
            return JsonResponse({'message':'Post is not existed'}, status = 400)

        post = Post.objects.get(id = post)

        Comment(
            user    = request.user,
            post    = post,
            comment = comment
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class CommentGet(View):
    @validate_token
    def get(self, request):
        comment = Comment.objects.filter(post = 1)

        return JsonResponse(serializers.serialize('json', comment), safe = False, status = 200)

class LikePost(View):
    @validate_token
    def post(self, request):
        data = json.loads(request.body)

        if 'post' not in data or 'like' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        post = Post.objects.get(id = data['post'])
        like = int(data['like'])

        if like != 0 and like != 1:
            return JsonResponse({'message':'INVALIED_VALUE'}, status = 400)

        if like == 1:
            post.liked_user.add(request.user.id)
            return JsonResponse({'message':'Like Plus'}, status = 200)
        else:
            post.liked_user.remove(request.user.id)
            return JsonResponse({'message':'Like Minus'}, status = 200)

class LikeGet(View):
    @validate_token
    def get(self, request):
        data = json.loads(request.body)

        if 'post' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        post = data['post']

        try:
            like_count = Post.objects.get(id = post).liked_user.count()
            return JsonResponse({'like_count':like_count}, status = 200)

        except ObjectDoesNotExist:
            return JsonResponse({'message':'DoesNotExist'}, status = 400)
