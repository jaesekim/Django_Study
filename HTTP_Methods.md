# 23.03.20.
# `render` vs `redirect`

- `render` : `render(request, template_name, context=**None**, content_type=**None**, status=**None**, using=**None**)`
    
    이 중에서 `request`  와 `template_name` 은 필수적으로 필요합니다. request 는 위와 동일하게 써주게 되고, template_name 은 불러오고 싶은 템플릿을 기재해줍니다. 쉽게 생각해서 화면에 html 파일을 띄운다고 생각하면 됩니다. 이 때 `context`로 원하는 인자를, 즉 view 에서 사용하던 파이썬 변수를html 템플릿으로 넘길 수 있습니다. context 는 딕셔너리형으로 사용하며 key 값이 탬플릿에서 사용할 변수이름, value 값이 파이썬 변수가 됩니다.
    
- `redirect` : `redirect(to, permanent=False, **args, ***kwargs)`
    
    to에는 어느 URL로 이동할지 정하게 된다. 이 떄 상대 URL, 절대 URL 모두 가능하며 urls.py에 name을 정의하고 이를 많이 사용한다. 단지 URL로 이동하는 것이기 때문에  render처럼 context 값을 넘기지는 못한다.
    

출처: [https://ssungkang.tistory.com/entry/Django-render-와-redirect-의-차이](https://ssungkang.tistory.com/entry/Django-render-%EC%99%80-redirect-%EC%9D%98-%EC%B0%A8%EC%9D%B4)

```python
# models.py
from django.db import models

# Create your models here.
class Article(models.Model):  
    # django에 기본적으로 내장된 다른 클래스를 상속받는다고 생각하면된다.
    # models.Model은 그래서 함부로 바꾸면 안된다.
    title = models.CharField(max_length=30)
    content = models.TextField()

    # 날짜와 시간까지 모두 필요할 때 DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now_add: 생성되는 순간 값을 한 번 넣어주는 옵션
    # auto_now: 변경될 때마다 시간과 날짜를 자동으로 변경

    def __str__(self) -> str:
        return f'{self.id} 번째 글 - {self.title}'
```

1. `python [manage.py](http://manage.py/) shell` : django 환경에서 여러가지를 테스트해 보고 싶을 때 입장
    1. `Article.objects.all()` : 모든 article 데이터 가져오기
        
        바로 가져오게 되면 아직 import를 하지 않은 상태이므로 에러가 뜬다.
        
        1.  `from articles.models import Article` : Article 가져오기. shell plus를 사용하면 이러한 작업을 스킵할 수 있다.
        2.  `Article.objects.all()` : 모든 article 데이터 가져오기
        3. QuerySet 형태로 데이터 가져오는 것을 확인
    2. `article = Article.objects.get(id=2)` : article에 있는 특정 게시글 가져오기(두번째)
    3. `Article.objects.create(title='게시글4', content='내용4')` : 새로운 게시글 생성하기. model에서 우리가 채워줄 것은 title, content이고 생성일, 수정일은 자동으로 생성되기 때문에 인자 두 개만 넣어주면 된다.
    4. 게시글 수정하는 방법
        
        → `article = Article.objects.get(id=4)` : 바꾸고 싶은 게시글 따로 변수에 저장
        
        → `article.title = '수정되나’` / `article.content= '게시 내용 수정` : 선언한 변수에 바꾸고 싶은 개별 인자를 `.` 를 사용해서 지정하고 값을 변경해 주면 된다.
        
    
    # READ1 전체 게시글 조회
    
    ```python
    # views.py
    from django.shortcuts import render
    from .models import Article
    
    def index(request):
        articles = Article.objects.all()  # articles 모두 가져오기
        context = {'articles': articles}
        return render(request, 'articles/index.html', context)
    ```
    
    ```html
    {% comment %} index.html {% endcomment %}index.html
    
    {% extends 'base.html' %}
    {% block content %}
      <h1>INDEX</h1>
      <hr>
      {% for article in articles %}
      <p>글 번호: {{ article.id }}</p>
      <p>글 제목: {{ article.title }}</p>
      <p>글 내용: {{ article.content }}</p>
      <hr>
      {% endfor %}
    {% endblock content %}
    ```
    
    # READ2 (Detail Page 조회)
    
    - 개별 게시글 상세 페이지 제작
    - 모든 게시글마다 뷰 함수와 템플릿 파일을 만들 수는 없다. 따라서 글의 번호(pk)를 활용해서 하나의 뷰 함수와 템플릿 파일로 대응한다.
    - Variable Routing 활용
    - 생성/수정시간 시간 바꾸기: [`settings.py`](http://settings.py) → `TIME_ZONE` → `‘Asia/Seoul’`
    
    ```python
    # urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'articles'  # url 매핑 할 때 중복을 피하기 위해 상위 url을 설정해준다.
    urlpatterns = [
        path('', views.index, name='index'),
        path('<int:pk>/', views.detail, name='detail'),
    ]
    ```
    
    **제목을 누르면 상세 페이지로 이동하게 만들기**
    
    ```html
    {% extends 'base.html' %}
    {% block content %}
      <h1>INDEX</h1>
      <hr>
      {% for article in articles %}
      <p>글 번호: {{ article.id }}</p>
      <p><a href="{% url 'articles:detail' article.pk %}">글 제목: {{ article.title }}</a></p>
      <p>글 내용: {{ article.content }}</p>
      <hr>
      {% endfor %}
    {% endblock content %}
    {% comment %} index.html {% endcomment %}
    ```
    
    `"{% url 'articles:detail' %}"` 이렇게 진행하면 views.py에 있는 detail 함수에 필요한 파라미터 값 하나가 들어가지 않기 때문에 오류가 난다.
    
    `"{% url 'articles:detail' article.pk %}"` 이렇게 `pk` 인자를 넣어줘야 한다.
    
    `url` 태그 문법은 `{% url '넣어줄 url' 넣어줄 인자 %}` 로 구성된다.
    
    # Create
    
    ```html
    {% extends 'base.html' %}
    {% block content %}
      <h1>글작성</h1>
      <hr>
      
      <form action="" method="GET">
        <label for="title">제목 : </label>
        <input type="text" id="title" name="title"> <br>
    
        <label for="content">내용 : </label>
        <input type="text" id="content" name="content"> <br>
    
        <input type="submit">
    	</form>
    
        
      
      
    {% endblock content %}
    {% comment %} new.html {% endcomment %}
    ```
    
    - `<form action="" method="GET">`
        
        action 안에 쓰는 값이 form을 작성하면 넘어가지는 값이 된다.
        
    - `redirect()`
        
        인자가 작성된 곳으로 다시 요청을 보냄. 다시 어떤 url로 보내줄 건데??
        
        사용 가능한 인자
        
        1. view name (URL pattern name): ex) `return redirect('articles:index')`
        2. absolute or relative URL
        
        ```python
        def create(request):
            # 사용자가 정의한 데이터는 모두 request에 들어가 있다.
            title = request.GET.get('title')
            content = request.GET.get('content')
            # GET 방식으로 들어온 요청에서 get()을 가져온다
            # new.html의 form안의 name을 받아오는 것.
        
            # DB에 새로운 Article 저장
        		# 방법 1
            Article.objects.create(
                title=title,
                content=content
            )
        	
        		# 방법2
            '''
            ariticle = Article()
            article.title = title
            article.content = content
            article.save()
            '''
        
            # 방법3
            '''
            article = Article(title=title, content=content)
            article.save()
            '''	
            return redirect('articles:index')
        ```
        
    - 방법2 또는 3을 사용하는 이유
        - create 메서드가 더 간단해 보이지만 추후 데이터가 저장되기 전에 유효성 검사를 거치게 될 예정
        - 유효성 검사가 진행도니 후에 save 메서드가 호출되는 구조를 택하기 위함
    
    # HTTP Method
    
    - `**GET**`은 데이터를 조회할 때 사용해야 한다.
    - 데이터를 조작하려 할 때는 `**POST**`를 사용해야 한다.
    
    ## CSRF 토큰
    
    - Cross-Site-Request-Forgery
    - 사이트 간 요청 위조
    - 사용자가 자신의 의지와 무관하게 공격자가 의도한 행동을 하여 특정 웹 페이지를 보안에 취약하게 하거나 수정, 삭제 등의 작업을 하게 만드는 공격 방법
    - 이를 방지하고자 csrf 토큰을 발급해서 암호를 줘야한다.
        
        ```
        <form action="{% url 'articles:create' %}" method="POST">
            {% csrf_token %}
        
        form 태그의 method 부분을 POST로 변경해 주고 
        form 태그 내부에 csrf_token을 적어주기만 하면 된다
        ```
        
    
    ---