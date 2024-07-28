from apptracker.models import *
from django.db.models import Q, Count, Min, Max
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from geopy.geocoders import Nominatim
from django.views.decorators.http import require_GET, require_POST
import json
import calendar
import random
import pycountry
import time


# Functions dedicated to grab applications based on requirements separated by category

# ---- GET ALL FUNCTIONS ---- #


# Function that returns applications of certain status
def get_all_status_applications(status_name):
    status = Status.objects.get(name=status_name)   
    if status and status_name != "Interview":
        return Application.objects.filter(status=status).order_by('-id')
    elif status and status_name == "Interview":
        return Application.objects.filter(interview_counter__gt=0).order_by('-id')
    else:
        return None


# Function that returns all applications
def get_all_applications():
    return Application.objects.all() 


# Function that returns the count of Application objects
def get_all_application_count():
    return Application.objects.count()


# Functions that returns all employers
def get_all_employers():
    return Employer.objects.all()


# Function that returns all locations
def get_all_locations():
    return Location.objects.exclude(city="Remote")


# Function that returns all sources
def get_all_sources():
    return Source.objects.all()


# Function that returns all dates, no duplicates
def get_all_dates(applications):
    if not applications:
        applications = get_all_applications()
    dates = applications.values_list('application_date', flat=True).distinct()
    return dates


# Function that returns all statuses
def get_all_statuses():
    return Status.objects.all()


# ---- GET ALL FUNCTIONS END ---- #
# ---- GET FUNCTIONS ---- #


# Function to get interview applications based on index in status list
def get_status_application_count(status_name, index):
    status = Status.objects.get(name=status_name)
    if status_name != "Interview":
        return Application.objects.filter(interview_counter=index, status=status)
    else:
        return Application.objects.filter(interview_counter__gte=index)


# Function to get all applications that have received a response
def get_response_count(applications):
    if not applications:
        return (Application.objects.count() - len(get_all_status_applications("Applied")))
    else:
        return applications.count() - applications.filter(status=Status.objects.get(name="Applied")).count()


# Function that return all applications that have received no response
def get_no_response_count(applications):
    if not applications:
        return Application.objects.filter(status=Status.objects.get(name="Applied")).count()
    else:
        return applications.filter(status=Status.objects.get(name="Applied")).count()


# Function that return the week periods of the current month.
def get_month_weeks(year, month):
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month+1, 1) - timedelta(days=1)
    week_periods = []
    
    current_day = first_day_of_month
    while current_day <= last_day_of_month:
        week_start = current_day - timedelta(days=current_day.isoweekday() % 7)
        week_end = week_start + timedelta(days=6)
        week_period = f"{week_start.strftime('%m/%d')}-{week_end.strftime('%m/%d')}"
        week_periods.append(week_period)
        current_day = week_end + timedelta(days=1)
    return week_periods


# Function that returns the applications in heatmap data format.
def get_applications_date(week):
    start_date_str, end_date_str = week.split('-')
    start_date = datetime.strptime(start_date_str, '%m/%d').replace(year=2024)
    end_date = datetime.strptime(end_date_str, '%m/%d').replace(year=2024)
    application_data = []


    current_date = start_date
    while current_date <= end_date:
        applications_for_date_count = len(Application.objects.filter(application_date=current_date.strftime('%Y-%m-%d')))
        application_data.append(
            {
                'week': "|" + week + "|",
                'weekday': current_date.strftime('%A'),
                'value': applications_for_date_count
            },
        )
        current_date += timedelta(days=1)
        
        
    return application_data


# Function that returns the current month.
def get_month():
    return date.today().strftime('%B')


# Function that returns the longest streak of uninterrupted days of applying, and uninterrupted days not applying
def get_streaks(applications):
    if not applications:
        applications = get_all_applications()
    dates = get_all_dates(applications)
    current_streak_applying = 1
    longest_streak_applying = 1
    # We count only the days between dates we have applied for for streak_not_applying
    current_streak_not_applying = 0
    longest_streak_not_applying = 1
    
    last_date = dates[0]
    for date in dates[1:]:
        if date != (last_date + timedelta(days=1)):
            longest_streak_applying = max(longest_streak_applying, current_streak_applying)
            current_streak_applying = 1
            current_streak_not_applying += 1
        else:
            longest_streak_not_applying = max(longest_streak_not_applying, current_streak_not_applying-1)
            current_streak_applying += 1
            current_streak_not_applying = 0
        last_date = date
            
    longest_streak_applying = max(longest_streak_applying, current_streak_applying)
    longest_streak_not_applying = max(longest_streak_not_applying, current_streak_not_applying)
    
    return longest_streak_applying, longest_streak_not_applying


# Function that return the number of most applications in 1 day, and the date.
def get_most_applications_in_day():
    result = Application.objects.values('application_date').annotate(count=Count('id')).order_by('-count').first()
    return result['count'], result['application_date'] if result else (0, None)


# Function that return the number of most applications in a month, and the month.
def get_most_applications_in_month():
    result = Application.objects.values('application_date__month').annotate(count=Count('id')).order_by('-count').first()
    return result['count'], calendar.month_name[result['application_date__month']] if result else (0, None)


# Function that returns the employer with the most applications, and the number of applications
def get_most_applications_employers():
    result = Application.objects.values('employer__name').annotate(count=Count('id')).order_by('-count')
    max_count = result[0]['count'] if result else 0
    employers = [r['employer__name'] for r in result if r['count'] == max_count]
    return employers, max_count


# Function that returns the source with the most applications done.
def get_most_source():
    sources = get_all_sources()
    source_count = 0
    source_arr = []
    
    for source in sources:
        if Application.objects.filter(source=source).count() > source_count:
            source_count = Application.objects.filter(source=source).count()
            source_arr[:] = []
            source_arr.append(source.name)
        elif Application.objects.filter(source=source).count() == source_count:
            source_arr.append(source.name)
            
    return source_count, source_arr


# Function that return the location that has been applied to the most
def get_most_applied_location():
    result = Application.objects.values('location__state').annotate(count=Count('id')).order_by('-count')
    result = result[1]
    return result['count'], result['location__state'] if result else (0, None)


# Function that returns the applications by locations
def get_applications_by_location(location):
    return Application.objects.filter(location=location)


# Function that gets all Employers with a link and appends them to an array
def get_logo_links(request):
    applications = Employer.objects.exclude(Q(website_url__isnull=True))
    links = []
    for application in applications:
        url = application.website_url.replace('https://', '').replace("www.", "")
        if url.endswith('/'):
            url = url[:-1]  # Remove the final slash
        links.append("https://logo.uplead.com/" + url)
    
    random.shuffle(links)
    return JsonResponse({'links': links})


# Function that returns the latitude and longitude of City, State
def get_latitude_and_longitude(location_city, location_state):
    geolocator = Nominatim(user_agent="appl_tracker")
    state_code = pycountry.subdivisions.search_fuzzy(location_state)[0].code if location_state != "D.C." else 'US-DC'
    state_code = state_code[3:]
    geo_location_str = f'{location_city}, {state_code}'
    geo_location = geolocator.geocode(geo_location_str)
    location_latitude = geo_location.latitude
    location_longitude = geo_location.longitude
    return location_latitude, location_longitude


# Function that returns the most applied for role and count
def get_position_and_count(applications):
    if not applications:
        applications = get_all_applications()
    
    position_count = {}

    for application in applications:
        position = application.position
        if position in position_count:
            position_count[position] += 1
        else:
            position_count[position] = 1

    sorted_positions = sorted(position_count.items(), key=lambda item: item[1], reverse=True)
    most_applied_position, highest_count = sorted_positions[0]

    return most_applied_position, highest_count


# Function that returns the average salary of the given query_set of applications or all applications if None
def get_average_salary(applications):
    if not applications:
        applications = get_all_applications()
    
    total_salary = 0
    for application in applications:
        salary = application.pay
        total_salary += salary 

    return round(total_salary/applications.count(), 2)


# Function that returns the hourly based of a regular 40 hour work week, 2080 hours a year
def get_average_hourly(salary):
    return round(salary/2080, 2)


# Function that returns the total days between two dates
def get_total_days():
    first_date = Application.objects.aggregate(first_date=Min('application_date'))['first_date']
    last_date = Application.objects.aggregate(last_date=Max('application_date'))['last_date']
    return (last_date - first_date).days + 1


# Function that returns the latest application object
def get_latest_application():
    return Application.objects.order_by('-application_id').first()


# Function that returns the average amount of application applied a day
def get_avg_applications_per_day():
    avg_applications = (get_all_application_count() / get_total_days())
    return round(avg_applications, 2)


# Function that returns the average amount of days per application
def get_avg_days_per_application():
    avg_days = (get_total_days() / get_all_application_count())
    return int(avg_days)


# ---- GET FUNCTIONS END ---- #
# ---- CHART.HTML DATA FUNCTIONS ---- #


# Function that correctly labels and sends the values for the Sankey chart display
def get_sankeychart_data():
    applied_label = "[bold]Applied[/] " + "(" + str(Application.objects.count()) + ")"
    no_response_label = "[bold]No Response[/] " + "(" + str(get_no_response_count(None)) + ")"
    response_label =  "[bold]Response[/] " + "(" + str(get_response_count(None)) + ")"
    rejected_label = "[bold]Rejected[/] " + "(" + str(len(get_status_application_count("Rejected", 0))) + ")"
    withdrawn_label = "[bold]Withdrawn[/] " + "(" + str(len(get_status_application_count("Withdrawn", 0))) + ")"
    first_interview_label = "[bold]1st Interview[/] " + "(" + str(len(get_status_application_count("Interview", 1))) + ")"
    second_interview_label = "[bold]2nd Interview[/] " + "(" + str(len(get_status_application_count("Interview", 2))) + ")"
    rejected_after_first_label =  "[bold]Rejected After 1st[/] " + "(" + str(len(get_status_application_count("Rejected", 1))) + ")"
    withdrawn_after_first_label = "[bold]Withdrawn After 1st[/] " + "(" + str(len(get_status_application_count("Withdrawn", 1))) + ")"
    rejected_after_second_label = "[bold]Rejected[/] " + "(" + str(len(get_status_application_count("Rejected", 2))) + ")"
    
    data =  [
                {'from': applied_label, "to": no_response_label, "value": len(get_all_status_applications("Applied")), "labelText": "Node 1 (100)"},
                {'from': applied_label, "to": response_label, "value": get_response_count(None)},
                {'from': applied_label, "to": withdrawn_label, "value": len(get_status_application_count("Withdrawn", 0))},
                {'from': response_label, "to": rejected_label, "value": len(get_status_application_count("Rejected", 0))},
                {'from': response_label, "to": first_interview_label, "value": len(get_status_application_count("Interview", 1))},
                {'from': first_interview_label, "to": rejected_after_first_label, "value": len(get_status_application_count("Rejected", 1))},
                {'from': first_interview_label, "to": withdrawn_after_first_label, "value": len(get_status_application_count("Withdrawn", 1))},
                {'from': first_interview_label, "to": second_interview_label, "value": len(get_status_application_count("Interview", 2))},
                {'from': second_interview_label, "to": rejected_after_second_label, "value": len(get_status_application_count("Rejected", 2))}
            ]
    
    return data


# Function that grabs heatmap data
def get_heatmap_data():
    week_period_data = []
    application_date_data = []
    max_value = 0
    for week in get_month_weeks(datetime.now().year, datetime.now().month):
        for data in get_applications_date(week):
            if data['value'] > max_value:
                max_value = data['value']
            application_date_data.append(data)
        
        week_period_data.append({'week': "|" + week + "|"})
    
    data = {
        "week_periods": week_period_data,
        "applications_by_date": application_date_data,
        "max_value": max_value,
        "month": get_month(),
    }
    
    return data


# Function that gets map data, formats it, and returns it in GeoJSON
def get_map_data():
    applications_locations = []
    locations = get_all_locations()

    for location in locations:  
        applications = get_applications_by_location(location)
        subdivisions = pycountry.subdivisions.search_fuzzy(location.state) if location.state != 'D.C.' else pycountry.subdivisions.search_fuzzy('US-DC')
        us_subdivisions = [subdivision for subdivision in subdivisions if subdivision.country_code == 'US']
        state_code = us_subdivisions[0].code
        for i in range(applications.count()):
            location_map_str = {
                "MAIL_ST_PROV_C": state_code[3:],
                "LNGTD_I": location.latitude,
                "LATTD_I": location.longitude,
                "mail_city_n": location.city,
                "count": i,
            }
            applications_locations.append(location_map_str)
            
    data = {
        "query_results": applications_locations,
    }
    
    return data


# Function that gets miscellaneous stats
def get_miscstats():
    longest_streak_applying, longest_streak_not_applying = get_streaks(None)
    most_applications_day, date = get_most_applications_in_day()
    most_applications_month, month = get_most_applications_in_month()
    most_applied_company, num_applications_company = get_most_applications_employers()
    most_source_count, most_source = get_most_source()
    avg_application_per_day = get_avg_applications_per_day()
    avg_days_per_application = get_avg_days_per_application()

    data = {
        "applying_streak": longest_streak_applying,
        "not_applying_streak": longest_streak_not_applying,
        "most_applications_in_day": most_applications_day,
        "most_applications_day": date,
        "most_applications_in_month": most_applications_month,
        "most_applications_month": month,
        "most_applied_company": most_applied_company,
        "num_applications_company": num_applications_company,
        "most_source_count": most_source_count,
        "most_source": most_source,
        "avg_applications_per_day": avg_application_per_day,
        "avg_days_per_application": avg_days_per_application,
    }
    
    return data


# Function that gets source and # of applications from each source, organizes them from in decreasing order and returns the data
def get_source_stats():
    sources = Source.objects.order_by('-num_applications')
    sources_applications = []
    
    for source in sources:
        if source not in sources_applications:
            sources_applications.append({'name': source.name, 'num_applications': source.num_applications})

    data = {
        "source_data": sources_applications
    }

    return data


# Function that gets current month statistics and returns the data
def get_current_month_stats():
    current_month = get_month()
    current_month = datetime.strptime(current_month, "%B").month
    current_month_applications = Application.objects.filter(application_date__month=current_month)
    current_month_applications_count = current_month_applications.count()
    longest_streak_applying, longest_streak_not_applying = get_streaks(current_month_applications) if current_month_applications else 0
    response_count = get_response_count(current_month_applications) if current_month_applications else 0
    no_response_count = get_no_response_count(current_month_applications) if current_month_applications else 0
    response_rate = calc_rate("Applied", current_month_applications) if current_month_applications else 0
    position, position_count = get_position_and_count(current_month_applications) if current_month_applications else None
    position_count_percent = round((position_count/current_month_applications_count) * 100, 2) if current_month_applications_count != 0 else 0
    current_month_avg_salary = get_average_salary(current_month_applications) if current_month_applications else 0
    current_month_avg_hourly = get_average_hourly(current_month_avg_salary) if current_month_avg_salary else 0
    
    data = {
        "application_streak": longest_streak_applying,
        "not_application_streak": longest_streak_not_applying,
        "no_response_count": no_response_count,
        "response_count": response_count,
        "response_rate": response_rate,
        "position": position,
        "position_count": position_count,
        "position_count_percent": position_count_percent,
        "avg_salary": current_month_avg_salary,
        "avg_hourly": current_month_avg_hourly,
        "month": get_month(),
        "num_applications": current_month_applications.count(),
    }
    
    return data


# Function that gets Location object statistics and return the data
def get_locations_stats():
    remote_applications = Application.objects.filter(location=Location.objects.get(city="Remote"))
    non_remote_applications = Application.objects.exclude(location=Location.objects.get(city="Remote"))
    num_remote_applications = remote_applications.count()
    non_remote_applications_count = non_remote_applications.count()
    most_location_count, most_location = get_most_applied_location()
    avg_salary_remote_applications = get_average_salary(remote_applications)
    avg_hourly_remote_applications = get_average_hourly(avg_salary_remote_applications)
    avg_salary_non_remote_applications = get_average_salary(non_remote_applications)
    avg_hourly_non_remote_applications = get_average_hourly(avg_salary_non_remote_applications)
    
    data = {
        "num_remote_applications": num_remote_applications,
        "avg_salary_remote": avg_salary_remote_applications,
        "avg_hourly_remote": avg_hourly_remote_applications,
        "num_non_remote_applications": non_remote_applications_count,
        "avg_salary_non_remote": avg_salary_non_remote_applications,
        "avg_hourly_non_remote": avg_hourly_non_remote_applications,
        "most_applied_location": most_location,
        "most_applied_location_count": most_location_count,
    }
    
    return data


# ---- CHART.HTML DATA FUNCTIONS END ---- #
# ---- BOOLEAN FUNCTION ---- #


# Function that returns a boolean based if an Application object exists with today's date
def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()


# ---- BOOLEAN FUNCTION END ---- #
# ---- REQUEST FUNCTIONS ---- #


@require_POST
# Function that submits a new application submission
def application_submission(request):
    position = request.POST.get('position')
    pay = request.POST.get('pay')
    employer_name = request.POST.get('employer') or request.POST.get('other_employer')
    employer, _ = Employer.objects.get_or_create(name=employer_name) if employer_name else (None, None)
    location_name = request.POST.get('location') or request.POST.get('other_location')
    if location_name == "Remote":
        location = Location.objects.get(city=location_name)
    else:
        location_city, location_state = location_name.split(", ")
        latitude, longitude = get_latitude_and_longitude(location_city, location_state)
        location, _ = Location.objects.get_or_create(city=location_city, state=location_state, latitude=latitude, longitude=longitude) if location_name else (None, None)
    employment_type = request.POST.get('employment_type')
    source_name = request.POST.get('source') or request.POST.get('other_source')
    if Source.objects.filter(name=source_name).exists():
        source = Source.objects.get(name=source_name)
        source.num_applications += 1
        source.save()
    else:
        source, _ = Source.objects.get_or_create(name=source_name, num_applications=1) if source_name else (None, None)
    description = request.POST.get('description')
    notes = request.POST.get('notes')
    save_url(request.POST.get('websiteurl'), employer)
    application_date = request.POST.get('application_date')
    applied_status = Status.objects.get(status_id=1, name='Applied')
    
    application = Application.objects.create(
        status=applied_status,
        application_id = Application.objects.count() + 1,
        position=position,
        pay=pay,
        employer=employer,
        location=location,
        employment_type=employment_type,
        source=source,
        desc=description,
        notes=notes,
        application_date = application_date,
    )
    application.save()
    
    return JsonResponse({'success': True})


@require_POST
# Function that updates a status based on a drag-drop ui
def update_status(request):
    application = Application.objects.get(application_id=request.POST.get("applicationId")) if request.POST.get("applicationId") else None
    status = Status.objects.get(name=request.POST.get("status")) if request.POST.get("status") else None
    if not application or not status:
        JsonResponse({ "error": "No valid status or application." }, status=500)
    else:
        if application.status.name != "Interview" and application.status.name != "Applied":
            return JsonResponse({ "error": "Application status cannot be changed to new status." }, status=500)
        if status.name == "Interview":
            application.interview_counter += 1
        
        # Updates the most recent date a response was given
        application.response_time = date.today()
        application.status = status
        application.save()

    return JsonResponse({ "success": True})


@require_GET
# Function that formats the application from request and application_id, if not return latest application
def get_application_json(request):
    application_id = request.GET.get('applicationId')
    if not application_id:
        application = get_latest_application()
    else:
        application = Application.objects.get(application_id=application_id)
    
    if application:
        data = {
            'application_id': application.application_id,
            'status': str(application.status),
            'location': str(application.location) if str(application.location) != "Remote, " else "Remote",
            'employer': str(application.employer),
            'role': application.position,
            'pay': application.pay,
            'hourly_pay': get_average_hourly(application.pay),
            'desc': application.desc,
            'source': str(application.source),
            'notes': application.notes,
            'application_date': application.application_date,
            'employment_type': application.get_employment_type_display(),
            'employer_url_logo': format_url_for_logo(application.employer.website_url),
            'employer_url': application.employer.website_url,
            'response_time': application.response_time if application.response_time else None,
        }
    else:
        data = {'description': 'No applications available'}
    return JsonResponse(data)


@require_POST
# Function that returns the stats shown in the navbar, updates navbar stats when an application update occurs
def get_navbar_stats(request):
    print()
    data = {
        'responserate': calc_rate("Applied", None),
        'rejectionrate': calc_rate("Rejected", None),
        'interviewrate': calc_rate("Interview", None),
        'withdrawnrate': calc_rate("Withdrawn", None),
        'offeredrate': calc_rate("Offered", None),
        'acceptedrate': calc_rate("Accepted", None),
        'responsetime': calc_avg_response_time(),
        'avgpay': calc_avg_salary(),
    }
    return JsonResponse(data)


# ---- REQUEST FUNCTIONS END ---- #
# ---- MISC FUNCTIONS ---- #


# Function that saves an image
def save_url(url, employer):
    if url and not employer.website_url:
        employer.website_url = url
        employer.save()


# Function that calculates the rate for the given status out of all Application objects
def calc_rate(status_name, applications):
    if not applications:
        applications_count = get_all_application_count()
        response_count = get_response_count(None)
    else:
        applications_count = applications.count()
        response_count = get_response_count(applications)
        
    rate = 0
    if status_name == "Applied":
        rate = (response_count/applications_count) * 100
    else:
        rate = (len(get_all_status_applications(status_name))/applications_count) * 100
        # print(get_all_status_applications("Interview"))
    return round(rate, 2)


# Function that calculates the average response time period after sending an application
def calc_avg_response_time():
    applications = Application.objects.exclude(Q(response_time__isnull=True))
    time_period = 0
    for application in applications:
        time = application.response_time - application.application_date
        time_period += time.days
    time_period = time_period / len(applications)
    return int(time_period)


# Function that calculates the average salary/pay if the information is available from applications
def calc_avg_salary():
    applications = Application.objects.filter(pay__gt=0)
    pay = 0
    for application in applications:
        pay += application.pay
    avg_pay = pay / len(applications)
    return round(avg_pay, 2)


# Function that formats the employer's url to correct logo api format
def format_url_for_logo(url):
    if url:
        url_without_https = url.replace('https://', '')
        url_without_https = url_without_https.replace("www.", "")
        if url_without_https.endswith('/'):
            url_without_https = url_without_https[:-1]  # Remove the final slash
        return url_without_https
    else:
        return url


# ---- MISC FUNCTIONS END ---- #

