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

definition UNINITIALIZED() returns uint256 = 0;

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

// any function called on meeting #1 will have no effect on another meeting
rule aChangeToOneMeetingDoesNotAffectTheOther(uint256 meetingId1, uint256 meetingId2) {
    env e1; calldataarg args1;
    env e2; calldataarg args2;
    method f1;
    method f2;

    // call the parametric function on two different meetings
    require meetingId1 != meetingId2;

    // get the state of the 2 meetings, #1 and #2, before making a function call
    
    uint256 startTime1Before; uint256 endTime1Before;
    startTime1Before = getStartTimeById(meetingId1);
    endTime1Before = getEndTimeById(meetingId1);

    uint8 status2Before; uint256 startTime2Before; uint256 endTime2Before; uint256 numParticipants2Before;
    status2Before = getStateById(meetingId2);
    startTime2Before = getStartTimeById(meetingId2);
    endTime2Before = getEndTimeById(meetingId2);
    numParticipants2Before = getNumOfParticipents(meetingId2);

    // make the state change on #1
    callFunctionWithParams(f1, meetingId1, startTime1Before, endTime1Before);

    // check that calls to #1 had no effect on #2
    uint8 status2After; uint256 startTime2After; uint256 endTime2After; uint256 numParticipants2After;
    status2After = getStateById(meetingId2);
    startTime2After = getStartTimeById(meetingId2);
    endTime2After = getEndTimeById(meetingId2);
    numParticipants2After = getNumOfParticipents(meetingId2);
    assert (status2Before == status2After, "status changed");
    assert (startTime2Before == startTime2After, "startTime changed");
    assert (endTime2Before == endTime2After, "endTime changed");
    assert (numParticipants2Before == numParticipants2After, "numParticipants changed");
}



// all function calls that succeed for a non-organizer would all succeed for an organizer
rule nonOrganizerCallsAlwaysSucceedForOrganizer(method f, address nonOrganizer, address organizer) {
    env e1; env e2; calldataarg args;

    require e1.msg.sender == nonOrganizer;
    require e2.msg.sender == organizer;

    require e1.msg.value == e2.msg.value;
    require e1.block.timestamp == e2.block.timestamp;
    require e1.block.number == e2.block.number;

    storage initial = lastStorage;

    f(e1, args);
    bool nonOrgCallSuccess = !lastReverted;

    f(e2, args) at initial;
    bool orgCallSuccess = !lastReverted;

    assert nonOrgCallSuccess => orgCallSuccess, "A function succeeded for the nonOrganizer, but failed for the organizer";
}

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
rule endStateShouldCauseFailureForAllNonViewFunctions(method f, uint256 meetingId, uint256 startTime, uint256 endTime)
    filtered { f -> !f.isView } {

    uint8 stateBefore = getStateById(meetingId);
    require stateBefore == 3;

    callFunctionWithParams@withrevert(f, meetingId, startTime, endTime);

    assert lastReverted;
}

rule uninitializedStateTransition(uint256 meetingId) {
    method f;
    env e;
    calldataarg args;

    uint256 stateBefore = getStateById(meetingId);

    require stateBefore == 0;

    f(e, args);

    uint256 stateAfter = getStateById(meetingId);

    assert (stateBefore != stateAfter => f.selector == scheduleMeeting(uint256,uint256,uint256).selector &&
        stateAfter == 1, "the state transition is invalid");
}

// TODO write rules 6, 7, 8, 9 from 06.Lesson_ThinkingProperties/meetingscheduler_properties_solution, which
// all are of the same form as the above rule

// numParticipants should never decrease
rule numParticipantsShouldNeverDecrease(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    uint256 numParticipantsBefore = getNumOfParticipents(meetingId);
    uint8 stateBefore = getStateById(meetingId);

    // need to handle the case where scheduleMeeting can be called (and set
    // numParticipants to 0) and not called in a separate manner
    if (stateBefore == 0) {
        // if the state is unitialized, then we assume nothing has been done with
        // the meeting, so assuming numParticipants == 0 is a sound assumption
        require numParticipantsBefore == 0;
    }

    f(e, args);

    uint256 numParticipantsAfter = getNumOfParticipents(meetingId);

    assert (numParticipantsBefore <= numParticipantsAfter, "numParticipants decreased");
}

// TODO: figure out why the assert at the end is passing, even though it shouldn't.
// I think this should not pass because it is possible for the `scheduleMeeting` call
// to revert when `state == 0` (specifically, if state == 0 && startTime > endTime).
// How come the CVT isn't finding any errors, am I using @withrevert incorrectly?
//
// Verification Report: https://prover.certora.com/output/20739/30f1a79670be41648dafead9b4c6604a?anonymousKey=2f01c25f3a82e050ce9a48b765c12d02c2f55e64
// scheduleMeeting meeting should only fail on a particular set of inputs
rule scheduleMeetingWorksCorrectly(uint256 meetingId, method f, uint256 startTime, uint256 endTime) {
    env e;
    calldataarg args;

    uint8 state = getStateById(meetingId);

    scheduleMeeting@withrevert(e, meetingId, startTime, endTime);

    bool didRevert = lastReverted;

    assert (didRevert => (state != 0 || e.msg.value != 0 || (e.block.timestamp >= startTime || startTime >= endTime)));
}