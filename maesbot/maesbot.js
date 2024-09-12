const color = require('./consoleColors'); // my colot: script
const readline = require('readline'); // ask questions
const { spawn } = require('child_process'); // execute other scripts
const fs = require('fs'); // access to filesystem
const path = require('path'); // work with file paths

/* ******************************************************************************************************************************************* */

/* ****************** */
/* READ SETTINGS JSON */
/* ****************** */

// Get settings from settings-maesbot.json
fs.readFile('settings-maesbot.json', 'utf8', (err, data) => { // Read the JSON file
   if (err) {
      console.error('Error reading settings-maesbot.json:', err);
      return;
   }
   try {
      const jsonObjectSettings = JSON.parse(data); // Parse the JSON string into an object

      // Continue if the JSON is loaded
      // Get settings from private-data-dir/klassen-en-leerlingen
      fs.readFile(path.join(jsonObjectSettings ['private-data-dir'], jsonObjectSettings ['klassen en leerlingen']), 'utf8', (err, data) => { // Read the JSON file
         if (err) {
            console.error('Error reading klassen-en-leerlingen.json', err);
            return;
         }
         try {
            const jsonObjectKlassen = JSON.parse(data); // Parse the JSON string into an object
            showMenu(jsonObjectSettings, jsonObjectKlassen); // Continue when everything is loaded
         } catch (parseError) {
            console.error('Error parsing klassen-en-leerlingen.json', parseError);
         }
      });

   } catch (parseError) {
      console.error('Error parsing settings-maesbot.json:', parseError);
   }
});

/* ******************************************************************************************************************************************* */

/* ********************************************* */
/* CONTINUE WHEN settings-maesbot.json is loaded */
/* ********************************************* */

function showMenu(settingsJson, klassenJSON) {

   // show debug info is the script is runned like this: $ node maesbot.js debug
   const debugMode = process.argv.includes('debug'); // true or false
   if (debugMode) {
      console.log("settingsJson:", settingsJson);
      console.log();
      console.log("klassenJSON:", klassenJSON);
      console.log();
   }

   /* ********* */
   /* ASCII ART */
   /* ********* */
   console.log(color.art("          __            "));
   console.log(color.art("  _(_\\   |") + color.highlight("@@") + color.art("|           "));
   console.log(color.art(" (__/\\__ \\--/ __        "));
   console.log(color.art("    \\___|----|  |   __  "));
   console.log(color.art("        \\ }{ /\\ )_ / _\\ "));
   console.log(color.art("        /\\__/\\ \\__O (__ "));
   console.log(color.art("       (--/\\--)    \\__/ "));
   console.log(color.art("       _)(  )(_         "));
   console.log(color.art("      `---''---`        "));

   /* *************** */
   /* INTRO QUESTIONS */
   /* *************** */

   console.log();
   console.log(color.info('Punten'))
   console.log(color.answer(' 1. CVS 2 sheet'));
   console.log(color.answer(' 2. Sheet 2 PDF'));
   console.log();
   console.log(color.info('Diff'))
   console.log(color.answer(' 3. Open dir'));
   console.log(color.answer(' 4. Diff files'));
   console.log();
   console.log(color.info('Anykey to quit'));
   console.log();

   /* ************** */
   /* ASK WHAT TO DO */
   /* ************** */

   const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
   });
   rl.question(color.question('🤖 What do you want to do? '), (answer) => {

      // execute what you chose
      if (answer == '1') {

         /* *********** */
         /* CSV 2 SHEET */
         /* *********** */

         console.log(color.executing('🤖 Punten sheets maken...'));

         const command = 'node';
         const args = ['punten/csv-to-sheets.js'];
         const child = spawn(command, args); // Execute the command
         child.stdout.on('data', (data) => {
            console.log(`${data}`); // output the Python scrip output

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         });
         child.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         });
         child.on('error', (error) => {
            console.error(`Error from nodejs script: ${error.message}`);

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         });

      } else if (answer == '2') {

         /* *********** */
         /* SHEET 2 PDF */
         /* *********** */

         console.log(color.executing("🤖 Punten PDF's maken..."));

         // RUN MAESBOT AGAIN?
         // runAgain(settingsJson);

      } else if (answer == '3') {

         /* ************** */
         /* DIFF: OPEN DIR */
         /* ************** */

         const directoryPath = path.join(settingsJson['private-data-dir'], settingsJson['diff-files-dir']);
         console.log(color.executing('🤖 Opening diff files dir: ' + directoryPath));

         let command;
         let args;
         if (process.platform === 'win32') {
            // Windows
            command = 'cmd';
            args = ['/c', `start "" "${directoryPath}"`];

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         } else if (process.platform === 'darwin') {
            // macOS
            command = 'open';
            args = [directoryPath];

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         } else {
            // Linux and other UNIX-like OSes
            command = 'xdg-open';
            args = [directoryPath];

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);

         }

         // Execute the command
         const child = spawn(command, args, { stdio: 'ignore' });
         child.on('error', (err) => {
            console.error(`Error opening directory: ${err}`);
         });

      } else if (answer == '4') {

         /* **************** */
         /* DIFF: DIFF FILES */
         /* **************** */

         const directoryPath = path.join(settingsJson['private-data-dir'], settingsJson['diff-files-dir']);
         console.log(color.executing('🤖 Diff files...'));

         const pythonProcess = spawn('/usr/bin/python3', ['batchFileDiff.py', directoryPath], { cwd: 'diff-file/' });
         // /usr/bin/python3: the location of the Python3 binary, find with this command $ which python3
         // cwd: the location from where the python scripts is executed

         pythonProcess.stdout.on('data', (data) => {
            console.log(`${data}`); // output the Python scrip output

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);
         });
         pythonProcess.stderr.on('data', (data) => {
            console.error(`Error from Python script: ${data}`);

            // RUN MAESBOT AGAIN?
            // runAgain(settingsJson);
         });

      } else {

         /* ******* */
         /* NOTHING */
         /* ******* */

         console.log(color.executing('🤖 Nothing...'));
      }

      rl.close();
   });

} // function showMenu(settingsJson) {

/* ******************************************************************************************************************************************* */

/* ***************** */
/* RUN MAESBOT AGAIN */
/* ***************** */

// run maesbot again without loading the json settings (aka just showing the menu again)
function runAgain(settingsJson) {

   // ask to run again

   showMenu(settingsJson);
}

/* ******************************************************************************************************************************************* */
// GUIDE

// $ node maesbot.js
// $ node maesbot.js debug
