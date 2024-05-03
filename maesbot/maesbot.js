const readline = require('readline');       // ask questions
const { spawn } = require('child_process'); // execute other scripts

// into
console.log();
console.log('1. Diff files?');
console.log();

// ask what to do
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
rl.question('🤖 What do you want to do? ', (answer) => {
    console.log();

    // execute what you chose
    if (answer == '1') {
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
        
    } else {
        console.log('🤖 Nothing...');
    }
    
    rl.close();
});
