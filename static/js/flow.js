jQuery(document).ready(function ( $ ) {
	$("#hotbooks").mpmansory(
		{
			childrenClass: 'item', // default is a div
			columnClasses: 'padding', //add classes to items
			breakpoints:{
				lg: 3, 
				md: 4, 
				sm: 6,
				xs: 12
			},
			distributeBy: { order: true, height: false}, //default distribute by order, options => order: true/false, height: true/false, attr => 'data-order', attrOrder=> 'asc'/'desc'
			onload: function (items) {
				//make somthing with items
			} 
		}
	);
});