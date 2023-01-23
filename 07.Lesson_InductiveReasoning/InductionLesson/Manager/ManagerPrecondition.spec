methods {
		getCurrentManager(uint256 fundId) returns (address) envfree
		getPendingManager(uint256 fundId) returns (address) envfree
		isActiveManager(address a) returns (bool) envfree
}



rule uniqueManager(uint256 fundId1, uint256 fundId2, method f) {
	require fundId1 != fundId2;
	// require getCurrentManager(fundId1) != 0 && isActiveManager(getCurrentManager(fundId1));
	// require getCurrentManager(fundId2) != 0 && isActiveManager(getCurrentManager(fundId2));
	// require getCurrentManager(fundId1) != getCurrentManager(fundId2) ;

	address oldM1 = getCurrentManager(fundId1);
	address oldM2 = getCurrentManager(fundId2);
	require oldM1 != oldM2;
	bool active1 = isActiveManager(getCurrentManager(fundId1));	
	bool active2 = isActiveManager(getCurrentManager(fundId2));	
	// assume each manager is either active and a current manager,
	// or not active and not a current manager
	require ((oldM1 != 0x0) && active1) || ((oldM1 == 0) && !active1);
	require ((oldM2 != 0x0) && active2) || ((oldM2 == 0) && !active2);
				
	env e;
	if (f.selector == claimManagement(uint256).selector)
	{
		uint256 id;
		require id == fundId1 || id == fundId2;
		claimManagement(e, id);  
	}
	else {
		calldataarg args;
		f(e,args);
	}
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	assert getCurrentManager(fundId1) != 0 && isActiveManager(getCurrentManager(fundId1)), "manager of fund1 is not active";
	assert getCurrentManager(fundId2) != 0 && isActiveManager(getCurrentManager(fundId2)), "manager of fund2 is not active";
}



		
	
