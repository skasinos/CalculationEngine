from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Emission
from .serializers import EmissionFactorSerializer
from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .utils.calculation import load_activity_data, load_emission_factors, calculate_emissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from rest_framework.generics import get_object_or_404


class EmissionListView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'emissions/emission_factor_list.html'

    def get(self, request):
        """
        This method handles GET requests to obtain emissions.
        """
        sort_by_co2e = request.GET.get('sort_by_co2e')
        group_by_activity = request.GET.get('group_by_activity')
        scope_filter = request.GET.get('scope')
        category_filter = request.GET.get('category')

        emissions = Emission.objects.all()

        if scope_filter:
            emissions = emissions.filter(scope=scope_filter)
        if category_filter:
            emissions = emissions.filter(category=category_filter)
        if sort_by_co2e:
            emissions = emissions.order_by('-co2e')

        total_emissions = emissions.aggregate(total_sum=Sum('co2e'))['total_sum']

        if group_by_activity:
            emissions = emissions.values('activity').annotate(co2e_sum=Sum('co2e')).order_by('activity')
            serialized_data = [
                {'activity': item['activity'], 'co2e_sum': item['co2e_sum']}
                for item in emissions
            ]
            context = {'emissions': serialized_data, 'group_by_activity': True, 'total_emissions': total_emissions}
        else:
            serializer = EmissionFactorSerializer(emissions, many=True)
            context = {'emissions': serializer.data, 'total_emissions': total_emissions}

        if request.accepted_renderer.format != 'html':
            return Response(context)

        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request):
        """
        This method handles POST requests to calculate and store emissions in the database. It requires two
        CSV files, namely, 'activity_data' and 'emission_factors'. Emissions are calculated on the basis of
        the provided emission_factors. Once the calculation is completed the emissions are stored in the database.
        """
        # TODO: An improvement, would be to make emission_factors optional and store and fetch from the database.

        activity_data_file = request.FILES.get('activity_data')
        factors_file = request.FILES.get('emission_factors')

        if not activity_data_file or not factors_file:
            return Response({'error': 'activity_data and emission_factors are required.'}, status=HTTP_400_BAD_REQUEST)
        try:
            activity_data = load_activity_data(activity_data_file)
            emission_factors = load_emission_factors(factors_file)
            calculate_emissions(activity_data, emission_factors)
            return Response({'success': 'Emissions calculated and stored successfully.'}, status=HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Delete Emission object using its primary key.
        """
        emission = get_object_or_404(Emission, pk=pk)
        emission.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """
        Update Emission object using its primary key
        """
        emission = get_object_or_404(Emission, pk=pk)
        serializer = EmissionFactorSerializer(emission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)