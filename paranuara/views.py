from django.views.generic.base import TemplateView
from rest_framework import viewsets, generics, views
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, People
from .serializer import PeopleSerializer, CommonFriendSerializer


# Create your views here.
class PeopleListView(generics.ListAPIView):
    serializer_class = PeopleSerializer

    def get_queryset(self, *args, **kwargs):
        if not 'company_index' in self.kwargs:
            raise APIException("Company Index required!")
        company_index = self.kwargs['company_index']
        if not Company.objects.filter(index=company_index).exists():
            raise NotFound('Company with given index not found')
        return People.objects.filter(company=company_index)


class PeopleRetrieveView(generics.RetrieveAPIView):
    serializer_class = PeopleSerializer
    lookup_field = 'index'
    queryset = People.objects.all()


class CommonFriendView(views.APIView):
    serializer_class = CommonFriendSerializer

    def get(self, request, *args, **kwargs):
        if 'p1_index' not in self.kwargs or 'p2_index' not in self.kwargs:
            raise APIException("Index for people 1 and people 2 required!")
        p1_index = self.kwargs['p1_index']
        p2_index = self.kwargs['p2_index']
        if p1_index == p2_index:
            raise APIException(
                "Index for people 1 and people 2 should be different!")
        # if request.GET:
        people_one = People.objects.values('name', 'age', 'address',
                                           'phone').get(
            index=p1_index)
        people_two = People.objects.values('name', 'age', 'address',
                                           'phone').get(
            index=p2_index)
        common_friends = (
                People.objects.filter(index=p1_index, has_died=False,
                                      eyeColor__iexact='brown').values_list(
                    'friend__name', flat=True).intersection(People.objects.filter(index=p2_index, has_died=False,
                                      eyeColor__iexact='brown').values_list(
                    'friend__name', flat=True))
        )

        return Response({'people_one': people_one, 'people_two': people_two,
                         'common_friends': common_friends})
