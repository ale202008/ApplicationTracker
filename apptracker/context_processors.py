from .utils import *

def common_data(request):
    return {
        'applicationcount': get_all_application_count(),
        'appliedtoday': applied_today(),
        'responserate': calc_rate("Applied", None),
        'rejectionrate': calc_rate("Rejected", None),
        'interviewrate': calc_rate("Interview", None),
        'withdrawnrate': calc_rate("Withdrawn", None),
        'offeredrate': calc_rate("Offered", None),
        'acceptedrate': calc_rate("Accepted", None),
        'responsetime': calc_avg_response_time(),
        'avgpay': get_average_salary(None),
    }