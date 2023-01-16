
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

rule neverReachedPlayer4Parametric(method f, env e, calldataarg args) {
	uint256 ballPosition = ballAt();

	require ballPosition == 1;

	f(e, args);

	uint256 newBallPosition = ballAt();
	assert(newBallPosition != 4, "ball managed to get into position 4");
}