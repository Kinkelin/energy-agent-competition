
function string_split(text, delimiter){
	var token_nr = 0;
	var tokens;
	tokens[0] = "";
	for (var i = 1; i < string_length(text)-1; i++) { //Loop over text, ignore cr lf at the end
		var c = string_char_at(text, i);
		if c == delimiter {
			token_nr += 1;
			tokens[token_nr] = "";
		} else {
			tokens[token_nr] += c;
		}
	}
	return tokens;
}

function string_parse_2d_array(size, token) {
	var array = array_create(size[0]);
	var row = 0;
	var column = 0;
	for (var i = 2; i < string_length(token); i++) { //Loop through token, ignore outer array brackets
		var c = string_char_at(token, i);
		switch c {
			case "[":
				array[row] = array_create(size[1],"");
				break;
			case "]":
				row += 1;
				column = 0;
				break;
			case " ":
				column += 1;
				break;
			default:
				show_debug_message(array);
				array[row][column] += c;
				break;
		}
	}
	return array;
}