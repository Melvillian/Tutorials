methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	// assume different managers
	address oldM1 = getCurrentManager(fundId1);
	address oldM2 = getCurrentManager(fundId2);
	require oldM1 != oldM2;

	bool active1 = isActiveManager(getCurrentManager(fundId1));	
	bool active2 = isActiveManager(getCurrentManager(fundId2));	

	// assume each manager is either active and a current manager,
	// or not active and not a current manager
	require ((oldM1 != 0x0) && active1) || ((oldM1 == 0) && !active1);
	require ((oldM2 != 0x0) && active2) || ((oldM2 == 0) && !active2);

	
	// hint: add additional variables just to look at the current state
	
	env e;
	calldataarg args;
	f(e,args);

	address m1 = getCurrentManager(fundId1);
	address m2 = getCurrentManager(fundId2);
	
	// verify that the managers are still different 
	assert m1 != m2, "managers not different";
}


// /* A version of uniqueManagerAsRule as an invariant */
// invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
// 	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
