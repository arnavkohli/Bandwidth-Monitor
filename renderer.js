

const renderer = require('electron').ipcRenderer
window.$ = window.jQuery = require('jquery')
var Chart = require('chart.js');

let x = 0;

renderer.send('init', 'Connecting...')

let myChart, ctx;


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// renderer.on('overlimit', function(event, arg){
// 	// const { getDoNotDisturb } = require('electron-notification-state')
// 	// console.log(getDoNotDisturb());

// 	let myNotification = new Notification('LE', {
// 	  body: '1MB downloaded!'
// 	})
// })

// renderer.on('switch', function(event, arg){
// 	let s = $("#switch")

// 	s.animate({
// 		left: '185px'
// 	}, 2500)
// })

// renderer.on('switched', function(event, arg){
// 	let s = $("#switch")

// 	s.animate({
// 		left: '1000px'
// 	}, 2500);

// 	info.animate({
// 		marginTop: '30px'
// 	}, 2000);

// 	graph.animate({
// 		top: '10px'
// 	}, 2000, () =>{
// 	});

// 	x = 0
// 	ctx = document.getElementById('graph').getContext('2d');
// 	myChart = new Chart(ctx, {
// 	    type: 'line',
// 	    data: {
// 	        datasets: [{
// 	        	label: 'Down Speed',
// 	            data: [],
// 	            showLine: true,
// 	            borderColor: 'white',
// 	            pointBackgroundColor: 'yellow'
// 	        }]
// 	    },
// 	    options: {
// 	    	responsive: false,
// 			// maintainAspectRatio: true,
// 	        scales: {
// 	            yAxes: [{
// 	                ticks: {
// 	                    display: false,
// 	                    min: 0,
// 	                    max: 100
// 	                }
// 	            }]
// 	        }
// 	    }
// 	});

// })


renderer.on('info', function(event, arg){
	// if (parseInt(arg[0], 10) > 5 && notifs < 5){
	// 	console.log('NOTIF:' + parseInt(arg[0], 10))
	// 	let myNotification = new window.Notification('Limit Exeeded', {
	// 	  body: 'You exceeded the limit you set.'
	// 	})
	// 	notifs += 3
	// }
	
	document.getElementById('total-val').innerHTML = Number(arg[0]).toFixed(2) + ' MB';
	document.getElementById('speed-val').innerHTML = Number(arg[1]).toFixed(2) + ' MB/s';


	addData(myChart, arg[1], '')
	x += 1
	if (x > 10)
		removeData(myChart)
})

function addData(chart, data, label) {
	try{
		chart.data.labels.push(label);
	    chart.data.datasets.forEach((dataset) => {
	        dataset.data.push(data);
	        // console.log('ADDED')
	        // console.log(dataset.data)

	    });
	    chart.update(0);
	    // chart.update();
	}
	catch(e){
		console.error(e)
	}
}

function removeData(chart) {
	try{
		chart.data.labels = chart.data.labels.slice(1,)
	    chart.data.datasets.forEach((dataset) => {
	        dataset.data = dataset.data.slice(1,)
	        // console.log('POPPED')
	        // console.log(dataset.data[0])
	    });
	    chart.update(0);
	    // chart.update();
	}
	catch(e){
		console.error(e)
	}
}

renderer.on('on-connected', async function(event, arg){
	// let myNotification = new Notification('Connected', {
	//   body: 'main -> renderer'
	// })
	document.getElementById('total-val').innerHTML = '0.00 MB';
	document.getElementById('speed-val').innerHTML = '0.00 MB/s';

	let discon = $("#disconnected")
	let info = $("#info")
	let graph = $("#graph")

	let ssid = $("#ssid")
	ssid.html(arg.slice(4, arg.length))

	discon.animate({
	    left : '-1000px'
	  }, 1500).removeClass('hidden');

	info.animate({
		marginTop: '30px'
	}, 2000);

	graph.animate({
		top: '10px'
	}, 2000, () =>{
	});

	x = 0
	ctx = document.getElementById('graph').getContext('2d');
	myChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        datasets: [{
	        	label: 'Down Speed',
	            data: [],
	            showLine: true,
	            borderColor: 'white',
	            pointBackgroundColor: 'yellow'
	        }]
	    },
	    options: {
	    	responsive: false,
			// maintainAspectRatio: true,
	        scales: {
	            yAxes: [{
	                ticks: {
	                    display: false,
	                    min: 0,
	                    max: 100
	                }
	            }]
	        }
	    }
	});


})

renderer.on('disconnected', function(event, arg){
	$("#header").after("<div id='disconnected' style='position:absolute;padding: 2px;border: solid 1px white;text-align: center;left: -1000px;margin-top: 20px;'>DISCONNECTED<p>Your device is not connected to the internet.</p><div id='loader'></div>Listening for a connection....</div>")

	let discon = $("#disconnected")
	let info = $("#info")
	let graph = $("#graph")

	let ssid = $("#ssid")
	ssid.html("None")


	info.animate({
		marginTop: '300px',
	}, 2000);

	discon.animate({
	    left: '0px'
	  }, 2500);

	graph.animate({
		top: '-1000px'
	}, 2000);
})