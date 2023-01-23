SOLC_VERSION=0.8.6 certoraRun Manager.sol:Manager --verify Manager:ManagerPostcondition.spec \
--send_only \
--msg "$1"