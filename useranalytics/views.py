from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import *
from .exceptions import CustomException
from .data_handler import  *
# Create your views here.


class ClientView(APIView):
    """
    """

    def post(self, request, *args, **kwargs):
        """
        :return:
        """
        client_name = kwargs['client_name']
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data.get('email')

        try:
            api_key = create_client(client_name, email)
        except CustomException as exc:
            response = {'message': exc.args[0], 'status_code': exc.args[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = {'api_key': api_key}
        return Response(response, status=status.HTTP_201_CREATED)


class ClientDataView(APIView):
    """
    """

    def get(self, request, *args, **kwargs):
        """
        :return:
        """
        client_name = kwargs['client_name']
        api_key = request.query_params.get('api_key')
        page_name = request.query_params.get('page_name')

        try:
            if not api_key:
                response = {'message': 'api_key is required in query string', 'status_code': 4001}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            client = get_client(client_name, api_key)
            client_data = get_client_data(client, page_name)
        except CustomException as exc:
            response = {'message': exc.args[0], 'status_code': exc.args[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(client_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        :return:
        """
        client_name = kwargs['client_name']
        serializer = ClientDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        page_name = serializer.data.get('page_name')
        timestamp = serializer.data.get('timestamp')
        user_info = serializer.data.get('userinfo')
        session_info = serializer.data.get('sessioninfo')
        location = serializer.data.get('location')
        api_key = serializer.data['api_key']

        try:
            client = get_client(client_name, api_key)
            create_client_data(page_name, timestamp, location,
                               user_info, session_info, client)
        except CustomException as exc:
            response = {'message': exc.args[0], 'status_code': exc.args[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({}, status=status.HTTP_201_CREATED)


class ClientOnlineUserView(APIView):
    """
    """

    def get(self, request, *args, **kwargs):
        """
        :return:
        """
        client_name = kwargs['client_name']
        api_key = request.query_params.get('api_key')
        page_name = request.query_params.get('page_name')

        try:
            if not api_key:
                response = {'message': 'api_key is required in query string', 'status_code': 4001}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            client = get_client(client_name, api_key)
            client_data = get_client_current_users(client, page_name)
        except CustomException as exc:
            response = {'message': exc.args[0], 'status_code': exc.args[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(client_data, status=status.HTTP_200_OK)