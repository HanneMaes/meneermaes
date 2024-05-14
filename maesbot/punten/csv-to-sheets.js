// $ node csv-to-sheets.js '../../docs/_data/webtechnology/file.csv' 5AD

const fs = require('fs');
const csv = require('csv-parser');
const ExcelJS = require('exceljs');
const path = require('path');

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
	console.log('CSV file:', csvFile);
	console.log('Klas:', klas);
} else {
	console.log();
	console.log("❌ Command line arguments need to be like this:");
	console.log("node csv-to-sheets.js ../../docs/_data/webtechnology/file.csv 5AD");

	process.exit(); // stop script
}

// Handle klas
let names
if (klas == "5AD") {
	names = ['Bibi Yassine', 'Bicer M.Kerem', 'Coremans Victor', 'Dante Gallardo Ledon', 'Tiago Niz Ferreira', 'Nouredine Tahrioui', 'Bram Van Ballaert', 'Yorbe Watthé', 'Noureddine Yazrak', 'Xibe Dierckx', 'Baharah Ghafori'];
} else {
	console.log();
	console.log("❌ Klas", klas, "is not known.");
}

/* *************************** */
/* CREATE SHEETS FROM CVS FILE */
/* *************************** */
console.log();

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
		
		// Read CSV file again to add data to sheet worksheet
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
			outputFile = 'output/' + /*path.parse(csvFile).name + '/' +*/ nameStudent + '.xlsx';
			workbook.xlsx.writeFile(outputFile)
			.then(() => {
				console.log('🔨', nameStudent, '➡️', outputFile);
			})
			.catch((err) => {
				console.error('❌', nameStudent, 'error:', err);
			});
		});
	});
  });