import copy

from dj_rest_auth import jwt_auth
from django import http
from django import shortcuts
from django.db.models import query
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import request as req
from rest_framework import response as resp
from rest_framework import status

from calendar_j import exceptions as calendar_exceptions
from calendar_j import models as calendar_models
from calendar_j import paginations as calendar_paginations
from calendar_j import permissions as calendar_permissions
from calendar_j import serializers as calendar_serializers
from calendar_j.services.attendance import attendance
from calendar_j.services.protection import protection
from user import models as user_models
from utils import time as time_utils


class ScheduleListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_queryset(self) -> query.QuerySet:
        params = self.request.GET
        if not all(key in params.keys() for key in ("pk", "from", "to")):
            raise calendar_exceptions.GetScheduleListKeyException

        target_user_id = params.get("pk")
        target_user = shortcuts.get_object_or_404(user_models.User, pk=target_user_id)

        start_date = time_utils.normal_date_formatter.parse(params.get("from"))
        end_date = time_utils.normal_date_formatter.parse(params.get("to"))

        queryset: query.QuerySet = super().get_queryset()
        total_queryset = queryset.filter(is_opened=True)

        related_queryset = total_queryset.filter(
            query.Q(created_by__pk=target_user_id) | query.Q(participants__id__contains=target_user_id)
        ).distinct()
        date_filtered_queryset = related_queryset.filter(~(query.Q(start_at__gte=end_date) | query.Q(end_at__lte=start_date)))
        permission_refined_queryset = date_filtered_queryset.filter(
            protection_level__lte=protection.ProtectionLevel.filter_user_schedule(self.request.user, target_user),
        )
        return permission_refined_queryset

    def create(self, request: req.Request, *args, **kwargs) -> resp.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.save()
        serialized_data = self.serializer_class(data, many=True).data

        for row in serialized_data:
            headers = self.get_success_headers(row)
        if len(serialized_data) == 1:
            response_data = serialized_data[0]
        else:
            queryset = self.queryset.filter(pk__in=[row["id"] for row in serialized_data])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            serializer = self.get_serializer(queryset, many=True)
            response_data = serialized_data.data

        return resp.Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_paginated_response(self, data, **kwargs):
        assert self.paginator
        return self.paginator.get_paginated_response(data, **kwargs)


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    permission_classes = [calendar_permissions.IsScheduleCreatorOrReader]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_object(self):
        schedule: calendar_models.Schedule = super().get_object()
        if not schedule.is_opened:
            raise http.Http404("No such schedule")
        return schedule

    def destroy(self, request, *args, **kwargs) -> resp.Response:
        schedule_id = self.kwargs["pk"]
        schedule = shortcuts.get_object_or_404(calendar_models.Schedule, id=schedule_id)
        schedule.is_opened = False
        schedule.save()
        return resp.Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleAttendanceUpdateView(generics.UpdateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Participant.objects.all()
    permission_classes = [calendar_permissions.IsScheduleParticipant]
    serializer_class = calendar_serializers.ParticipantSerializer

    def get_object(self) -> calendar_models.Participant:
        pk = self.kwargs["pk"]
        schedule = calendar_models.Schedule.objects.get(pk=pk)
        if not schedule.is_opened:
            raise http.Http404("No such schedule")
        return shortcuts.get_object_or_404(calendar_models.Participant, participant=self.request.user, schedule=schedule)


class ScheduleGroupUpdateDestroyView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.RecurringScheduleGroup.objects.all()
    permission_classes = [calendar_permissions.IsRecurringScheduleGroupCreator]
    serializer_class = calendar_serializers.RecurringScheduleGroupSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request: req.Request, *args, **kwargs) -> resp.Response:
        partial = kwargs.pop("partial", False)
        params = request.data

        schedules = calendar_models.Schedule.objects.filter(recurring_schedule_group=self.kwargs["pk"])
        updated_params = copy.deepcopy(params)
        for schedule in schedules:
            if "cron_expr" in params.keys():
                raise exceptions.ValidationError("Recurring Rule cannot be updated")

            if ("start_at" in params.keys()) ^ ("end_at" in params.keys()):
                raise exceptions.ValidationError("start_at, end_at must be existed together")

            if all(key in params.keys() for key in ("start_at", "end_at")):
                start_at = time_utils.normal_datetime_formatter.parse(params.get("start_at"))
                end_at = time_utils.normal_datetime_formatter.parse(params.get("end_at"))

                updated_start_at = time_utils.replace_time(schedule.start_at, start_at)
                updated_end_at = time_utils.replace_time(schedule.end_at, end_at)
                updated_params.update(
                    {
                        "start_at": updated_start_at,
                        "end_at": updated_end_at,
                    }
                )

            schedule_serializer = calendar_serializers.ScheduleSerializer(instance=schedule, data=updated_params, partial=partial)
            schedule_serializer.is_valid(raise_exception=True)
            schedule_serializer.save()

            if getattr(schedule, "_prefetched_objects_cache", None):
                schedule._prefetched_objects_cache = {}

        recurring_schedule_group = self.get_object()
        serializer = self.get_serializer(recurring_schedule_group)
        return resp.Response(serializer.data)

    def destroy(self, request, *args, **kwargs) -> resp.Response:
        schedules = calendar_models.Schedule.objects.filter(recurring_schedule_group=self.kwargs["pk"])
        for schedule in schedules:
            schedule.is_opened = False
            schedule.save()

        recurring_schedule_group: calendar_models.RecurringScheduleGroup = self.get_object()
        recurring_schedule_group.is_opened = False
        recurring_schedule_group.save()
        return resp.Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleParticipantNotificationView(generics.ListAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_queryset(self) -> query.QuerySet:
        participant = self.request.user
        queryset: query.QuerySet = super().get_queryset()
        targets = calendar_models.Participant.objects.filter(
            participant=participant,
            status=attendance.AttendanceStatus.UNANSWERED,
        )
        return queryset.filter(pk__in=[target.schedule.pk for target in targets])
