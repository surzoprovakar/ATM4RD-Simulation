Rules = {}

Rules.update({tuple((90, 100)) : lambda d: d <= 12})
Rules.update({tuple((65, 89)) : lambda d: d <= 10})
Rules.update({tuple((50, 64)) : lambda d: d <= 8})
Rules.update({tuple((25, 49)) : lambda d: d <= 5})
Rules.update({tuple((0, 24)) : lambda d: d <= 2})


def sla(trust, delta):
    
    idx = None
    check = None
    for i, ele in enumerate(Rules.keys()):
        if  trust >= ele[0]  and trust <= ele[1]:
            idx = i
            x = Rules[ele]
            check = x(delta)
            break
    
    return action(idx, check, trust)

    

def action(idx, check, trust):
    decision = ""
    updated_trust = 0

    if idx >= 3:
        decision = "Ignored"
        if check == True:
            updated_trust = trust + 5
        else:
            updated_trust = trust - 5
    else:
        if check == True:
            decision = "Accepted"
            updated_trust = trust + 5
        else:
            decision = "Ignored"
            updated_trust = trust - 5

    if updated_trust > 100:
        updated_trust = 100

    if updated_trust < 0:
        updated_trust = 0

    return decision, updated_trust


def SLA_Old(trust, delta):
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
