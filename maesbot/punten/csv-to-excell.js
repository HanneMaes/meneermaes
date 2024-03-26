const fs = require('fs');
const csv = require('csv-parser');
const ExcelJS = require('exceljs');

const names = ['Bibi Yassine', 'Bicer M.Kerem', 'Coremans Victor', 'Dante Gallardo Ledon', 'Tiago Niz Ferreira', 'Nouredine Tahrioui', 'Bram Van Ballaert', 'Yorbe Watthé', 'Noureddine Yazrak', 'Xibe Dierckx', 'Baharah Ghafori'];
const inputFilePath = 'input.csv';

// Read CSV file
fs.createReadStream(inputFilePath)
  .pipe(csv())
  .on('data', (row) => {
    //console.log(row); // Do something with each row if needed
  })
  .on('end', () => {
    // Iterate over each name
    names.forEach((name) => {
        // Convert CSV to Excel
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('Sheet1');
        let total = 0; // Variable to store the total of column B
        
        // Read CSV file again to add data to Excel worksheet
        fs.createReadStream(inputFilePath)
        .pipe(csv())
        .on('data', (row) => {
            worksheet.addRow(Object.values(row));
            // Sum the values in column B
            total += parseInt(row['punt'], 10) || 0;
        })
        .on('end', () => {
            // Write total to cell C1
            worksheet.getCell('D1').value = 'Totaal';
            worksheet.getCell('D2').value = { formula: '=SUM(C:C)' };
            
            // Ensure the output directory exists
            fs.mkdirSync('output', { recursive: true });

            // Save Excel file to the output directory
            workbook.xlsx.writeFile(`output/${name}.xlsx`)
            .then(() => {
                console.log(name);
            })
            .catch((err) => {
                console.error('Error:', err);
            });
        });
    });
  });