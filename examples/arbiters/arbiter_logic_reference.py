def arbiter_governance(packet):
    """
    Example optional policy layer deciding how bridge data should be surfaced.

    The Arbiter is not required by the base protocol and is not the semantic
    source of truth.
    """
    # Example policy: only allow 'Emergency' level 1.0 haptics during 'Work Hours'
    if packet['payload']['metadata']['intensity_suggestion'] == 1.0:
        return {
            "status": "APPROVED",
            "delivery": "IMMEDIATE_HAPTIC"
        }
    
    return {"status": "DEFERRED", "delivery": "VISUAL_QUEUE_ONLY"}
