from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello(request):
    return Response({"message": "API is working"})

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    return Response({"message": "API is working!"})

@api_view(['GET'])
def accessibility_instructions(request):
    instructions = """
    Welcome to the voting system. Use the big buttons to vote.
    Press the speaker button if you want the computer to read for you.
    """
    return Response({"instructions": instructions})
