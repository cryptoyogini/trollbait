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
    classifierdiv=document.getElementById("classifier")
    var myIndex=0
    classifierdiv.innerHTML=data[myIndex.toString()]['text_clean']
    data2=[]
    var nextbutton = document.createElement("button");
    nextbutton.innerHTML = "Next";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(nextbutton);

    // 3. Add event handler
    nextbutton.addEventListener ("click", function() {
        console.log(data.length)
        data2.push(data[myIndex.toString()])
        console.log(data2.length)
        myIndex = (myIndex+1)%(data.length);
        console.log(myIndex)
        classifierdiv.innerHTML=data[myIndex.toString()]['text_clean']
        classifierdiv.innerHTML+=""
        
    });
    
    var dlbutton = document.createElement("button");
    dlbutton.innerHTML = "Download Your Work";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(dlbutton);

    dlbutton.addEventListener ("click", function() {
        
        downloadJSON({filename:"mywork.json",
                    data:data2
                    })
    });

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