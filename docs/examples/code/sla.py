import json

def SLA(trust, delta):
    decision = ""
    updated_trust = 0.0

    if trust >= 0.9:
        # Very Trusty
        if delta <= 20: # and time_freq <= 20:
            decision = "Accepted"
            # Max trust value is 1.0
            if trust < 1.0:
                updated_trust = trust + 0.1
                if updated_trust > 1:
                    updated_trust = 1.0
            else:
                updated_trust = trust 
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.6 and trust < 0.9:
        # Medium Trusty
        if delta <= 15: # and time_freq <= 18:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.5 and trust < 0.6:
        # Low Trusty
        if delta <= 10: # and time_freq <= 12:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.25 and trust < 0.5:
        # Less Untrustworthy
        if delta <= 7: # and time_freq <= 0.8:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    else:
        # Very Untrustworthy
        if delta <= 3: # and time_freq <= 5:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            if trust > 0.0:
                # Min trust value is 0.0
                updated_trust = trust - 0.1
                if updated_trust < 0.0:
                    updated_trust = 0
            else:
                updated_trust = trust
    
    return decision, updated_trust


# x = json.dumps(SLA(0.6, 16))

# print(x)