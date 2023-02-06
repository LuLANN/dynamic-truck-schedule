
//alert("Loading a Script!!")
console.log("In currTime.js")

function twoDigitPad(num) {
    return num < 10 ? "0" + num : num;
}

function display_c(){
    var refresh=1000; // Refresh rate in milli seconds
    mytime=setTimeout('display_currtime()',refresh)
};

function display_currtime() {
    
    var datetime = new Date();
    var days_in_week = ["SUN","MON", "TUE", "WED", "THU", "FRI", "SAT" ];
    var months_in_year = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];

    var time_output =   days_in_week[datetime.getDay()] + " "  
                        +months_in_year[datetime.getMonth()] + "-" 
                        +datetime.getDate() + "-" 
                        +datetime.getFullYear() + ", " 
                        +twoDigitPad(datetime.getHours()) + ":"
                        +twoDigitPad(datetime.getMinutes()) + ":"
                        +twoDigitPad(datetime.getSeconds());

    document.getElementById('currTime').innerHTML = time_output;
    display_c();
}
