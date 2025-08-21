from django.urls import path
from django.urls import re_path
from django.views.generic.list import ListView

from schedule.feeds import CalendarICalendar, UpcomingEventsFeed
from schedule.models import Calendar
from schedule.periods import Day, Month, Week, Year
from schedule.views import (
    CalendarByPeriodsView,
    CalendarView,
    CancelOccurrenceView,
    CreateEventView,
    CreateOccurrenceView,
    DeleteEventView,
    EditEventView,
    EditOccurrenceView,
    EventView,
    FullCalendarView,
    OccurrencePreview,
    OccurrenceView,
    api_move_or_resize_by_code,
    api_occurrences,
    api_select_create,
)

urlpatterns = [
    path("", ListView.as_view(model=Calendar), name="calendar_list"),
    re_path(
        r"^calendar/year/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_year.html"),
        name="year_calendar",
        kwargs={"period": Year},
    ),
    re_path(
        r"^calendar/tri_month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_tri_month.html"),
        name="tri_month_calendar",
        kwargs={"period": Month},
    ),
    re_path(
        r"^calendar/compact_month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(
            template_name="schedule/calendar_compact_month.html"
        ),
        name="compact_calendar",
        kwargs={"period": Month},
    ),
    re_path(
        r"^calendar/month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_month.html"),
        name="month_calendar",
        kwargs={"period": Month},
    ),
    re_path(
        r"^calendar/week/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_week.html"),
        name="week_calendar",
        kwargs={"period": Week},
    ),
    re_path(
        r"^calendar/daily/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_day.html"),
        name="day_calendar",
        kwargs={"period": Day},
    ),
    re_path(
        r"^calendar/(?P<calendar_slug>[-\w]+)/$",
        CalendarView.as_view(),
        name="calendar_home",
    ),
    re_path(
        r"^fullcalendar/(?P<calendar_slug>[-\w]+)/$",
        FullCalendarView.as_view(),
        name="fullcalendar",
    ),
    # Event Urls
    re_path(
        r"^event/create/(?P<calendar_slug>[-\w]+)/$",
        CreateEventView.as_view(),
        name="calendar_create_event",
    ),
    re_path(
        r"^event/edit/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$",
        EditEventView.as_view(),
        name="edit_event",
    ),
    path("event/<int:event_id>/", EventView.as_view(), name="event"),
    path(
        "event/delete/<int:event_id>/",
        DeleteEventView.as_view(),
        name="delete_event",
    ),
    # urls for already persisted occurrences
    path(
        "occurrence/<int:event_id>/<int:occurrence_id>/",
        OccurrenceView.as_view(),
        name="occurrence",
    ),
    path(
        "occurrence/cancel/<int:event_id>/<int:occurrence_id>/",
        CancelOccurrenceView.as_view(),
        name="cancel_occurrence",
    ),
    path(
        "occurrence/edit/<int:event_id>/<int:occurrence_id>/",
        EditOccurrenceView.as_view(),
        name="edit_occurrence",
    ),
    # urls for unpersisted occurrences
    path(
        "occurrence/<int:event_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/",
        OccurrencePreview.as_view(),
        name="occurrence_by_date",
    ),
    path(
        "occurrence/cancel/<int:event_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/",
        CancelOccurrenceView.as_view(),
        name="cancel_occurrence_by_date",
    ),
    path(
        "occurrence/edit/<int:event_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/",
        CreateOccurrenceView.as_view(),
        name="edit_occurrence_by_date",
    ),
    # feed urls
    path(
        "feed/calendar/upcoming/<int:calendar_id>/",
        UpcomingEventsFeed(),
        name="upcoming_events_feed",
    ),
    re_path(r"^ical/calendar/(.*)/$", CalendarICalendar(), name="calendar_ical"),
    # api urls
    re_path(r"^api/occurrences", api_occurrences, name="api_occurrences"),
    path(
        "api/move_or_resize/", api_move_or_resize_by_code, name="api_move_or_resize"
    ),
    path("api/select_create/", api_select_create, name="api_select_create"),
    path("", ListView.as_view(queryset=Calendar.objects.all()), name="schedule"),
]
