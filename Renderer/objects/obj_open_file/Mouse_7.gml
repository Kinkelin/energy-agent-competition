file_name = get_open_filename("","");
if file_name != "" {
	
	file = file_bin_open(file_name, 0);
	if file != -1 {
		world_size = [500,500];
		terrain = parse_2d_array(world_size,file);
		version = "1.0.0";
		with obj_simulation instance_destroy();
		instance_create_depth(200,200,0,obj_simulation, {version: version, world_size: world_size, terrain: terrain});
	}
}
