// $ node csv-to-sheets.js path/to/punten.csv klas
// $ node csv-to-sheets.js '../../docs/_data/webtechnology/file.csv' 5AD

// SETTINGS
let outputPath =  '/home/hanne/Documents/School/Code/maesbot-private-data/punten';

/* ********************************************************************************************************************************* */

const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const ExcelJS = require('exceljs');
const { exec } = require('child_process');

/* ***************************** */
/* HANDLE COMMAND LINE ARGUMENTS */
/* ***************************** */

let csvFile;
let klas;

const args = process.argv.slice(2);
if (args.length >= 2) {
	csvFile = args[0];
	klas = args[1];

	console.log();
	console.log('Settings:');
	console.log('✅ CSV file:', csvFile);
	console.log('✅ Klas:', klas);
	console.log('✅ Output path:', outputPath);
} else {
	console.log();
	console.log("❌ Command line arguments need to be like this:");
	console.log("node csv-to-sheets.js path/to/punten.csv klas output/path");

	process.exit(); // stop script
}

// Handle klas
let names
if (klas == "5AD") {
	names = ['Bibi Yassine', 'Bicer M.Kerem', 'Coremans Victor', 'Gallardo Ledon Dante', 'Niz Ferreira Tiago', 'Tahrioui Nouredine', 'Van Ballaert Bram', 'Watthé Yorbe', 'Yazrak Noureddine', 'Dierckx Xibe', 'Ghafori Baharah'];
} else {
	console.log();
	console.log("❌ Klas", klas, "is not known.");
}

/* *************************** */
/* CREATE SHEETS FROM CVS FILE */
/* *************************** */
console.log();

// create a new dir to put the files in
const fileNameWithoutExtension = path.basename(csvFile, path.extname(csvFile));
const directoryPath = outputPath + '/' + fileNameWithoutExtension;

fs.mkdir(directoryPath, { recursive: true }, (err) => {
	if (err) {
		console.error('❌ Error creating directory:', err);
	} else {
		console.log('📁 Dir created:', directoryPath);
	}
});

// create a new dir for the verbeterde punten sheets
const directoryPathVerbeterd = directoryPath + '/' + fileNameWithoutExtension + '-verbeterd';
fs.mkdir(directoryPathVerbeterd, { recursive: true }, (err) => {
	if (err) {
		console.error('❌ Error creating directory:', err);
	} else {
		console.log('📁 Dir created:', directoryPathVerbeterd);
		console.log();
	}
});

// Read CSV file
fs.createReadStream(csvFile)
	.pipe(csv())
	.on('data', (row) => {
		//console.log(row); // Do something with each row if needed
	})
	.on('end', () => {
	// Iterate over each name
	names.forEach((nameStudent) => {
	
		// Convert CSV to sheet
		const workbook = new ExcelJS.Workbook();
		const worksheet = workbook.addWorksheet('Sheet1');
		let total = 0; // Variable to store the total of column B

		// Read CSV file to add data to sheet worksheet
		fs.createReadStream(csvFile)
		.pipe(csv())
		.on('data', (row) => {
			worksheet.addRow(Object.values(row));

			// Sum the values in column C
			total += parseInt(row['punt'], 10) || 0;
		})
		.on('end', () => {
			// Punten / totaal
			worksheet.getCell('E1').value = 'Punten';
			worksheet.getCell('E2').value = { formula: '=SUM(B:B)' };

			worksheet.getCell('F1').value = '/ totaal';
			worksheet.getCell('F2').value = { formula: '=SUM(C:C)' };
		
			// Ensure the output directory exists
			fs.mkdirSync('output', { recursive: true });

			// Save sheet file to the output directory
			outputFile = directoryPath + '/' + nameStudent + '.xlsx';
			workbook.xlsx.writeFile(outputFile)
				.then(() => {
					console.log('📗', nameStudent);
				})
				.catch((err) => {
					console.error('❌', nameStudent, 'error:', err);
				});

		});
	});
});

/* ************ */
/* OPEN NEW DIR */
/* ************ */

exec(`xdg-open ${directoryPath}`);	// Linux
// exec(`open ${directoryPath}`); 	// MacOs
// exec(`start ${directoryPath}`);	// Windows