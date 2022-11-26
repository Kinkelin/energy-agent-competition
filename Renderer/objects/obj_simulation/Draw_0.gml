var field_size = 32;
for (var i = 0; i < world_size[0]; i++) {
	for (var j = 0; j < world_size[1]; j++) {
		draw_sprite(spr_field, real(terrain[i][j]),x+i*field_size,y+ j*field_size);
	}
}