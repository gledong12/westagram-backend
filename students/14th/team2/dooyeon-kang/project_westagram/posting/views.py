import json

from django.http import JsonResponse, QueryDict
from django.views import View
from django.db.models import Q

from posting.models import Posting, Comment
from user.models import User, Like
from user.utils import login_check

class PostingView(View):
    @login_check
    def post(self, request):
        data    = json.loads(request.body)
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        try:
            image_url   = data['image_url']
            description = data['description']
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        if description.isspace():
            return JsonResponse({'message': 'INVALID_TEXT'}, status = 400)

        try:
            Posting(
                image_url   = image_url,
                description = description,
                user        = user,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception:
            return JsonResponse({'message': 'Somthing wrong'}, status = 400)

    def get(self, request):
        posts = Posting.objects.all().order_by('-id').values()

        try:
            result = [
                {'user': {
                    'user_id': post['user_id'],
                    'username': User.objects.get(id=post['user_id']).name
                 },
                 'comments': [{ 'comment_id': comment['id'],
                                'user_id': comment['user_id'],
                                'username': User.objects.get(id=comment['user_id']).name,
                                'posting_id': comment['posting_id'],
                                'text': comment['text'],
                                'created_at': comment['created_at'],
                              } for comment in Comment.objects.filter(posting_id=post['id']).values()\
                                if not comment['reply_on_id']],
                 'img_url': post['image_url'],
                 'description': post['description'],
                 'posting_id': post['id'],
                 'likes': {
                     'count': len(Like.objects.filter(posting_id=post['id'])),
                     'liked_users': [{'user_id': like.user_id,
                                      'username': User.objects.get(id=like.user_id).name,
                                     } for like in Like.objects.filter(posting_id=post['id'])]
                 },
                 'created_at': post['created_at']} for post in posts
            ]

            return JsonResponse({'result': result}, status = 200)

        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

    @login_check
    def delete(self, request):
        user_id = request.user.id

        try:
            posting_id = request.GET.get('post')
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        try:
            posting = Posting.objects.get(id=posting_id, user_id=user_id)
            posting.delete()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception:
            return JsonResponse({'message': 'INVALID USER OR POSTING'}, status = 400)

    @login_check
    def patch(self, request):
        user_id = request.user.id
        data    = json.loads(request.body)

        try:
            posting_id = request.GET.get('post')
        except KeyError:
            return JsonResponse({'message': 'POSTING ID IS REQUIRED'}, status = 400)

        if not data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        try:
            posting = Posting.objects.get(id=posting_id, user_id=user_id)
        except Exception as error_message:
            return JsonResponse({'message': 'INVALID USER OR POSTING'}, status = 400)

        for key, value in data.items():
            if not key == 'image_url' and not key == 'description':
                return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
            elif key == 'image_url':
                posting.image_url = value
            elif key == 'description':
                if value.isspace():
                    return JsonResponse({'message': 'INVALID_TEXT'}, status = 400)
                posting.description = value

        try:
            posting.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

class CommentView(View):
    @login_check
    def post(self, request):
        data    = json.loads(request.body)
        user_id = request.user.id
        posting_id = request.GET.get('post')

        if not posting_id:
            return JsonResponse({'message': 'Check Querystring'}, status = 400)

        try:
            comment_text = data['text']
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        try:
            posting_obj = Posting.objects.get(id=posting_id)
        except Exception:
            return JsonResponse({'message': 'INVALID POSTING'}, status = 400)

        if not comment_text or comment_text.isspace():
            return JsonResponse({'message': 'INVALID_TEXT'}, status = 400)

        try:
            Comment(
                text    = comment_text,
                user    = user_obj,
                posting = posting_obj,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception as error_message:
            return JsonResponse({'meesage': error_message}, status = 401)

    def get(self, request):

        try:
            post_id = request.GET.get('post')
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

        if Comment.objects.filter(posting_id=post_id).values():
            comments = Comment.objects.filter(posting_id=post_id).values()
        else:
            return JsonResponse({'message': 'No comment for this posting'}, status = 400)

        result = [
            {'posting_id': comment['posting_id'],
             'user': {
                'user_id': comment['user_id'],
                'username': User.objects.get(id=comment['user_id']).name
             },
             'replies': [
                 {'reply_id': reply['id'],
                  'text': reply['text'],
                  'created_at': reply['created_at'],
                  'user_id': reply['user_id'],
                  'username': User.objects.get(id=reply['user_id']).name,
                 } for reply in Comment.objects.filter(reply_on_id=comment['id']).values()
             ],
             'comment_id': comment['id'],
             'text': comment['text'],
             'created_at': comment['created_at'] } for comment in comments if not comment['reply_on_id']
        ]

        try:
            return JsonResponse({'result': result}, status = 200)
        except Exception:
            return JsonResponse({'message': 'Something Wrong'}, status = 400)

    @login_check
    def delete(self, request):
        user_id = request.user.id

        try:
            comment_id = request.GET.get('comment')
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        try:
            comment = Comment.objects.get(id=comment_id, user_id=user_id)
            comment.delete()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception:
            return JsonResponse({'message': 'INVALID USER OR COMMENT'}, status = 400)

class LikeView(View):
    @login_check
    def post(self, request):
        user_id = request.user.id
        posting_id = request.GET.get('post')

        if not posting_id:
            return JsonResponse({'message': 'Check Querystring'}, status = 400)

        try:
            user    = User.objects.get(id=user_id)
            posting = Posting.objects.get(id=posting_id)

            if not Like.objects.filter(user_id=user, posting_id=posting):
                Like.objects.create(user=user, posting=posting)
                return JsonResponse({'message': 'User liked SUCCESSFULLY'}, status = 201)

            return JsonResponse({'message': 'The user has already liked the posting'}, status = 400)

        except Exception as error_message:
            return JsonResponse({'message': 'Invalid user or posting'}, status = 400)

class ReplyView(View):
    @login_check
    def post(self, request):
        user_id = request.user.id
        data    = json.loads(request.body)

        try:
            comment_id = request.GET.get('comment')
            user       = User.objects.get(id=user_id)
            comment    = Comment.objects.get(id=comment_id)
            text       = data['text']
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except Exception:
            return JsonResponse({'message': 'wrong id'}, status = 400)

        if not text or text.isspace():
            return JsonResponse({'message': 'INVALID_TEXT'}, status = 400)

        Comment(
            text       = text,
            user_id    = user.id,
            posting_id = comment.posting_id,
            reply_on   = comment,
        ).save()

        return JsonResponse({'message': 'SUCCESS'}, status = 200)
