// SETTINGS
const outputPath = '/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten';
const dataPath='/home/hanne/Documents/Nextcloud/School/maesbot-private-data/klassen-en-leerlingen.json';

/* ********************************************************************************************************************************* */

const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const ExcelJS = require('exceljs');
const { exec } = require('child_process');
const os = require('os');

/* ***************************** */
/* HANDLE COMMAND LINE ARGUMENTS */
/* ***************************** */

let csvFile;
let klas;

const args = process.argv.slice(2);
if (args.length >= 2) {
   csvFile = args[0];
   klas = args[1].toLowerCase(); // Convert to lowercase to prevent typos

   console.log('Settings:');
   console.log('  ℹ️C CSV file:', csvFile);
   console.log('  ℹ️K Klas:', klas);
} else {
   console.log("❌ Command line arguments need to be like this:");
   console.log("node csv-to-sheets.js path/to/punten.csv klas");

   process.exit(); // stop script
}

// read JSON data
fs.readFile(dataPath, 'utf8', (error, data) => {

    // throw error when not able to read the data
    if (error) {
        console.error('Error reading file:', error);
        return;
    }
    const jsonData = JSON.parse(data);

   // assign JSON data to correct vars
   const klassen = jsonData.klassen
	const names = klassen[klas]

   /* *************************** */
   /* CREATE SHEETS FROM CVS FILE */
   /* *************************** */
   console.log();

   // create a new dir to put the files in
   const fileNameWithoutExtension = path.basename(csvFile, path.extname(csvFile));
   const directoryPath = outputPath + '/' + fileNameWithoutExtension + ' ' + klas;

   fs.mkdir(directoryPath, { recursive: true }, (err) => {
      if (err) {
         console.error('❌ Error creating directory:', err);
      } else {
         console.log('📁 Dir created:', directoryPath);
      }
   });

   // create a new dir for the verbeterde punten sheets
   const directoryPathVerbeterd = directoryPath + '/' + fileNameWithoutExtension + ' ' + klas + ' - verbeterd';
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

                  // **********************
                  // PUNTEN LEERLING: START

                  const rowData = [
                     row['onderdeel'],               // Column A: description
                     '',                             // Column B: punt leerling (momenteel leeg)
                     '/',                            // Column C: '/'
                     parseInt(row['punt'], 10) || 0  // Column D: punt maximum, converted to a number
                  ];
                  worksheet.addRow(rowData);

                  total += parseInt(row['punt'], 10) || 0;

                  // PUNTEN LEERLING: STOP
                  // *********************

               })
               .on('end', () => {

                  // *******************************
                  // TOTALE PUNTEN BEREKENING: START

                  worksheet.getCell('F1').value = 'Punten';
                  worksheet.getCell('F2').value = { formula: '=SUM(B:B)' };

                  worksheet.getCell('G1').value = '/';
                  worksheet.getCell('G2').value = '/';

                  worksheet.getCell('H1').value = 'Totaal';
                  worksheet.getCell('H2').value = { formula: '=SUM(D:D)' };

                  // TOTALE PUNTEN BEREKENING: STOP
                  // ******************************

                  // *************************
                  // SPREADSHEET DESIGN: START

                  // Onderdeel breder
                  worksheet.getColumn(getColumnIndex('A')).width = 40;

                  // '/' smaller en centreren
                  worksheet.getColumn(getColumnIndex('C')).width = 2;
                  worksheet.getColumn(getColumnIndex('G')).width = 2;
                  worksheet.getColumn(getColumnIndex('C')).alignment = { horizontal: 'center' };
                  worksheet.getColumn(getColumnIndex('G')).alignment = { horizontal: 'center' };

                  // getallen smaller
                  worksheet.getColumn(getColumnIndex('B')).width = 4;
                  worksheet.getColumn(getColumnIndex('D')).width = 4;

                  // getallen na '/' links uitlijnen
                  worksheet.getColumn(getColumnIndex('D')).alignment = { horizontal: 'left' };
                  worksheet.getColumn(getColumnIndex('H')).alignment = { horizontal: 'left' };

                  // het woord punten rechts uitlijnen
                  worksheet.getColumn(getColumnIndex('F')).alignment = { horizontal: 'right' };

                  // SPREADSHEET DESIGN: STOP
                  // ************************

                  // Ensure the output directory exists
                  fs.mkdirSync('output', { recursive: true });

                  // Save sheet file to the output directory
                  outputFile = directoryPath + '/' + nameStudent + '.xlsx';
                  workbook.xlsx.writeFile(outputFile)
                     .then(() => {
                        console.log('📘', nameStudent);
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

	const platform = os.platform();

	if (platform === 'linux') {
	exec(`xdg-open "${directoryPath}"`, (err) => {
		if (err) console.error('Error opening directory on Linux:', err);
	});
	} else if (platform === 'darwin') {
	exec(`open "${directoryPath}"`, (err) => {
		if (err) console.error('Error opening directory on macOS:', err);
	});
	} else if (platform === 'win32') {
	exec(`start "${directoryPath}"`, (err) => {
		if (err) console.error('Error opening directory on Windows:', err);
	});
	} else {
	console.error('Unsupported operating system:', platform);
	}

});

/* ********************************************************************************************************************************* */
// Helper functions

function getColumnIndex(columnLetter) {
   return columnLetter.toUpperCase().charCodeAt(0) - 64;
}

/* ********************************************************************************************************************************* */
// GUIDE

// $ node csv-to-sheets.js path/to/punten.csv klas
// $ node csv-to-sheets.js '../../docs/_data/webtechnology/file.csv' 5AD
// $ node csv-to-sheets.js /home/hanne/Documents/meneermaes/docs/_data/hardware/artikel-soorten-computers.csv 5IFCW
