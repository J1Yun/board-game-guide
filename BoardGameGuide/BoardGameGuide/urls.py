"""BoardGameGuide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
import boardgame.views

urlpatterns = [
    path('create/', boardgame.views.create, name = "create"),
    path('comu_list/<int:community_id>', boardgame.views.comu_detail, name = 'comu_detail'),
    path('comu_write/', boardgame.views.comu_write, name = 'comu_write'),
    path('comu_list/', boardgame.views.comu_list, name = 'comu_list'),
    path('logout/', boardgame.views.logout, name = 'logout'),
    path('signup_done/', boardgame.views.signup_done, name = 'signup_done'),
    path('rank/', boardgame.views.rank, name = "rank"),
    path('admin/', admin.site.urls),
    path('', boardgame.views.main, name='main'),
    path('search', boardgame.views.search, name='search'),
    path('login/',boardgame.views.login, name='login'),
    path('signup/',boardgame.views.signup, name='signup'),
    path('mypage/',boardgame.views.mypage, name='mypage'),
    path('game/', boardgame.views.game, name = 'game'),
    
]
