
methods {
    transactionFee() returns (uint64) envfree
    owner() returns (address) envfree
}

ghost uint256 numberOfEvents;

hook Sstore numEvents uint16 v STORAGE {
    numberOfEvents = numberOfEvents;
}


// only createEvent can change the number of events
rule createEventIsOnlyFunctionThatCanIncreaseNumEvents() {
    method f;
    env e;
    calldataarg args;

    uint256 nEventsBefore = numberOfEvents;

    f(e, args);

    uint256 nEventsAfter = numberOfEvents;

    assert (nEventsBefore != nEventsAfter <=> f.selector == createEvent(uint64, uint16).selector, "something unexpected happened with numEvents");
}