methods {
    getStateById(uint256) returns (uint8) envfree
    getStartTimeById(uint256) returns (uint256) envfree
    getEndTimeById(uint256) returns (uint256) envfree
    getNumOfParticipents(uint256) returns (uint256) envfree
}

definition uninitialized(uint256 meetingId) returns bool = 
        getStartTimeById(meetingId) == 0 &&
        getEndTimeById(meetingId) == 0 &&
        getNumOfParticipents(meetingId) == 0 &&
        getStateById(meetingId) == 0;

definition initialized(uint256 meetingId) returns bool =
        getStartTimeById(meetingId) != 0 &&
        getEndTimeById(meetingId) != 0 &&
        getStateById(meetingId) != 0;

function callFunctionWithParams(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
    env e;

    if (f.selector == scheduleMeeting(uint256,uint256,uint256).selector) {
        scheduleMeeting(e, meetingId, startTime, endTime);
    } else if (f.selector == startMeeting(uint256).selector) {
        startMeeting(e, meetingId);
    } else if (f.selector == cancelMeeting(uint256).selector) {
        cancelMeeting(e, meetingId);
    } else if (f.selector == endMeeting(uint256).selector) {
        endMeeting(e, meetingId);
    } else if (f.selector == joinMeeting(uint256).selector) {
        joinMeeting(e, meetingId);
    } else {
        calldataarg args;
        f(e, args);
    }
}


// TODO: I don't know how to enforce that the parametric function calls each need to use a specific
// meetingId. Gotta ask Mike
// any 2 functions called on 2 different meetingId's will have no effect on each other's meetings
// rule aChangeToOneMeetingDoesNotAffectTheOther(uint256 meetingId1, uint256 meetingId2) {
//     env e1; calldataarg args1;
//     env e2; calldataarg args2;
//     method f1;
//     method f2;

//     // call the parametric function on two different meetings
//     require meetingId1 != meetingId2;

//     // get the state of the 2 meetings before the calls
//     uint8 status1Before; uint256 startTime1Before; uint256 endTime1Before; uint256 numParticipants1Before;
//     status1Before = getStateById(meetingId1);
//     startTime1Before = getStartTimeById(meetingId1);
//     endTime1Before = getEndTimeById(meetingId1);
//     numParticipants1Before = getNumOfParticipents(meetingId1);

//     uint8 status2Before; uint256 startTime2Before; uint256 endTime2Before; uint256 numParticipants2Before;
//     status2Before = getStateById(meetingId2);
//     startTime2Before = getStartTimeById(meetingId2);
//     endTime2Before = getEndTimeById(meetingId2);
//     numParticipants2Before = getNumOfParticipents(meetingId2);


//     f1(e1, args1);

//     // TODO

//     assert true;

// }


// TODO: i don't know how to compare reachability of 2 function calls (1 by the organizer, the other
// by the non-organizer using the `storage` syntax. Gotta ask Mike)
// all function calls that succeed for a non-organizer would all succeed for an organizer
// rule nonOrganizerCallsAlwaysSucceedForOrganizer(address nonOrganizer, address organizer) {
//     env e; calldataarg args;

//     require e.msg.sender == organizer;


//     // I wanna check, if we start in the same state, and then consider 2 possibilities:
//     // 1. an organizer calls a function
//     // 2. a non-organizer calls a function
//     // then there should be no instances where non-organizer succeeds, and organizer fails
//     // another way of saying this is that the set of successful function calls for organizer
//     // is a superset of the non-organizer's set of successful function calls


//     // take a snapshot of the state so we can compare 
//     storage initial = lastStorage;
// }

// after a transition to the ENDED (status = 3), then block.timestamp > endTime
rule stateOfEnded(uint256 meetingId) {
    env e;

    uint256 stateBefore = getStartTimeById(meetingId);
    // we want to ensure we're in the right initial state, which if
    // we're trying to transition to ENDED means we must be in the STARTED
    // (status = 2) state
    require stateBefore == 2;

    endMeeting(e, meetingId);

    uint256 endTimeAfter = getEndTimeById(meetingId);
    uint8 stateAfter = getStateById(meetingId);

    assert (stateAfter == 3, "unexpected state");
    assert (e.block.timestamp > endTimeAfter, "block.timestamp is before the end time");
}

rule stateOfEndedParametric(uint256 meetingId) {
    env e;
    method f;
    calldataarg args;

    require getStateById(meetingId) != 3;

    f(e, args);
    uint8 stateAfter = getStateById(meetingId);

    // ensure that the status transitioned to ENDED
    require stateAfter == 3;

    uint256 endTimeAfter = getEndTimeById(meetingId);

    assert (e.block.timestamp >= endTimeAfter, "block.timestamp is before the end time");
}

// once a meeting is in the ENDED state, every non-view function called
// on it should revert (ENDED should be a terminal state)
rule endStateShouldCauseFailureForAllNonViewFunctions(uint256 meetingId, uint256 startTime, uint256 endTime) {
    method f;

    require f.isView == false;

    uint8 stateBefore = getStateById(meetingId);
    require stateBefore == 3;

    callFunctionWithParams(f, meetingId, startTime, endTime);

    assert false;
}

rule uninitializedStateTransition(uint256 meetingId) {
    method f;
    env e;
    calldataarg args;

    uint256 stateBefore = getStateById(meetingId);

    require stateBefore == 0;

    f(e, args);

    uint256 stateAfter = getStateById(meetingId);

    assert (stateBefore != stateAfter => f.selector == scheduleMeeting(uint256,uint256,uint256).selector, "some other function was called!");
}