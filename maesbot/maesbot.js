const readline = require('readline');		// ask questions
const { spawn } = require('child_process'); // execute other scripts
const fs = require('fs');					// access to filesystem

/* ****************** */
/* READ SETTINGS JSON */
/* ****************** */

try {
	const data = fs.readFileSync('settings-maesbot.json', 'utf8'); 	// Read the contents of the JSON file synchronously
	const jsonData = JSON.parse(data); 								// Parse the JSON data into a JavaScript object

	// Get settings
	const privateDataDir = jsonData['private data dir'];

	console.log();
	console.log('settings-maesbot.json:');
	console.log('- Private data directory:', privateDataDir);
	
	/* *************** */
	/* INTRO QUESTIONS */
	/* *************** */

	console.log();
	console.log('1. Diff files?');
	console.log('2. Punten sheet maken?');
	console.log();

	/* ************** */
	/* ASK WHAT TO DO */
	/* ************** */

	const rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout
	});
	rl.question('🤖 What do you want to do? ', (answer) => {
		console.log();

		// execute what you chose
		if (answer == '1') {

			/* ********** */
			/* DIFF FILES */
			/* ********** */

			console.log('🤖 Diff files:');

			const pythonProcess = spawn('/usr/bin/python3', ['batchFileDiff.py'], { cwd: 'diff-file/' });
			// /usr/bin/python3: the location of the Python3 binary, find with this command $ which python3
			// cwd: the location from where the python scripts is executed
			pythonProcess.stdout.on('data', (data) => {
				console.log(`Python script output: ${data}`);
			});
			pythonProcess.stderr.on('data', (data) => {
				console.error(`Error from Python script: ${data}`);
			});
			pythonProcess.on('close', (code) => {
				console.log(`Python script exited with code ${code}`);
			});

		} else if (answer == '2') {

			/* ****************** */
			/* PUNTEN SHEET MAKEN */
			/* ****************** */

			console.log('🤖 Punten sheet maken:');

			spawn('node punten/csv-to-sheet.js', (error, stdout, stderr) => {
				if (error) {
					console.error(`exec error: ${error}`);
					return;
				}
				console.log(`stdout: ${stdout}`);
				console.error(`stderr: ${stderr}`);
			});


		} else {
			console.log('🤖 Nothing...');
		}
		
		rl.close();
	});

/* ****************************** */
/* ON ERROR READING SETTINGS JSON */
/* ****************************** */

} catch (error) {
	console.error('❌ Error reading or parsing settings-maesbot.json:', error);
}
