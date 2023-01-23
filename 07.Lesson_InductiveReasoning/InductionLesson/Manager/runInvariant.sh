SOLC_VERSION=0.8.6 certoraRun Manager.sol:Manager --verify Manager:Manager.spec \
--send_only \
--msg "$1"
--rule "uniqueManagerAsInvariant"