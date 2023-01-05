# Rules

## Takeaways
1. proving valid states is hard when using rules because you need a bunch possibly unsound `require`s
2. For the State Transitions when you're narrowing down the function selectors to a allowlisted set, you should use `filter` because that will be speedier

## Valid States

def uninitialized:
    - startTime and endTime are 0
    - numOfParticipants is 0
    - organizer is 0
    - status is UNINITIALIZED

def initialized:
    - startTime and endTime are nonzero
    - status is not UNINITIALIZED




1. if status is UNINITIALIZED, then state should be uninitialized
    - probably want an invariant here
2. if status is not UNINITIALIZED, then state should be initialized
3. if status is ENDED, then block.timestamp must be > endTime 
4. once status is ENDED, every non-view function should revert

## State Transitions

5. starting in uninitialized state, the only non-reverting non-view function should be scheduleMeeting
6. If the state changed from UNINITIALIZED to PENDING, the only way that could happen is if `scheduleMeeting` was called
7. If the state changed from PENDING to STARTED, the only way that could happen is if `startMeeting` was called
8. If the state changed from STARTED to CANCELLED, the only way that could happen is if `cancelMeeting` was called
9. If the state changed from STARTED to ENDED, the only way that could happen is if `endMeeting` was called


## Variable Transitions

10. (parametric) numParticipants should only increase or stay the same, never decrease

## High-Level Properties

11. (parametric) All functions that succeed for a non-organizer user would also succeed for an organizer
12. (parametric) The status value can never decrease, only increase or stay the same

## Unit Tests

13. `scheduleMeeting` should only fail if the same meetingId is used and startTime, endTime are both zero
14. `joinMeeting` always increases numParticipants by exactly 1


## Risk Analysis

15. (parametric) any 2 function calls acting on different meetingId's should have no impact on each other


# Rule Priority

## High Priority

- #15 is HP because it ensures 2 meetings are logically distinct. If this is false, then there is a subtle dependency between 2 meetings when there should not be
- #11 is HP because then it means non-owners have extra permissions that they should not, and they might be malicious
- #3 is HP, otherwise the meeting's basic property is not met (ends after endTime)
- #10, because if participants can decrease, then that means someone can be removed, which would be very bad

## Medium Priority

- #1, because this might be DoS where some nonzero state prevents a transition to PENDING
- #2, same as reason above, but it could DoS it by not allowing a state transition to a NON-PENDING state
- #4, because otherwise ENDED is not a terminal state and something might happen to a meeting after everyone assumes it's done
- #5, because then some state transition that shouldn't be allowed, is in fact allowed
- #6, for same reason as above
- #7, #8, #9 for same reason as above
- #12, for same reason as above
- #14, because then it's counter the the spec, but it may not be damaging

## Low Priority

- #13, because it would only affect PENDING meetings, which people care less about