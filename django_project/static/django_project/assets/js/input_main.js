/*
	Future Imperfect by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/
if (document.querySelector("#main > article > header > div > div > h2 > font").textContent.startsWith('GHG')) { document.addEventListener("DOMContentLoaded", ghg_aggregate()); }

console.log(document.querySelector("#main > article > header > div > div > h2 > font").textContent.startsWith('GHG'))
const fileTypes = [
	'image/apng',
	'image/bmp',
	'image/gif',
	'image/jpeg',
	'image/pjpeg',
	'image/png',
	'image/svg+xml',
	'image/tiff',
	'image/webp',
	`image/x-icon`,
	'application/pdf',
];

function ghg_aggregate() {
	const scope1 = convertFormattedTextToNumber(document.getElementById('id_ghg_scope_1'));
	const scope2loc = convertFormattedTextToNumber(document.getElementById('id_ghg_loc_scope_2'));
	const scope2mkt = convertFormattedTextToNumber(document.getElementById('id_ghg_mkt_scope_2'));

	document.getElementById('total_scope1_2_loc').innerText = formatNumberToFormattedText(scope1 + scope2loc);
	document.getElementById('total_scope1_2_mkt').innerText = formatNumberToFormattedText(scope1 + scope2mkt);
	var scope3_loc = 0;
	const all_categories_loc = [
		"id_ghg_purch_scope3",
		"id_ghg_capital_scope3",
		"id_ghg_fuel_energy_loc_scope3",
		"id_ghg_upstream_td_scope3",
		"id_ghg_waste_ops_scope3",
		"id_ghg_bus_travel_scope3",
		"id_ghg_commute_scope3",
		"id_ghg_up_leased_scope3",
		"id_ghg_downstream_td_scope3",
		"id_ghg_proc_sold_scope3",
		"id_ghg_use_sold_scope3",
		"id_ghg_eol_sold_scope3",
		"id_ghg_down_leased_scope3",
		"id_ghg_franchises_scope3",
		"id_ghg_investments_scope3",
		"id_ghg_other_upstream_scope3",
		"id_ghg_other_downstream_scope3"
	];
	for (const element of all_categories_loc) {
		scope3_loc += convertFormattedTextToNumber(document.getElementById(element));
	}
	document.getElementById('total_scope_3_loc').innerText = formatNumberToFormattedText(scope3_loc);
	document.getElementById('total_scope1_2_3_loc').innerText = formatNumberToFormattedText(scope1 + scope2loc + scope3_loc);

	var scope3_mkt = 0;
	const all_categories_mkt = [
		"id_ghg_purch_scope3",
		"id_ghg_capital_scope3",
		"id_ghg_fuel_energy_mkt_scope3",
		"id_ghg_upstream_td_scope3",
		"id_ghg_waste_ops_scope3",
		"id_ghg_bus_travel_scope3",
		"id_ghg_commute_scope3",
		"id_ghg_up_leased_scope3",
		"id_ghg_downstream_td_scope3",
		"id_ghg_proc_sold_scope3",
		"id_ghg_use_sold_scope3",
		"id_ghg_eol_sold_scope3",
		"id_ghg_down_leased_scope3",
		"id_ghg_franchises_scope3",
		"id_ghg_investments_scope3",
		"id_ghg_other_upstream_scope3",
		"id_ghg_other_downstream_scope3"
	];
	for (const element of all_categories_mkt) {
		scope3_mkt += convertFormattedTextToNumber(document.getElementById(element));
	}
	document.getElementById('total_scope_3_mkt').innerText = formatNumberToFormattedText(scope3_mkt);
	document.getElementById('total_scope1_2_3_mkt').innerText = formatNumberToFormattedText(scope1 + scope2mkt + scope3_mkt);
}

$('[id*=id_ghg_]').keyup(function (event) {

	// skip for arrow keys
	if (event.which >= 37 && event.which <= 40) return;

	$(this).val(function (index, value) {
		return value
			.replace(/\D/g, "")
			.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	});
	ghg_aggregate();

});


(function ($) {

	var $window = $(window),
		$body = $('body'),
		$menu = $('#menu'),
		$sidebar = $('#sidebar'),
		$main = $('#main');

	// Breakpoints.
	breakpoints({
		xlarge: ['1281px', '1680px'],
		large: ['981px', '1280px'],
		medium: ['737px', '980px'],
		small: ['481px', '736px'],
		xsmall: [null, '480px']
	});

	// Play initial animations on page load.
	$window.on('load', function () {
		window.setTimeout(function () {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Menu.
	$menu
		.appendTo($body)
		.panel({
			delay: 500,
			hideOnClick: true,
			hideOnSwipe: true,
			resetScroll: true,
			resetForms: true,
			side: 'right',
			target: $body,
			visibleClass: 'is-menu-visible'
		});

	// Search (header).
	var $search = $('#search'),
		$search_input = $search.find('input');

	$body
		.on('click', '[href="#search"]', function (event) {

			event.preventDefault();

			// Not visible?
			if (!$search.hasClass('visible')) {

				// Reset form.
				$search[0].reset();

				// Show.
				$search.addClass('visible');

				// Focus input.
				$search_input.focus();

			}

		});

	$search_input
		.on('keydown', function (event) {

			if (event.keyCode == 27)
				$search_input.blur();

		})
		.on('blur', function () {
			window.setTimeout(function () {
				$search.removeClass('visible');
			}, 100);
		});

	// Intro.
	var $intro = $('#intro');

	// Move to main on <=large, back to sidebar on >large.
	breakpoints.on('<=large', function () {
		$intro.prependTo($main);
	});

	breakpoints.on('>large', function () {
		$intro.prependTo($sidebar);
	});

})(jQuery);

function updateFile(input) {

	const preview = $(input).closest('.single-file').find('.preview')[0];
	const clear = $(input).closest('.single-file').find('.clear_option')[0];
	const curFiles = input.files;
	const para = document.createElement('div');
	const para2 = document.createElement('div');

	para.className = "upload-filename";

	if (curFiles.length === 0) {
		para.textContent = 'No files currently selected for upload';
		preview.appendChild(para);
	} else {
		const file = curFiles[0];
		while (preview.firstChild) {
			preview.removeChild(preview.firstChild);
		}
		if (clear) {
			while (clear.firstChild) {
				clear.removeChild(clear.firstChild);
			}
		}

		if (validFileType(file)) {
			para.textContent = `File selected: ${file.name}`;
			preview.appendChild(para);
			para2.textContent = `Size: ${returnFileSize(file.size)}.`;
			preview.appendChild(para2);

		} else {
			para.textContent = `File name ${file.name}: Not a valid file type. Update your selection.`;
			preview.appendChild(para);
		}
	}
}

function validFileType(file) {
	return fileTypes.includes(file.type);
}

function returnFileSize(number) {
	if (number < 1024) {
		return number + 'bytes';
	} else if (number > 1024 && number < 1048576) {
		return (number / 1024).toFixed(1) + 'KB';
	} else if (number > 1048576) {
		return (number / 1048576).toFixed(1) + 'MB';
	}
}

$(document).ready(function () {

	$(".btn-new").on('click', function () {
		if ($(".single-file").length < 5) {
			const upload_idx = ($(".single-file").length + 1).toString();
			const input_id = "id_upload_" + upload_idx;
			const input_name = "upload_" + upload_idx;
			const html_insert = "<div class='single-file' ><div class='merged-label-input'>\
<label class='upload-clickable-label' for='"+ input_id + "'>\
Upload</label><input class='upload-file-input'\
 type='file' id='"+ input_id + "' name='" + input_name + "'\
 accept='.jpg, .jpeg, .png, .pdf' onchange='updateFile(this)'></div>\
 <div class='preview'>No files currently selected for upload\
 </div></div>"
			$("#upload_files").append(html_insert);
		}
		else {
			alert("Max 5 files");
		}
	});
});




