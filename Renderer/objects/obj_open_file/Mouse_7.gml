file_name = get_open_filename("","");
if file_name != "" {
	
	file = file_bin_open(file_name, 0);
	if file != -1 {
		
		// HEADER
		title = parse_string(64, file);
		version = parse_short(file);
		world_size = parse_short_array(2, file);
		show_debug_message(world_size);
		terrain = parse_2d_array(world_size,file);
		//show_debug_message(terrain);
		vegetation = parse_2d_array(world_size,file);
		//show_debug_message(vegetation);
		number_of_strategies = parse_short(file);
		number_of_agents_per_strategy = parse_short(file);
		with obj_simulation instance_destroy();
		instance_create_depth(200,200,0,obj_simulation, {version: version, world_size: world_size, terrain: terrain, vegetation: vegetation});
	}
}
