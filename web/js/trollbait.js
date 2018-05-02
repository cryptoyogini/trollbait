function log(message){
	var logdiv = document.getElementById('log');
	logdiv.innerHTML = "<br>"+ message;
}


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

function trollbait_classify(data){
    classifierdiv=document.getElementById("classifier")
    myIndex=0
    classifierdiv.innerHTML=data[myIndex]['text_clean']
    data2=[]
    var nextbutton = document.createElement("button");
    nextbutton.innerHTML = "Next";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(nextbutton);

    // 3. Add event handler
    nextbutton.addEventListener ("click", function() {
        data2.push(data[myIndex])
        console.log(data2.length)
        myIndex = (myIndex+1)%(data.length);
        classifierdiv.innerHTML=data[myIndex]['text_clean']
        classifierdiv.innerHTML+=""
        
    });
    
    var dlbutton = document.createElement("button");
    dlbutton.innerHTML = "Download CSV";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(dlbutton);

    dlbutton.addEventListener ("click", function() {
        
        downloadCSV({filename:"mywork.csv",
                    data:data2
                    })
    });

}


function convertArrayOfObjectsToCSV(args) {  
        var result, ctr, keys, columnDelimiter, lineDelimiter, data;

        data = args.data || null;
        if (data == null || !data.length) {
            return null;
        }

        columnDelimiter = args.columnDelimiter || ',';
        lineDelimiter = args.lineDelimiter || '\n';

        keys = Object.keys(data[0]);

        result = '';
        result += keys.join(columnDelimiter);
        result += lineDelimiter;

        data.forEach(function(item) {
            ctr = 0;
            keys.forEach(function(key) {
                if (ctr > 0) result += columnDelimiter;

                result += item[key];
                ctr++;
            });
            result += lineDelimiter;
        });

        return result;
    }


function downloadCSV(args) {  
        var csv = JSON2CSV(json);
        var downloadLink = document.createElement("a");
        var blob = new Blob(["\ufeff", csv]);
        var url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = "data.csv";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
}