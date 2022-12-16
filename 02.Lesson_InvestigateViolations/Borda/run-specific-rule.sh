SOLC_VERSION=0.7.6 certoraRun BordaBug1.sol:Borda --verify Borda:Borda.spec \
--rule "$1" \
--msg "$2"
