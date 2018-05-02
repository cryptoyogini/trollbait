function log(message){
	var logdiv = document.getElementById('log');
	logdiv.innerHTML = "<br>"+ message;
}


function trollbait_init(sheetkey){
    url="https://docs.google.com/spreadsheets/d/"+sheetkey+"/pubhtml"
    //log("Loading data...")
    console.log(url)
    log("Loading...<img src='img/glow.gif' height='60px' width='60px'>")                   
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
    classifierdiv.onclick = function(){
        myIndex = (myIndex+1)%(data.length);
        classifierdiv.innerHTML=data[myIndex]['text_clean']
    };
}