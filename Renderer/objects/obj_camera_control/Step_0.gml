left = keyboard_check(vk_left);
right = keyboard_check(vk_right);
up = keyboard_check(vk_up);
down = keyboard_check(vk_down);
cam_speed = 10;

//camera_set_view_pos(view_camera[0], 
//	camera_get_view_x(view_camera[0])-left*cam_speed+right*cam_speed,
//	camera_get_view_y(view_camera[0])-up*cam_speed+down*cam_speed);

in = keyboard_check(ord("O"));
out = keyboard_check(ord("P"));
show_debug_message(in);
zoom -= in * zoom_speed;
show_debug_message(zoom);
zoom += out * zoom_speed;
actual_zoom = power(zoom,1.5);

camera_set_view_size(view_camera[0], 1920*actual_zoom, 1080*actual_zoom);