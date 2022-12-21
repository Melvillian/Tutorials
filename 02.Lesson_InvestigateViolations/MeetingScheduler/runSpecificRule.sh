SOLC_VERSION=0.8.7 certoraRun MeetingSchedulerBug1.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--send_only \
--rule "$1" \
--msg "$2"