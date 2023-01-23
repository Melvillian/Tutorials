SOLC_VERSION=0.8.6 certoraRun ManagerBug2.sol:Manager --verify Manager:Manager.spec \
--send_only \
--msg "$1"