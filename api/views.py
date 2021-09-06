from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny


class RootApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({
            'person': {
                'token': reverse('person_api:token_obtain_pair', request=request,
                                 format=format, current_app='person'),
                'token-refresh': reverse('person_api:token_refresh', request=request,
                                         format=format, current_app='person'),
                'users': reverse('person_api:user-list', request=request,
                                 format=format, current_app='person'),
                'verifycodes': reverse('person_api:verifycode-list', request=request,
                                       format=format, current_app='person'),
            },
            'barber': {
                'customer': {
                    'orders': reverse('barber_api:customer:order-list', request=request,
                                      format=format, current_app='barber'),
                },
                'cashier': {
                    'order-ratingss': reverse('barber_api:cashier:order_rating-list', request=request,
                                              format=format, current_app='barber'),
                },
                'general': {
                    'stat': reverse('barber_api:general:stat', request=request,
                                    format=format, current_app='feeder'),
                    'styles': reverse('barber_api:general:style-list', request=request,
                                      format=format, current_app='barber'),
                    'styles-oty': reverse('barber_api:general:style_oty-list', request=request,
                                          format=format, current_app='barber'),
                    'barbermans': reverse('barber_api:general:barberman-list', request=request,
                                          format=format, current_app='barber'),
                    'brochures': reverse('barber_api:general:brochure-list', request=request,
                                         format=format, current_app='barber'),
                    'rules': reverse('barber_api:general:rules-list', request=request,
                                     format=format, current_app='barber'),
                    'branchs': reverse('barber_api:general:branch-list', request=request,
                                       format=format, current_app='barber'),
                    'groups': reverse('barber_api:general:group-list', request=request,
                                      format=format, current_app='barber'),
                    'informations': reverse('barber_api:general:information-list', request=request,
                                            format=format, current_app='barber'),
                }
            }
        })


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def ping(request):
    csrftoken = request.COOKIES.get('csrftoken')
    if not csrftoken:
        raise NotFound(detail=_("CSRF Token not set"))
    return Response({'csrftoken': csrftoken})
