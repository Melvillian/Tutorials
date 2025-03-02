pragma solidity ^0.8.7;

/** Meeting Scheduler Overview
 * @dev This contract simulate a meeting scheduler for various uses.
 * 
 * The scheduler follows a very clear path through different states of meeting's life.
 * The system allows one to create a schedule, defining start & end of the meeting.
 * The scheduler also tracks the number of participants attending the meeting.
 *
 * - The meetings in the system are going through the following states - before creation they are
 * classified as UNINITIALIZED.
 *
 * - At creation the state change to PENDING, the start & end time are being set according to 
 * organizer's order, and the num of participants are nullified.
 *
 * - At this point a meeting can be started by anybody if start time has arrived (change to STARTED),
 * or be cancelled (change to CANCELLED) by owner. A meeting that has already occured can not be labeld CANCELLED.
 *
 * - In case that the meeting has already started and the end time arrived, anybody can change the status
 * to ENDED.
 * 
 * UNITIALIZED
 * PENDING
 * STARTED
 * CANCELLED
 * ENDED
 */

interface IMeetingScheduler {
    
    enum MeetingStatus {
        UNINITIALIZED, 
        PENDING,
        STARTED,
        ENDED,
        CANCELLED
    }

    struct ScheduledMeeting {
        uint256 startTime;
        uint256 endTime;
        uint256 numOfParticipents;
        address organizer;
        MeetingStatus status;
    }

    // Gets the status of a specified meetingId
    function getStateById(uint256 meetingId)
        external
        view
        returns (MeetingStatus);

    // Gets the start time of a specified meetingId
    function getStartTimeById(uint256 meetingId)
        external
        view
        returns (uint256);

    // Gets the end time of a specified meetingId
    function getEndTimeById(uint256 meetingId) external view returns (uint256);

    // Gets the number of participants of a specified meetingId
    function getNumOfParticipents(uint256 meetingId)
        external
        view
        returns (uint256);

    // Gets the organizer of a specified meetingId
    function getOrganizer(uint256 meetingId)
        external
        view
        returns (address);

    // Creates a registry of meetingId in the map and updating its details.
    function scheduleMeeting(
        uint256 meetingId,
        uint256 startTime,
        uint256 endTime
    ) external;

    // Changes the status of a meeting to STARTED
    function startMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to CANCELLED if it hasn't started yet
    function cancelMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to ENDED only if it really occured
    function endMeeting(uint256 meetingId) external;

    // Increases a meeting's participants' count
    function joinMeeting(uint256 meetingId) external;
}
