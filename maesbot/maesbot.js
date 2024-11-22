const color = require('./consoleColors'); // my color script
const readline = require('readline'); // ask questions
const { spawn, execSync } = require('child_process'); // execute other scripts
const fs = require('fs'); // access to filesystem
const path = require('path'); // work with file paths

/* ******************************************************************************************************************************************* */

/* ********************* */
/* 1. READ SETTINGS JSON */
/* ********************* */

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

/* *************************************** */
/* 2. ASK WHAT TO DO JSON FILES ARE LOADED */
/* *************************************** */

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
   console.log(color.answer(' 3. Open punten dir'));
   console.log();
   console.log(color.info('Diff'))
   console.log(color.answer(' 4. Open diff dir'));
   console.log(color.answer(' 5. Diff files'));
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

/* ******************************************************************************************************************************************* */

/* *************************** */
/* 3. DO WHAT I SELECTED TO DO */
/* *************************** */
	   
      /* *********** */
      /* CSV 2 SHEET */
	  /* *********** */
	   if (answer == '1') {

		   // selecteer een klas
		   const selectedKlas = selectFromArray(Object.keys(klassenJSON.klassen));
		  
		   // Selecteer een file
		   const directoryToSearch = '../docs/_data/'; // Where to look for files
		   const selectedFile = browseFile(directoryToSearch);
			
		   if (selectedFile) {
			   if (selectedKlas) {
				   console.log(`Selected file: ${selectedFile}`);
				   const command = 'node';
				   const args = ['punten/csv-to-sheets.js', selectedFile, selectedKlas];
				   const child = spawn(command, args, { stdio: 'inherit' }); // Pass stdio to inherit input/output
				   child.on('error', (err) => {
					   console.error('Failed to start subprocess:', err);
				   });
			   } else {
				   console.error('Geen klas geselecteerd.');
			   }
		   } else {
			   console.error('Geen file geselecteerd.');
		   }

		   /* *********** */
		   /* SHEET 2 PDF */
		   /* *********** */
	   } else if (answer == '2') {

		   console.log(color.executing("🤖 Punten PDF's maken..."));
		  
		   /* *************** */
		   /* OPEN PUNTEN DIR */
		   /* *************** */
	   } else if (answer == '3') {
		  
		  

         /* ************** */
         /* DIFF: OPEN DIR */
         /* ************** */

        //  const directoryPath = path.join(settingsJson['private-data-dir'], settingsJson['diff-files-dir']);
        //  console.log(color.executing('🤖 Opening diff files dir: ' + directoryPath));

        //  let command;
        //  let args;
        //  if (process.platform === 'win32') {
        //     // Windows
        //     command = 'cmd';
        //     args = ['/c', `start "" "${directoryPath}"`];

        //     // RUN MAESBOT AGAIN?
        //     // runAgain(settingsJson);

        //  } else if (process.platform === 'darwin') {
        //     // macOS
        //     command = 'open';
        //     args = [directoryPath];

        //     // RUN MAESBOT AGAIN?
        //     // runAgain(settingsJson);

        //  } else {
        //     // Linux and other UNIX-like OSes
        //     command = 'xdg-open';
        //     args = [directoryPath];

        //     // RUN MAESBOT AGAIN?
        //     // runAgain(settingsJson);

        //  }

        //  // Execute the command
        //  const child = spawn(command, args, { stdio: 'ignore' });
        //  child.on('error', (err) => {
        //     console.error(`Error opening directory: ${err}`);
		  //  });
		  
	    /* *********** */
         /* SHEET 2 PDF */
         /* *********** */

	// 	 console.log(color.executing("🤖 Punten PDF's maken..."));

	// 	} else if (answer == '4') {

    //   } else if (answer == '5') {

         /* **************** */
         /* DIFF: DIFF FILES */
         /* **************** */

        //  const directoryPath = path.join(settingsJson['private-data-dir'], settingsJson['diff-files-dir']);
        //  console.log(color.executing('🤖 Diff files...'));

        //  const pythonProcess = spawn('/usr/bin/python3', ['batchFileDiff.py', directoryPath], { cwd: 'diff-file/' });
        //  // /usr/bin/python3: the location of the Python3 binary, find with this command $ which python3
        //  // cwd: the location from where the python scripts is executed

        //  pythonProcess.stdout.on('data', (data) => {
        //     console.log(`${data}`); // output the Python scrip output

        //     // RUN MAESBOT AGAIN?
        //     // runAgain(settingsJson);
        //  });
        //  pythonProcess.stderr.on('data', (data) => {
        //     console.error(`Error from Python script: ${data}`);

        //     // RUN MAESBOT AGAIN?
        //     // runAgain(settingsJson);
        //  });

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

/* **************** */
/* HELPER FUNCTIONS */
/* *************** */

// run maesbot again without loading the json settings (aka just showing the menu again)
// function runAgain(settingsJson) {
//    showMenu(settingsJson);
// }

/* ************************************* */

// Open a dir in the default file explorer
function openDir(directory) {
	const platform = os.platform();

	if (platform === 'linux') {
	exec(`xdg-open "${directory}"`, (err) => {
		if (err) console.error('maesbot.js openDir() -> Error opening directory on Linux:', err);
	});
	} else if (platform === 'darwin') {
	exec(`open "${directory}"`, (err) => {
		if (err) console.error('maesbot.js openDir() -> Error opening directory on macOS:', err);
	});
	} else if (platform === 'win32') {
	exec(`start "${directory}"`, (err) => {
		if (err) console.error('maesbot.js openDir() -> Error opening directory on Windows:', err);
	});
	} else {
	console.error('maesbot.js openDir() -> Unsupported operating system:', platform);
	}
}

/* ************************************* */

// Select a file with fzf and return it, directory is the dir where to search in
function browseFile(directory) {
    try {
        // Run fzf to browse files in the specified directory
        const result = execSync(`find ${directory} -type f | fzf`, {
            encoding: 'utf-8', // Ensure the output is a string
            stdio: ['inherit', 'pipe', 'ignore'], // Pass input/output as needed
        }).trim(); // Remove trailing newline

        if (result) {
            // Resolve the absolute path of the selected file
            const absolutePath = path.resolve(result);

            // Ensure that the selected file is actually within the given directory
            if (!absolutePath.startsWith(path.resolve(directory))) {
                console.error('Selected file is outside the allowed directory.');
                return null;
            }

            return absolutePath;
        } else {
            return null; // Return null if no file is selected
        }
    } catch (error) {
        console.error('maesbot.js browseFile() -> canceled or error occurred.');
        return null; // Return null if something went wrong
    }
}

/* ************************************* */

// Select an element form an array with fzf and return it
function selectFromArray(inputArray) {
    try {
        // Join array elements with newlines, and escape special characters for fzf
        const inputString = inputArray.join('\n');
        const result = execSync(`echo "${inputString}" | fzf`, {
            encoding: 'utf-8',
            stdio: ['pipe', 'pipe', 'ignore'],
        }).trim();
        return result; // Return the selected class
    } catch (error) {
        console.error('maesbot.js selectFromArray() -> canceled or error occurred.');
        return null; // Return null to indicate cancellation
    }
}

/* ******************************************************************************************************************************************* */
// GUIDE

// $ node maesbot.js
// $ node maesbot.js debug
