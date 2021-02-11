import json
import re

from django.shortcuts import get_object_or_404
from django.views     import View
from django.http      import JsonResponse
from django.utils     import timezone

from .models          import Posting, Comment, PostingLike
from user.models      import User

class PostingView(View):
    def post(self, request):
        data         = json.loads(request.body)
        user_id      = data['user_id']
        content      = data['content']
        image        = data['image']
        created_date = timezone.now()
        
        if image:
            Posting.objects.create(
                user_id      = user_id,
                content      = content,
                image        = image,
                created_date = created_date
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        return JsonResponse({'message': 'PLEASE UPLOAD IMAGE'})
        
    def get(self, request):
        all_contents = Posting.objects.values('user__name', 'content', 'image', 'created_date')
        return JsonResponse({'Postings': list(all_contents)}, status=200)

    def delete(self, request, posting_id):
        data    = json.loads(request.body)
        user_id = data['user_id']
        posting = get_object_or_404(Posting, pk=posting_id)

        if posting.user_id == int(user_id):
            posting.delete()
            return JsonResponse({'message': 'DELETED'}, status=200)
        
        return JsonResponse({'message': 'NO PERMISSION'}, status=400)
    
    def put(self, request, posting_id):
        data          = json.loads(request.body)
        user_id       = data['user_id']
        content       = data['content']
        image         = data['image']
        modified_date = timezone.now()
        posting       = Posting.objects.filter(id=posting_id)

        if posting.first().user_id == int(user_id):
            posting.update(
                content       = content,
                image         = image,
                modified_date = modified_date
                )
            return JsonResponse({'message': 'EDITED'}, status=200)

        return JsonResponse({'message': 'NO PERMISSION'}, status=400)

class CommentView(View):
    def post(self, request, posting_id):
        data         = json.loads(request.body)
        posting      = get_object_or_404(Posting, pk = posting_id)
        user_id      = data['user_id']
        content      = data['content']
        thread_to    = data['comment_id']
        created_date = timezone.now()
        
        try:
            User.objects.get(id = user_id)
            if thread_to:
                posting.comment_set.create(
                    user_id      = user_id,
                    thread_to    = thread_to,
                    content      = content,
                    created_date = created_date
                )
            else:
                posting.comment_set.create(
                    user_id      = user_id,
                    content      = content,
                    created_date = created_date
                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)

    def get(self, request, posting_id):
        
        try:
            Posting.objects.get(id=posting_id)
            thread_to=request.GET.get('comment_id')
            Comment.objects.get(id=thread_to)
            if thread_to:
                threads=Comment.objects.filter(posting_id=posting_id, thread_to=int(thread_to)).values(
                    'user__name',
                    'content',
                    'created_date'
                )
                return JsonResponse({'Threads': list(threads)}, status=200)
        except Posting.DoesNotExist:
            return JsonResponse({'message': 'POST DOES NOT EXIST'}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'COMMENT DOES NOT EXIST'}, status=400)
        else:
            all_comments = Comment.objects.filter(posting_id=posting_id).values(
                'user__name', 
                'content', 
                'created_date'
                )
            return JsonResponse({'Comments': list(all_comments)}, status=200)

    def delete(self, request):
        data       = json.loads(request.body)
        user_id    = data['user_id']
        comment_id = data['comment_id']
        comments   = Comment.objects.get(id=comment_id)

        if comments.user_id == int(user_id):
            comments.delete()
            return JsonResponse({'message': 'DELETED'},status=200)
        return JsonResponse({'message': 'NO PERMISSION'}, status=400)

    def put(self, request):
        data          = json.loads(request.body)
        user_id       = data['user_id']
        comment_id    = data['comment_id']
        content       = data['content']
        modified_date = timezone.now()
        comments      = Comment.objects.filter(id=comment_id)
        
        if comments.first().user_id == int(user_id):
            comments.update(
                content       = content,
                modified_date = modified_date
                )
            return JsonResponse({'message': 'EDITED'}, status=200)
        return JsonResponse({'message': 'NO PERMISSION'}, status=400)

class LikeView(View):
    def post(self, request, posting_id):
        try:
            data    = json.loads(request.body)
            posting = get_object_or_404(Posting, pk=posting_id)
            user_id = data['user_id']
            user    = get_object_or_404(User, pk=user_id)

            if PostingLike.objects.filter(posting_id=posting.id, user_id=user.id):
                posting.like.remove(user_id)
                return JsonResponse({'message': 'UNLIKED'}, status=201)
            else:
                posting.like.add(user_id)
                return JsonResponse({'message': 'LIKED'}, status=201)   
                
        except json.JSONDecodeError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
 
