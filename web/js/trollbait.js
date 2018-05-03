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
    var body = document.getElementsByTagName("body")[0];
    var classifierdiv=document.getElementById("classifier")
    var myIndex=0
    
    // Empty array to hold mydata from this session
    data2=[]
    
    
    classifierdiv.innerHTML=data[myIndex.toString()]['text_clean']
    // Create a button to go to the next record
    var nextbutton = document.createElement("button");
    nextbutton.innerHTML = "Next";
    
    nextbutton.addEventListener ("click", function() {
        console.log(data.length)
        data2.push(data[myIndex.toString()])
        console.log(data2.length)
        myIndex = (myIndex+1)%(data.length);
        console.log(myIndex)
        classifierdiv.innerHTML=data[myIndex.toString()]['text_clean']
        classifierdiv.innerHTML+=""
        
    });
    
    // Create a button to download our data
    var dlbutton = document.createElement("button");
    dlbutton.innerHTML = "Download Your Work";
    dlbutton.addEventListener ("click", function() {
        
        downloadJSON({filename:"mywork.json",
                      data:data2
                    })
    });
    
    // Add buttons to body
    body.appendChild(nextbutton);
    body.appendChild(dlbutton);
    
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