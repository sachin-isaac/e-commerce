from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),

    path("register",views.register,name="register"),
    path("login",views.login_page,name="login"),
    path("logout",views.logout_page,name="logout"),

    path("collections",views.collections,name="collections"),
    path("collections/<str:name>",views.view,name="collections"),
    path("collections/<str:cname>/<str:pname>",views.details,name="details"),

    path("addtocart",views.addto_cart,name="addtocart"),
    path("cart",views.cart_page,name="cart"),
    path("remove_cart/<str:cid>",views.remove_cart,name="remove_cart"),

    path("fav",views.fav,name="fav"),
    path("fav_page",views.fav_page,name="fav_page"),
    path("remove_fav/<str:fid>",views.remove_fav,name="remove_fav"),

    path("checkout",views.checkout,name="checkout"),
    path("remove_checkout/<str:cid>",views.remove_checkout,name="remove_checkout"),
    path("placeorder",views.placeorder,name="placeorder"),

    path("my_orders",views.my_orders,name="my_orders"),
    path("view_order/<str:tid>",views.view_order,name="view_order"),
]
