import json
from ast              import literal_eval

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .exception_check import exception_check
from .models          import Post, PostImage, Comment, PostLike
from user.models      import User

class PostCreateView(View):
    def post(self, request):

        try :
            data = json.loads(request.body)
            user = User.objects.get(nickname = data['writer'])
            
            post = Post.objects.create(
                title   = data['title'],
                content = data['content'],
                writer  = user
            )
            
            try:
                image_urls = literal_eval(data['image_url'])       #String 형태의 image_url을 list로 변환

                for image_url in image_urls :
                    PostImage.objects.create(image_url = image_url, post = post)
            except:
                    pass

            return JsonResponse({'MESSAGE :':"SUCCESS"},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)

class PostReadView(View):
    def get(self, request):

        try:
            posts    = Post.objects.all()
            req_list = []

            for post in posts:
                images = post.postimage_set.all()
                likes  = post.postlike_set.all().count()

                if images.exists():
                    image_list = [ image.image_url for image in images ]  
                else:
                    image_list = []
                
                req_dict   = {
                    'id'        : post.id,
                    'title'     : post.title,
                    'content'   : post.content,
                    'writer'    : post.writer.nickname,
                    'image_url' : image_list,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at,
                    'likes'     : likes,
                }
                req_list.append(req_dict)

            return JsonResponse({'posts':req_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

class CommentCreateView(View):
    def post(self,request):

        try:
            data = json.loads(request.body)
            user = User.objects.get(nickname=data['writer'])
            post = Post.objects.get(id=data['post'])

            try:
                image_url = data['image_url']
            except:
                image_url = None

            try:
                recomment = Comment.objects.get(id = data['recomment'])
                if recomment.recomment != None :
                    return JsonResponse({'MESSAGE :':"CANNOT_REPLY_TO_REPLY"}, status = 400)

            except:
                recomment = None

            comment = Comment.objects.create(
                writer    = user,
                post      = post,
                image_url = image_url,
                recomment = recomment,
                content   = data['content']
            )
            
            return JsonResponse({'MESSAGE :':"SUCCESS"},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)
        
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_POST"},status = 400)

class CommentReadAllView(View):
    def get(self, request):

        try:
            comments = Comment.objects.all()
            req_list = []

            for comment in comments:
                try:
                    recomment = comment.recomment.id
                except:
                    recomment = None

                req_dict   = {
                    'id'           : comment.id,
                    'content'      : comment.content,
                    'writer'       : comment.writer.nickname,
                    'image_url'    : comment.image_url,
                    'recomment_id' : recomment,
                    'created_at'   : comment.created_at,
                    'updated_at'   : comment.updated_at,
                }
                req_list.append(req_dict)
            return JsonResponse({'COMMENTS :':req_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)



#[추가 구현 사항]: 5번 게시물의 댓글만 표출
class CommentReadView(View):
    def get(self, request, post_id):

        try:
            post     = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=post) 
            req_list = []

            for comment in comments:
                try:
                    recomment = comment.recomment.id
                except:
                    recomment = None

                req_dict   = {
                    'id'           : comment.id,
                    'content'      : comment.content,
                    'writer'       : comment.writer.nickname,
                    'image_url'    : comment.image_url,
                    'recomment_id' : recomment,
                    'created_at'   : comment.created_at,
                    'updated_at'   : comment.updated_at,
                }
                req_list.append(req_dict)
            return JsonResponse({'COMMENTS :':req_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

class LikeView(View):
    def post(self, request):

        try:
            data  = json.loads(request.body)
            post  = Post.objects.get(id=data['post'])
            user  = User.objects.get(id=data['user'])
            likes = PostLike.objects.filter(
                    Q(post=post) & Q(user=user) 
            )
            if likes.exists():
                likes.delete()

                return JsonResponse({'MESSAGE :':f"DISLIKED_POST_{post.title}"},status = 200)
            PostLike.objects.create(post=post, user=user)

            return JsonResponse({'MESSAGE :':f"LIKED_POST_{post.title}"},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)    
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)
        
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_POST"},status = 400)
            

class PostDeleteView(View):
    def post(self, request):

        try:
            data           = json.loads(request.body)
            post           = Post.objects.get(id=data['post'])
            delete_message = f"POST_'{post.title}'_DELETED!"
            
            post.delete()

            return JsonResponse({'MESSAGE :':delete_message}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)
        
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_POST"},status = 400)

class CommentDeleteView(View):
    def post(self, request):

        try:
            data           = json.loads(request.body)
            comment        = Comment.objects.get(id=data['comment'])
            delete_message = f"Comment_'{comment.id}'_DELETED!"

            comment.delete()

            return JsonResponse({'MESSAGE :':delete_message}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)
        
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_POST"},status = 400)

class PostUpdateView(View):
    def post(self, request):

        try:
            data         = json.loads(request.body)
            post         = Post.objects.get(id=data['post'])
            post.content = data['content']

            post.save()

            return JsonResponse({'MESSAGE :':"SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_POST"},status = 400)

class CommentUpdateView(View):
    def post(self, request):

        try:
            data            = json.loads(request.body)
            comment         = Comment.objects.get(id=data['comment'])
            comment.content = data['content']

            comment.save()

            return JsonResponse({'MESSAGE :':"SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)
        
        except Comment.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_COMMENT"},status = 400)
