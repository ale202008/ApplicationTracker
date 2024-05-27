from apptracker.models import *
from django.db.models import Q
from django.http import JsonResponse
from datetime import date, datetime, timedelta
import json
import calendar
import random

# Functions dedicated to grab applications based on requirements separated by category

# ---- GET ALL FUNCTIONS ---- #

# Function to get all applications of certain status
def get_all_status_applications(status_name):
    status = Status.objects.get(name=status_name)
    
    if status:
        return Application.objects.filter(status=status).order_by('-id')
    else:
        return None

# Function that gets all applications
def get_all_applications():
    return Application.objects.all() 

# Functions that gets all employers
def get_all_employers():
    return Employer.objects.all()

# Function that gets all sources
def get_all_sources():
    return Source.objects.all()

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
def get_response_count():
    return (Application.objects.count() - len(get_all_status_applications("Applied"))) - len(get_status_application_count("Withdrawn", 0))

# Function that returns the count of Application objects
def get_application_count():
    return Application.objects.count()

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
                'week': "(" + week + ")",
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
def get_streaks():
    applications = get_all_applications()
    streak_applying = 0
    longest_streak_applying = 0
    streak_not_applying = 0
    longest_streak_not_applying = 0

    last_date = date.today()
    for application in applications:
        if application.application_date != (last_date + timedelta(days=1)):
            last_date = application.application_date
            if streak_applying > longest_streak_applying:
                longest_streak_applying = streak_applying
                streak_applying = 0
                
            streak_not_applying +=1
        else:
            streak_applying += 1
            
            if streak_not_applying > longest_streak_not_applying:
                longest_streak_not_applying = streak_not_applying
                streak_not_applying = 0

    
    return streak_applying, streak_not_applying

# Function that return the number of most applications in 1 day, and the date.
def get_most_applications_in_day():
    applications = get_all_applications()
    most_applications = 0
    date = None
    
    for application in applications:
        if Application.objects.filter(application_date=application.application_date).count() > most_applications:
            most_applications = Application.objects.filter(application_date=application.application_date).count()
            date = application.application_date

    return most_applications, date

# Function that return the number of most applications in a month, and the month.
def get_most_applications_in_month():
    most_applications = 0
    month = None
    
    for i in range(12):
        if Application.objects.filter(application_date__month=i).count() > most_applications:
            most_applications = Application.objects.filter(application_date__month=i).count()
            month = calendar.month_name[i]
            
    return most_applications, month

# Function that returns the employer with the most applications, and the number of applications
def get_most_applications_employers():
    employers = get_all_employers()
    num_applications = 0
    applied_employers = []
    
    for employer in employers:
        if Application.objects.filter(employer=employer).count() > num_applications:
            num_applications = Application.objects.filter(employer=employer).count()
            applied_employers[:] = []
            applied_employers.append(employer.name)
        elif Application.objects.filter(employer=employer).count() >= num_applications:
            applied_employers.append(employer.name)
        
    return applied_employers, num_applications

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

# Function that correctly labels and sends the values for the Sankey chart display
def get_sankeychart_data():
    applied_label = "[bold]Applied[/] " + "(" + str(Application.objects.count()) + ")"
    no_response_label = "[bold]No Response[/] " + "(" + str(get_response_count()) + ")"
    response_label =  "[bold]Response[/] " + "(" + str(get_response_count()) + ")"
    rejected_label = "[bold]Rejected[/] " + "(" + str(len(get_status_application_count("Rejected", 0))) + ")"
    withdrawn_label = "[bold]Withdrawn[/] " + "(" + str(len(get_status_application_count("Withdrawn", 0))) + ")"
    first_interview_label = "[bold]1st Interview[/] " + "(" + str(len(get_status_application_count("Interview", 1))) + ")"
    second_interview_label = "[bold]2nd Interview[/] " + "(" + str(len(get_status_application_count("Interview", 2))) + ")"
    rejected_after_first_label =  "[bold]Rejected After 1st[/] " + "(" + str(len(get_status_application_count("Rejected", 1))) + ")"
    withdrawn_after_first_label = "[bold]Withdrawn After 1st[/] " + "(" + str(len(get_status_application_count("Withdrawn", 1))) + ")"
    
    data =  [
                {'from': applied_label, "to": no_response_label, "value": len(get_all_status_applications("Applied")), "labelText": "Node 1 (100)"},
                {'from': applied_label, "to": response_label, "value": get_response_count()},
                {'from': applied_label, "to": withdrawn_label, "value": len(get_status_application_count("Withdrawn", 0))},
                {'from': response_label, "to": rejected_label, "value": len(get_status_application_count("Rejected", 0))},
                {'from': response_label, "to": first_interview_label, "value": len(get_status_application_count("Interview", 1))},
                {'from': first_interview_label, "to": rejected_after_first_label, "value": len(get_status_application_count("Rejected", 1))},
                {'from': first_interview_label, "to": withdrawn_after_first_label, "value": len(get_status_application_count("Withdrawn", 1))},
                {'from': first_interview_label, "to": second_interview_label, "value": len(get_status_application_count("Interview", 2))},
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
        
        week_period_data.append({'week': "(" + week + ")"})
    
    data = {
        "week_periods": week_period_data,
        "applications_by_date": application_date_data,
        "max_value": max_value,
        "month": get_month(),
    }
    
    return data

# Function that gets miscellaneous stats
def get_miscstats():
    longest_streak_applying, longest_streak_not_applying = get_streaks()
    most_applications_day, date = get_most_applications_in_day()
    most_applications_month, month = get_most_applications_in_month()
    most_applied_company, num_applications_company = get_most_applications_employers()
    most_source_count, most_source = get_most_source()

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
    }
    
    return data

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

# ---- GET FUNCTIONS END ---- #
# ---- BOOLEAN FUNCTION ---- #

# Function that returns a boolean based if an Application object exists with today's date
def applied_today():
    return Application.objects.filter(application_date=date.today()).exists()

# ---- BOOLEAN FUNCTION END ---- #
# ---- MISC FUNCTIONS ---- #

# Function that saves an image
def save_url(url, employer):
    if url and not employer.website_url:
        employer.website_url = url
        employer.save()

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
        location, _ = Location.objects.get_or_create(city=location_city, state=location_state) if location_name else (None, None)
    employment_type = request.POST.get('employment_type')
    source_name = request.POST.get('source') or request.POST.get('other_source')
    source, _ = Source.objects.get_or_create(name=source_name) if source_name else (None, None)
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

# Function that updates a status based on a drag-drop ui
def update_status(request):
    data = json.loads(request.body)
    application = Application.objects.get(id=data.get("applicationId"))
    if application.status.name != "Interview" and application.status.name != "Applied":
        return JsonResponse({ "error": "Application status cannot be changed to new status." }, status=500)
    status = Status.objects.get(name=data.get("columnId"))
    if status.name == "Interview":
        application.interview_counter += 1
    
    # Updates the most recent date a response was given
    application.response_time = date.today()
    application.status = status
    application.save()

    return JsonResponse({ "success": True})

# Function that calculates the rate for the given status out of all Application objects
def calc_rate(status_name):
    total_applications = get_application_count()
    rate = 0
    if status_name == "Applied":
        rate = (get_response_count()/total_applications) * 100
    else:
        rate = (len(get_all_status_applications(status_name))/total_applications) * 100
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

# ---- MISC FUNCTIONS END ---- #
