file_name = get_open_filename("","");
if file_name != "" {
	
	file = file_bin_open(file_name, 0);
	if file != -1 {
		version = "1.0.0";
		world_size = parse_int_array(2, file);
		terrain = parse_2d_array(world_size,file);
		vegetation = parse_2d_array(world_size,file);
		show_debug_message(vegetation[0]);
		with obj_simulation instance_destroy();
		instance_create_depth(200,200,0,obj_simulation, {version: version, world_size: world_size, terrain: terrain, vegetation: vegetation});
	}
}
