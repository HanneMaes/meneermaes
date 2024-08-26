const color = require('./consoleColors'); // my color script
const readline = require('readline'); // ask questions
const { spawn } = require('child_process'); // execute other scripts
const fs = require('fs'); // access to filesystem
const path = require('path'); // work with file paths

/* ****************** */
/* READ SETTINGS JSON */
/* ****************** */

try {

	// Get settings
   privateDataDir = "";
   fs.readFile('settings-maesbot.json', 'utf8', (err, jsonString) => {
      if (err) {
         console.error("Error reading settings-maesbot.json:", err);
         return;
      }
      try {
         const data = JSON.parse(jsonString);
         // console.log("Parsed data:", data);
         if (data["private-data-dir"]) {
            privateDataDir = data["private-data-dir"];
            // console.log("private-data-dir:", privateDataDir);
         } else {
            console.error("Error: 'private-data-dir' not found in parsed data");
         }
      } catch(err) {
         console.error('Error parsing JSON string:', err);
      }
   });

	/* ********* */
	/* ASCII ART */
	/* ********* */
	console.log(color.highlight("          __            "));
	console.log(color.highlight("  _(_\\   |@@|           "));
	console.log(color.highlight(" (__/\\__ \\--/ __        "));
	console.log(color.highlight("    \\___|----|  |   __  "));
	console.log(color.highlight("        \\ }{ /\\ )_ / _\\ "));
	console.log(color.highlight("        /\\__/\\ \\__O (__ "));
	console.log(color.highlight("       (--/\\--)    \\__/ "));
	console.log(color.highlight("       _)(  )(_         "));
	console.log(color.highlight("      `---''---`        "));

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
         });
         child.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
         });
         child.on('error', (error) => {
            console.error(`Error from nodejs script: ${error.message}`);
         });

		} else if (answer == '2') {

			/* *********** */
			/* SHEET 2 PDF */
			/* *********** */

			console.log(color.executing("🤖 Punten PDF's maken..."));

		} else if (answer == '3') {

			/* ************** */
			/* DIFF: OPEN DIR */
			/* ************** */

			console.log(color.executing('🤖 Opening diff files dir...'));

			const directoryPath = path.join(__dirname, 'diff-file/Files to Diff/'); // Define the directory you want to open

			let command;
			let args;
			if (process.platform === 'win32') {
				// Windows
				command = 'cmd';
				args = ['/c', `start "" "${directoryPath}"`];
			} else if (process.platform === 'darwin') {
				// macOS
				command = 'open';
				args = [directoryPath];
			} else {
				// Linux and other UNIX-like OSes
				command = 'xdg-open';
				args = [directoryPath];
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

			console.log(color.executing('🤖 Diff files...'));

			const pythonProcess = spawn('/usr/bin/python3', ['batchFileDiff.py'], { cwd: 'diff-file/' });
			// /usr/bin/python3: the location of the Python3 binary, find with this command $ which python3
			// cwd: the location from where the python scripts is executed

			pythonProcess.stdout.on('data', (data) => {
				console.log(`${data}`); // output the Python scrip output
			});
			pythonProcess.stderr.on('data', (data) => {
				console.error(`Error from Python script: ${data}`);
			});

		} else {

         /* ******* */
         /* NOTHING */
         /* ******* */

			console.log(color.executing('🤖 Nothing...'));
		}

		rl.close();
	});

/* ****************************** */
/* ON ERROR READING SETTINGS JSON */
/* ****************************** */

} catch (error) {
	console.error('❌ Error reading or parsing settings-maesbot.json:', error);
}
