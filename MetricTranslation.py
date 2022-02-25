#Translates the dropdown values into values that can be passed into the API
def metrics(metric):
    match metric:
        case "Count Admin Bounce":
            return "count_admin_bounce"
        case "Count Accepted":
            return "count_accepted"
        case "Count Block Bounce":
            return "count_block_bounce"
        case "Count Bounce":
            return "count_bounce"
        case "Count Clicked":
            return "count_clicked"
        case "Count Delayed":
            return "count_delayed"
        case "Count Delayed First":
            return "count_delayed_first"
        case "Count Delivered":
            return "count_delivered"
        case "Count Delivered First":
            return "count_delivered_first"
        case "Count Delivered Subsequent":
            return "count_delivered_subsequent"
        case "Count Generation Failed":
            return "count_generation_failed"
        case "Count Generation Rejection":
            return "count_generation_rejection"
        case "Count Hard Bounce":
            return "count_hard_bounce"
        case "Count Inband Bounce":
            return "count_inband_bounce"
        case "Count Initial Rendered":
            return "count_initial_rendered"
        case "Count Injected":
            return "count_injected"
        case "Count Out of Band Bounce":
            return "count_outofband_bounce"
        case "Count Policy Rejection":
            return "count_policy_rejection"
        case "Count Rejected":
            return "count_rejected"
        case "Count Rendered":
            return "count_rendered"
        case "Count Sent":
            return "count_sent"
        case "Count Soft Bounce":
            return "count_soft_bounce"
        case "Count Spam Complaint":
            return "count_spam_complaint"
        case "Count Targeted":
            return "count_targeted"
        case "Count Undetermined Bounce":
            return "count_undetermined_bounce"
        case "Count Unique Clicked":
            return "count_unique_clicked"
        case "Count Unique Confirmed Opened":
            return "count_unique_confirmed_opened"
        case "Count Unique Initial Rendered":
            return "count_unique_initial_rendered"
        case "Count Unique Rendered":
            return "count_unique_rendered"
        case "Count Unsubscribe":
            return "count_unsubscribe"
        case "Total Delivery Time First":
            return "total_delivery_time_first"
        case "Total Delivery Time Subsequent":
            return "total_delivery_time_subsequent"
        case "Total Message Volume":
            return "total_msg_volume"