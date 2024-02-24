from django.http import JsonResponse, HttpResponseRedirect

from django.utils.deprecation import MiddlewareMixin

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = ["/ums/loginCon/", "/ums/addStudent/", "/ums/home/", "/ums/login/", "/ums/register/",
                 "/ums/studentAdd/"]


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        print(request.path not in API_WHITELIST)
        if request.path not in API_WHITELIST:
            print(request.path.find("/getVerify"))
            print(request.path.find("/static"))
            if request.path.find("/getVerify") > -1 or request.path.find("/static") > -1 \
                    or request.path.find("/login") > -1:
                pass
            else:
                print("login in")
                # 从请求头中获取 username 和 token
                username = '';
                try:
                    username = request.session['loginAccount']
                except:
                    return HttpResponseRedirect('/ums/home/')

                # token = request.META.get('HTTP_AUTHORIZATION')
                # if username is None or token is None:
                print(request.path)
                if username is None:
                    return JsonResponse({'code': 401, 'message': "未查询到登录信息"})
                else:
                    pass
                # 调用 check_token 函数验证
                # if check_token(username, token):
                #     pass
                # else:
                #     return JsonResponse({'code': 402, 'message': "登录信息错误或已过期"})
        else:
            pass
