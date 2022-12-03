var field_size = 128;
draw_set_color(c_grey);
var x1 = x - field_size*(view_x+0.5);
var y1 = y - field_size*(view_y+0.5);
draw_rectangle(x1,y1,x1+field_size*world_size[0], y1+field_size*world_size[1],false);
for (var i = 0; i < 128; i++) {
	for (var j = 0; j < 128; j++) {
		var field_x = view_x+i;
		var field_y = view_y+j;
		
		if field_x >= 0 and field_x < world_size[0] and field_y >= 0 and field_y < world_size[1] {
			draw_sprite(spr_field2, real(terrain[field_x][field_y]),x+i*field_size,y+ j*field_size);
			var veg = real(vegetation[field_x][field_y])+1;
			if veg < 10 draw_sprite(spr_vegetation2, veg,x+i*field_size,y+ j*field_size);
		}
		
	}
	
}
