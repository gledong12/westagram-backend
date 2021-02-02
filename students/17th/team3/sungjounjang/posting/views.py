import json

from django.views import View
from django.http  import JsonResponse

from .models     import Posting
from user.models import Accounts

class PostingView(View):
    def get(self, request):
        postings = Posting.objects.all()

        response_posting = [
            {
                # 'account'  : postings[i].account,
                'account'  : postings[i].account.nickname,
                # 'account'  : 'ㅋㅋㅋ',
                'image_url': postings[i].image_url,
                'contents' : postings[i].contents,
                'create_at': postings[i].create_at,
                'update_at': postings[i].update_at
            }
        for i in range(len(postings))]

        return JsonResponse({'message':'SUCCESS', 'result':response_posting}, status=200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            account = Accounts.objects.get(nickname=data['account'])

            Posting.objects.create(
                account   = account,
                image_url = data['image_url'],
                contents  = data['contents']
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)