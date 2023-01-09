SOLC_VERSION=0.8.7 certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetingscheduler.spec \
--msg "$1" \
--rule aChangeToOneMeetingDoesNotAffectTheOther
