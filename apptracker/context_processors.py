from .utils import *

def common_data(request):
    return {
        'applicationcount': get_application_count(),
        'appliedtoday': applied_today(),
        'responserate': calc_rate("Applied"),
        'rejectionrate': calc_rate("Rejected"),
        'interviewrate': calc_rate("Interview"),
        'withdrawnrate': calc_rate("Withdrawn"),
        'offeredrate': calc_rate("Offered"),
        'acceptedrate': calc_rate("Accepted"),
    }