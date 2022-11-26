var field_size = 32;
for (var i = 0; i < world_size[0]; i++) {
	for (var j = 0; j < world_size[1]; j++) {
		draw_sprite(spr_field, real(terrain[i][j]),x+i*field_size,y+ j*field_size);
		var veg = real(vegetation[i][j])+1;
		if veg == 256 veg = 0;
		draw_sprite(spr_vegetation, veg,x+i*field_size,y+ j*field_size);
	}
}