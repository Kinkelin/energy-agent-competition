///Text files are not performant enough
ReadTextFile = function() {
	show_debug_message("File loaded: "+ string(file));
		var line_number = 0;
		var delimiter = ";";
		var finish = false;
		while (!finish and !file_text_eof(file)) {
			line_number++;
			show_debug_message("read line: "+string(line_number));
			line = file_text_readln(file);
			
			var tokens = string_split(line, delimiter);
			show_debug_message(tokens);
			switch tokens[0] {
				case "VERSION":
					version = tokens[1];
					break;
				case  "WORLD_SIZE":
					world_size = [tokens[1], tokens[2]];
					break;
				case "TERRAIN":
					terrain = parse_2d_array(world_size, tokens[1]);
					break;
				case "STEPS":
					finish = true;
					break;
					
			}
			
		}
}