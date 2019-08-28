const {app, BrowserWindow} = require('electron')

const main = require('electron').ipcMain
let notifier = require('electron-notifications')

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let notifLimit = 3
let notifs = 0


async function update(pyshell, rend){
	let totalVal = null;
	let speedVal = null;

	let prev = 0


	try{
		pyshell.send('send-info');
		pyshell.on('message', async function(message){
			
			if (message.includes("CON:")){
				// console.log(message)
				rend.send('on-connected', message)
				await sleep(1000)
			}

			else if(message.includes("DISCON")){
				rend.send('disconnected')
				await sleep(1000)
			}

			// else if (message.includes("Switching")){
			// 	rend.send('switch')
			// 	await sleep(1000)
			// }

			else{

				totalVal = message
				speedVal = totalVal - prev

				prev = totalVal

				rend.send('info', [totalVal, speedVal])


				await sleep(1000);
				pyshell.send('send-info');
			}
		});

	}
	catch (e){
		console.log('ERROR')
		console.error(e)
	}
		
}



app.on('ready', async function(){

	let win = new BrowserWindow({width: 600, height: 250})
	win.setResizable(false)
	currentWindow = win

	win.loadURL(`file://${__dirname}/index.html`)

	let {PythonShell} = require('python-shell')

	let pyshell = new PythonShell('net-monitor.py');

	main.on('init', function(event, arg){
		let rend = event.sender
		update(pyshell, rend)
	})

})


