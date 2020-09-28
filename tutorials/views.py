from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view


# 1 :  Function based view
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)

        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


# 1.1 : class based view extending views from django
from django.views import View


class tutorial_list_view(View):
    def get(self, request):
        tutorials = Tutorial.objects.all()
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


# 1.2 : class based views using generics and mixins from rest_framwork
from rest_framework import generics, mixins


class tutorial_list_view_generic_mixins(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 1.3 : class based view extending generics from rest_framwork
# Since we are using the ListCreateAPIView we are allowed to do POST and GET because the method are already implemented
# for us, it is abstracted
# I don't think a generic class implement a DELETE on all objects unless you override one method
# Refer to the documentation http://www.cdrf.co for the methods implemented in this generic class
class tutorial_list_view_generic(generics.ListCreateAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


# 2 : Function based view
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)
    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    # GET / PUT / DELETE tutorial


# 2.1: Generics + mixins
class tutorial_detail_view_generic_mixins(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                          mixins.DestroyModelMixin):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    # default to pk, so if you dont have the lookup field not a problem for pk else
    # if you are using something else use lookup_field
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def delete(self, request, id=None):
        if id:
            return self.destroy(request)



# 2.2 : Generics from django rest framework
# All the above code can be done just using this generic class that implements GET PUT PATCH DELETE for single
# model instance
class tutorial_detail_view_generic(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


# 3 : Function based view
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


# 3.1 : using generics + mixins
class tutorial_list_published_view_generics_mixins(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Tutorial.objects.filter(published=True)
    serializer_class = TutorialSerializer

    def get(self, request):
        return self.list(request)


# 3.2 : using generics
class tutorial_list_published_view_generics(generics.ListCreateAPIView):
    queryset = Tutorial.objects.filter(published=True)
    serializer_class = TutorialSerializer
