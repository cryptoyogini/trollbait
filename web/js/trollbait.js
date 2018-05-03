function log(message){
	var logdiv = document.getElementById('log');
	logdiv.innerHTML = "<br>"+ message;
}

/*
function trollbait_init(sheetkey){
    url="https://docs.google.com/spreadsheets/d/"+sheetkey+"/pubhtml"
    //log("Loading data...")
    console.log(url)
    log("<center>Loading...<br><img src='img/glow.gif' height='60px' width='60px'><center>")                   
    Tabletop.init( { key: url,
                   callback: function(data,tabletop){
                       console.log(data)
                       
                       log("Data loaded")
                       trollbait_classify(data)
                   },
                   simpleSheet: true } )
}
*/
function trollbait_init(jsonpath){
    console.log(jsonpath)
    log("<center>Loading...<br><img src='img/glow.gif' height='60px' width='60px'><center>")   
    $.getJSON(jsonpath, function( data ) {
        console.log(data[0])
        log("Data loaded")
        trollbait_classify(data)
        
    })
}

function trollbait_classify(data){
    // Initialize some variables
    //var controls = document.getElementById("controls");
    var classifierdiv=document.getElementById("texttoclassify")
    var myIndex=0
    
    
    
    classifierdiv.innerHTML=data[myIndex.toString()]['text_clean']
    // Create a button to go to the next record
    var nextbutton = document.createElement("button");
    nextbutton.innerHTML = "Next";
    nextbutton.type="submit"
    nextbutton.addEventListener ("click", function() {
        currentrec=data[myIndex]
        console.log($("#is_sexist").val())
        currentrec['religion']=$("#religion").val()
        currentrec['is_sexist']=$("#is_sexist").val()
        sessiondata.push(currentrec)
		myIndex = (myIndex+1)%(data.length);
        classifierdiv.innerHTML=data[myIndex]['text_clean']
        classifierdiv.innerHTML+=""
        $("#religion").val("None")
        
    });
    
 
    // Add buttons to body
    controls.appendChild(nextbutton);
    
}

function downloadJSON(args) {  
        //var csv = JSON2CSV(args.data);
        var jsonstr = JSON.stringify(args.data)
        var downloadLink = document.createElement("a");
        var blob = new Blob(["\ufeff", jsonstr]);
        var url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = args.filename || "data.json";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
}

const downloadData = event => {
  
  // Stop the form from submitting since we’re handling that with AJAX.
  event.preventDefault();
  
  // TODO: Call our function to get the form data.

  var fname=$("#name").val()+"-"+strftime("%Y%m%d-%H%M%S")+".json"
  console.log(fname)
  downloadJSON({filename:fname,
                      data:sessiondata
                    })
};


const classify = event => {
  
  // Stop the form from submitting since we’re handling that with AJAX.
  event.preventDefault();
  
  // TODO: Call our function to get the form data.

  console.log("Classifying")
  
};


function strftime(sFormat, date) {
  if (!(date instanceof Date)) date = new Date();
  var nDay = date.getDay(),
    nDate = date.getDate(),
    nMonth = date.getMonth(),
    nYear = date.getFullYear(),
    nHour = date.getHours(),
    aDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    aMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    aDayCount = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
    isLeapYear = function() {
      return (nYear%4===0 && nYear%100!==0) || nYear%400===0;
    },
    getThursday = function() {
      var target = new Date(date);
      target.setDate(nDate - ((nDay+6)%7) + 3);
      return target;
    },
    zeroPad = function(nNum, nPad) {
      return ('' + (Math.pow(10, nPad) + nNum)).slice(1);
    };
  return sFormat.replace(/%[a-z]/gi, function(sMatch) {
    return {
      '%a': aDays[nDay].slice(0,3),
      '%A': aDays[nDay],
      '%b': aMonths[nMonth].slice(0,3),
      '%B': aMonths[nMonth],
      '%c': date.toUTCString(),
      '%C': Math.floor(nYear/100),
      '%d': zeroPad(nDate, 2),
      '%e': nDate,
      '%F': date.toISOString().slice(0,10),
      '%G': getThursday().getFullYear(),
      '%g': ('' + getThursday().getFullYear()).slice(2),
      '%H': zeroPad(nHour, 2),
      '%I': zeroPad((nHour+11)%12 + 1, 2),
      '%j': zeroPad(aDayCount[nMonth] + nDate + ((nMonth>1 && isLeapYear()) ? 1 : 0), 3),
      '%k': '' + nHour,
      '%l': (nHour+11)%12 + 1,
      '%m': zeroPad(nMonth + 1, 2),
      '%M': zeroPad(date.getMinutes(), 2),
      '%p': (nHour<12) ? 'AM' : 'PM',
      '%P': (nHour<12) ? 'am' : 'pm',
      '%s': Math.round(date.getTime()/1000),
      '%S': zeroPad(date.getSeconds(), 2),
      '%u': nDay || 7,
      '%V': (function() {
              var target = getThursday(),
                n1stThu = target.valueOf();
              target.setMonth(0, 1);
              var nJan1 = target.getDay();
              if (nJan1!==4) target.setMonth(0, 1 + ((4-nJan1)+7)%7);
              return zeroPad(1 + Math.ceil((n1stThu-target)/604800000), 2);
            })(),
      '%w': '' + nDay,
      '%x': date.toLocaleDateString(),
      '%X': date.toLocaleTimeString(),
      '%y': ('' + nYear).slice(2),
      '%Y': nYear,
      '%z': date.toTimeString().replace(/.+GMT([+-]\d+).+/, '$1'),
      '%Z': date.toTimeString().replace(/.+\((.+?)\)$/, '$1')
    }[sMatch] || sMatch;
  });
}
