SOLC_VERSION=0.6.12 certoraRun TicketDepot.sol --verify TicketDepot:ticketdepot.spec \
--msg "$1" \
--rule createEventIsOnlyFunctionThatCanIncreaseNumEvents
