from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Exhibitor
from .serializers import ExhibitorSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def company_list(request):
    """
    GET /api/exhibitors/companies/

    Returns a list of all exhibitor companies.

    Query params:
      ?country=UAE        → filter by country
      ?sector=Technology  → filter by sector
      ?hall=H1            → filter by hall
      ?search=apple       → search by name (case-insensitive)
    """
    queryset = Exhibitor.objects.all().order_by('name')

    # Optional filters
    country = request.query_params.get('country')
    sector  = request.query_params.get('sector')
    hall    = request.query_params.get('hall')
    search  = request.query_params.get('search')

    if country:
        queryset = queryset.filter(country__iexact=country)
    if sector:
        queryset = queryset.filter(sector__icontains=sector)
    if hall:
        queryset = queryset.filter(hall__iexact=hall)
    if search:
        queryset = queryset.filter(name__icontains=search)

    serializer = ExhibitorSerializer(queryset, many=True)

    return Response({
        'count':   queryset.count(),
        'results': serializer.data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def company_detail(request, pk):
    """
    GET /api/exhibitors/companies/<id>/

    Returns a single exhibitor company by ID.
    """
    try:
        exhibitor = Exhibitor.objects.get(pk=pk)
    except Exhibitor.DoesNotExist:
        return Response(
            {'error': f'Company with id={pk} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ExhibitorSerializer(exhibitor)
    return Response(serializer.data, status=status.HTTP_200_OK)