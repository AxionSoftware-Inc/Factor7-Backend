from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from .mixins import ViewCountMixin

from .models import Category, Tag, Tour, Booking, Inquiry, VisitorLog
from .serializers import (
    CategorySerializer, TagSerializer, TourSerializer, 
    BookingSerializer, InquirySerializer, UserSerializer
)

class DashboardStatsAPI(APIView):
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)
        
        stats = {
            "tours_count": Tour.objects.count(),
            "bookings_count": Booking.objects.count(),
            "inquiries_count": Inquiry.objects.count(),
            "visitors_today": VisitorLog.objects.filter(timestamp__date=today).count(),
            "visitors_week": VisitorLog.objects.filter(timestamp__date__gte=week_ago).count(),
        }
        
        popular_pages = VisitorLog.objects.values('path').annotate(count=Count('id')).order_by('-count')[:5]
        stats['popular_pages'] = list(popular_pages)
        
        visitors_by_day = VisitorLog.objects.filter(timestamp__date__gte=week_ago)\
            .annotate(date=TruncDate('timestamp'))\
            .values('date')\
            .annotate(count=Count('id'))\
            .order_by('date')
            
        chart_data_dict = {str(item['date']): item['count'] for item in visitors_by_day}
        
        labels = []
        data = []
        for i in range(7):
            d = week_ago + timedelta(days=i)
            labels.append(d.strftime("%d %b"))
            data.append(chart_data_dict.get(str(d), 0))
            
        stats['chart_labels'] = labels
        stats['chart_data'] = data
        
        return Response(stats)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TourViewSet(ViewCountMixin, viewsets.ModelViewSet):
    queryset = Tour.objects.select_related("category").prefetch_related("tags").all()
    serializer_class = TourSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        value = self.kwargs[lookup_url_kwarg]

        if value.isdigit():
            obj = queryset.filter(pk=value).first()
            if obj:
                return obj

        return get_object_or_404(queryset, slug=value)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
