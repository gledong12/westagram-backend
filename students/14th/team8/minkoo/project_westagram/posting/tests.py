import json

from django.test import TransactionTestCase
from django.urls import reverse
from django.db   import connection
from django.utils import timezone

class TestPost(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        user_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data_2), content_type='application/json')
        
        url        = reverse('login')
        login_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*'
        }
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']

        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        self.headers_2 = {'HTTP_Authorization' : self.access_token_2}

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')
            
    def test_create_post(self):
        data = {
            'content'   : 'ㄴ ㅏ는 ㄱ ㅏ끔 눈물을 흘린ㄷ ㅏㅠ',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_create_post_no_id(self):
        data = {
            'content'  : '도우너 어서 오고',
            'image_url': 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_create_post_no_image(self):
        data = {
            'content' : '어이 둘리'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_post_no_content(self):
        data = {
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_not_image_url(self):
        data = {
            'content'   : '초능력 맛 좀 볼래?',
            'image_url' : 'asdf@naver.com'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_IMAGE_URL_REQUEST'

    def test_get_posts(self):
        create_data = {
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200
        
        create_data_2 = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
         
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['posts'] == [
            {
                'name'       : 'douner',
                'content'    : '어이 둘리',
                'image_url'  : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : 0
            },
            {
                'name'       : 'dooly',
                'content'    : '도우너 어서 오고',
                'image_url'  : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : 0
            }
        ]

    def test_get_no_post(self):
        url      = reverse('post')
        response = self.client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'NO_POST_DATA'

class TestComment(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        user_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data_2), content_type='application/json')
        
        url        = reverse('login')
        login_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*'
        }
        response = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']

        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        self.headers_2 = {'HTTP_Authorization' : self.access_token_2}

        post_data = {
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200
        
        post_data_2 = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(post_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')
 
    def test_create_comment(self):
        url  = reverse('comment') 
        data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

    def test_fail_create_comment_no_id(self):
        url  = reverse('comment')
        data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_create_comment_no_post(self):
        url  = reverse('comment')
        data = {
            'comment' : '깐따삐야'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_comment_no_comment(self):
        url  = reverse('comment')
        data = {
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_post_not_found(self):
        url  = reverse('comment')
        data = {
            'post_id' : 5,
            'comment' : 'ㅎㅎㅎㅎㅎㅎ'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

    def test_fail_create_too_long_text(self):
        url  = reverse('comment')
        data = {
            'comment' : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'TOO_LONG_COMMENT'

    def test_get_comment(self):
        url         = reverse('comment') 
        create_data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

        create_data_2 = {
            'comment' : '어서 오고',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url      = reverse('comment_list', args=[2]) 
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['comments'] == [
            {
                'name'       : 'douner',
                'comment'    : '깐따삐야',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id'  : None
            },{
                'name'       : 'dooly',
                'comment'    : '어서 오고',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id'  : None

            }
        ]

    def test_get_comment_is_None(self):
        url         = reverse('comment') 
        create_data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

        create_data_2 = {
            'comment' : '어서 오고',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url      = reverse('comment_list', args=[1])
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'None_comment_data'

    def test_fail_get_comment_post_not_found(self):
        url      = reverse('comment_list', args=[100])
        response = self.client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'
    
class TestCommentPutDelete(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        user_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data_2), content_type='application/json')
        
        url        = reverse('login')
        login_data = {
            'name' : 'dooly',
            'password' : '123456qwerT*'
        }
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name' : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']

        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        self.headers_2 = {'HTTP_Authorization' : self.access_token_2}

        post_data = {
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }

        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200
        
        post_data_2 = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(post_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url         = reverse('comment') 
        create_data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')

    def test_put_comment(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 1,
            'comment'    : '대충 코멘트'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200 
    
    def test_fail_put_comment_no_id(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 1,
            'comment'    : '대충 코멘트'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'
#
    def test_fail_put_comment_no_comment_id(self):
        url  = reverse('comment')
        data = {
            'comment' : '대충 코멘트'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_put_comment_no_comment(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 1
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_put_comment_not_found(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 2,
            'comment'    : '대충 코멘트'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'COMMENT_NOT_FOUND'

    def test_delete_comment(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 1
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200 

    def test_fail_delete_comment_no_id(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 1
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401 
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_delete_comment_comment_not_found(self):
        url  = reverse('comment')
        data = {
            'comment_id' : 100
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'COMMENT_NOT_FOUND'

class TestLike(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        user_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data_2), content_type='application/json')

        url = reverse('login')
        login_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*'
        }
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']

        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        self.headers_2 = {'HTTP_Authorization' : self.access_token_2}

        post_data = {
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200
        
        post_data_2 = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(post_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')

    def test_add_like(self):
        url  = reverse('like')
        data = {
            'post_id' : 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
    
    def test_fail_add_like_no_id(self):
        url  = reverse('like')
        data = {
            'post_id' : 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')    
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_add_like_post_not_found(self):
        url  = reverse('like')
        data = {
            'post_id' : 5
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

    def test_delete_like_post(self):
        url  = reverse('like')
        data = {
            'post_id' : 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        data = {
            'post_id' : 1
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
    
    def test_get_like_list(self):
        url  = reverse('like')
        data = {
            'post_id' : 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('like')
        data = {
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
        
        url      = reverse('like_list', args=[1])
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['posts'] == [
            {
                'name'       : 'douner',
                'content'    : '어이 둘리',
                'image_url'  : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : 1 
            },
            {
                'name'       : 'dooly',
                'content'    : '도우너 어서 오고',
                'image_url'  : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : 1
            }
        ]
        
        url  = reverse('like')
        data = {
            'post_id' : 1
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url      = reverse('like_list', args=[1])
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['posts'] == [
            {
                'name'       : 'dooly',
                'content'    : '도우너 어서 오고',
                'image_url'  : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : 1 
            }
        ]
            
    def test_get_like_list_No_data(self):
        url      = reverse('like_list', args=[1])
        response = self.client.get(url)
        assert response.status_code == 404 
        assert json.loads(response.content)['message'] == 'NO_LIKE_DATA'

    def test_fail_get_like_list_not_exists(self):
        url      = reverse('like_list', args=[123])
        response = self.client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'USER_NOT_EXIST'

class TestPostDetail(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com' }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        url        = reverse('login')
        login_data = {
            'name' : 'dooly',
            'password' : '123456qwerT*'
        }
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        post_data = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')
    
    def test_get_post_detail(self):
        url  = reverse('comment') 
        data = {
            'comment' : '대충 댓글',
            'post_id' : 1 
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url      = reverse('post_detail', args=[1])
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['post'] == {
            'name'       : 'dooly',
            'content'    : '도우너 어서 오고',
            'image_url'  : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg',
            'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'like'       : 0,
            'comments'   : [{
                'name'       : 'dooly',
                'comment'    : '대충 댓글',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id'  : None
            },{
                'name'       : 'dooly',
                'comment'    : '대충 대댓글',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id'  : 1
            }] 
        }

    def test_fail_get_post_detail_post_not_found(self):
        url      = reverse('post_detail', args=[100])
        response = self.client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

    def test_put_post_detail_content(self):
        url  = reverse('post_detail', args=[1])
        data = {
            'content' : '처신 잘하라고'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_put_post_detail_image_url(self):
        url  = reverse('post_detail', args=[1])
        data = {
            'image_url' : '없지롱'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
    
    def test_put_post_detail_all_data(self):
        url  = reverse('post_detail', args=[1])
        data = {
            'content'   : '처신 잘하라고',
            'image_url' : '없지롱'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200 

    def test_fail_put_post_detail_no_id(self):
        url  = reverse('post_detail', args=[1])
        data = {
            'content'   : '처신 잘하라고',
            'image_url' : '없지롱'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_put_post_detail_not_found(self):
        url  = reverse('post_detail', args = [100])
        data = {
            'content'   : '처신 잘하라고',
            'image_url' : '없지롱'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

    def test_fail_put_post_detail_key_error(self):
        url  = reverse('post_detail', args=[1])
        data = {
            '대충 키' : '대충 값',
            '또 키'   : '또 값'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_delete_post_detail(self):
        url      = reverse('post_detail', args=[1])
        response = self.client.delete(url, content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_delete_post_detail_no_id(self):
        url  = reverse('post_detail', args=[1])
        data = {
            'content'   : '처신 잘하라고',
            'image_url' : '없지롱'
        }
        response = self.client.delete(url, json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_delete_post_detail_post_not_found(self):
        url      = reverse('post_detail', args=[100])
        response = self.client.delete(url, content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

class TestReply(TransactionTestCase):
    def setUp(self):
        user_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        
        user_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(user_data_2), content_type='application/json')

        url = reverse('login')
        login_data = {
            'name' : 'dooly',
            'password' : '123456qwerT*'
        }
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name' : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']
        
        self.headers_1 = {'HTTP_Authorization' : self.access_token_1}
        self.headers_2 = {'HTTP_Authorization' : self.access_token_2}

        post_data = {
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url      = reverse('post')
        response = self.client.post(url, data=json.dumps(post_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200
        
        post_data_2 = {
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(post_data_2), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url         = reverse('comment') 
        create_data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')

    def test_create_reply(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_create_reply_no_id(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply' : '대충 실패할 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_create_reply_wrong_comment(self):
        url  = reverse('reply', args=[100])
        data = {
            'reply'   : '대충 실패할 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'COMMENT_NOT_FOUND'
    
   
    def test_fail_create_reply_too_long(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'   : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'TOO_LONG_REPLY'

    def test_put_reply(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('reply', args=[1])
        data = {
            'reply_id' : 2,
            'reply'    : '대충 고친 대댓글'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_put_reply_no_id(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply' : '대충 고치려다가 실패할 대댓글'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401 
        assert json.loads(response.content)['message'] == 'INVALID_USER'
    
    def test_fail_put_reply_no_reply(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply_id' : 2
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_put_reply_no_reply_id(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'   : '대충 대댓글을 시도하는 대댓글'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_put_reply_wrong_comment(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('reply', args=[100])
        data = {
            'reply_id' : 2,
            'reply'    : '성공? 어림도 없지ㅋㅋ'
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'REPLY_NOT_FOUND'

    def test_delete_reply(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('reply', args=[1])
        data = {
            'reply_id' : 2 
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_delete_reply_no_id(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply_id' : 1 
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_delete_reply_wrong_comment(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply'      : '대충 대댓글'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('reply', args=[100])
        data = {
            'reply_id' : 2
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'REPLY_NOT_FOUND'

    def test_fail_delete_reply_wrong_reply_id(self):
        url  = reverse('reply', args=[1])
        data = {
            'reply_id' : 100
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'REPLY_NOT_FOUND'
