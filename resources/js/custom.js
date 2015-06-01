
//shopperscale.com
//





// JavaScript Document
 var gridster1,gridster2;
 var sessionPreferences = [];
 
 
 

function savePreferenceData(key, obj)
{
    localStorage.setItem(key, JSON.stringify(obj));
    
}


function getPreferenceData(key)
{   
    var stval = localStorage.getItem(key);
    
    console.log(JSON.parse(stval));
    
    return JSON.parse(stval);
    
}

 
 function removePoup()
 {
     
     
    $('.popup').animate({
            top:'-2000px'	
    }, 1000);
    
    $('.overlay').remove();
     
 }
 
 
 function deleteControl()
 {
     
     
    var rid = $('#currentrowid').val();
    
    
    var newarr = [];
    
    if( Array.isArray(sessionPreferences) == true)
    {

        for (var i = 0; i < sessionPreferences.length; i++) 
        {
            var row = sessionPreferences[i];
            
            if( row.id != rid)
            {
                newarr.push(row);
            }
            
        }
        
        
        
      savePreferenceData('controls', newarr);
      window.location = window.location; 
        
    }
     
     
     
     
     
 }
 
 function editControl(rowid)
 {
     
      $.get('form', function(data){
             
            
           $('.popup').html(data); 
            
            $('#currentrowid').val(rowid);
            
            
            if( Array.isArray(sessionPreferences) == true)
            {

                for (var i = 0; i < sessionPreferences.length; i++) 
                {
                    var row = sessionPreferences[i];

                    if( row.id == rowid)
                    {
                         $('#input-label').val(row.title);
                         $('#display-type').val(row.type);
                         
                         console.log(row.type);
                    }

                }

 
            } 


            
            $('#display-type').trigger('change');
            
             

            $('body').append('<span class="overlay"></span>');
            $('.popup').animate({
                    top:'50px'	
            }, 1000)


       });
     
     
 }
 
 
 
 function addToSession(type)
 {
     
    var currentrowid = $('#currentrowid').val();
    var rowindex = -1; 
     
    if( currentrowid != "")
    {
        
        if( Array.isArray(sessionPreferences) == true)
        {

            for (var i = 0; i < sessionPreferences.length; i++) 
            {
                var row = sessionPreferences[i];

                if( row.id == currentrowid)
                {
                        rowindex = i;
                }

            } 

        } 
    }
            
            
            
    if ($('#input-label').val() == "")
    {
        alert("Enter title");
        return;
    }
     
     
    
    
    
    if( Array.isArray(sessionPreferences) == false)
    {
        sessionPreferences = [];
    }
    
   
     
    
    if( type == 'Button')
    {
        
         
        var data = {};
        
        data.buttonlabel = $('#buttonlabel').val();
        
        data.dcmotor1 = {speed: ($('#dcmotor1-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor1-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor2 = {speed: ($('#dcmotor2-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor2-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor3 = {speed: ($('#dcmotor3-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor3-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor4 = {speed: ($('#dcmotor4-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor4-rampup').is(":checked") ? 1 : 0)};



         
        if( rowindex != -1)
        {
            sessionPreferences[rowindex] = {col: 1, row: 1, size_x: 1, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Button', 'data' : data};
            
            
        }
        else
        {
            sessionPreferences.push({col: 1, row: 1, size_x: 1, size_y:1, id: 'rowid'+ sessionPreferences.length + Math.random(), title: $('#input-label').val() ,type : 'Button', 'data' : data});
        }
        
       
         
    }
    
    
    
    
    if( type == 'Number')
    {
         
        var data = {};
        
        
        data.stepincrement = $('#stepincrement').val();
        
        data.dcmotor1 = {speed: ($('#dcmotor1-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor1-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor2 = {speed: ($('#dcmotor2-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor2-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor3 = {speed: ($('#dcmotor3-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor3-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor4 = {speed: ($('#dcmotor4-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor4-rampup').is(":checked") ? 1 : 0)};

        data.stepper1 = {speed: ($('#stepper1-speed').is(":checked") ? 1 : 0)};
        data.stepper2 = {speed: ($('#stepper2-speed').is(":checked") ? 1 : 0)};
         
        
        data.servo1  = {position: ($('#servo1-position').is(":checked") ? 1 : 0), rampup: ($('#servo1-rampup').is(":checked") ? 1 : 0)};
        data.servo2  = {position: ($('#servo2-position').is(":checked") ? 1 : 0), rampup: ($('#servo2-rampup').is(":checked") ? 1 : 0)};
        data.servo3  = {position: ($('#servo3-position').is(":checked") ? 1 : 0), rampup: ($('#servo3-rampup').is(":checked") ? 1 : 0)};
        
        data.pwm1     = {value: ($('#pwm1-value').is(":checked") ? 1 : 0), rampup: ($('#pwm1-rampup').is(":checked") ? 1 : 0)};
        data.pwm2     = {value: ($('#pwm2-value').is(":checked") ? 1 : 0), rampup: ($('#pwm2-rampup').is(":checked") ? 1 : 0)};
        data.pwm3     = {value: ($('#pwm3-value').is(":checked") ? 1 : 0), rampup: ($('#pwm3-rampup').is(":checked") ? 1 : 0)};
        
        if( rowindex != -1)
        {
            sessionPreferences[rowindex] = {col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Number', 'data' : data};
        
        }
        else
        {
            sessionPreferences.push({col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Number', 'data' : data});
        
        }
         
    }
    
    
    
    if( type == 'Number (slider)')
    {
        var data = {};
        data.dcmotor1 = {speed: ($('#dcmotor1-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor1-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor2 = {speed: ($('#dcmotor2-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor2-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor3 = {speed: ($('#dcmotor3-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor3-rampup').is(":checked") ? 1 : 0)};
        data.dcmotor4 = {speed: ($('#dcmotor4-speed').is(":checked") ? 1 : 0), rampup: ($('#dcmotor4-rampup').is(":checked") ? 1 : 0)};

        data.stepper1 = {speed: ($('#stepper1-speed').is(":checked") ? 1 : 0)};
        data.stepper2 = {speed: ($('#stepper2-speed').is(":checked") ? 1 : 0)};
         
        
        data.servos1  = {speed: ($('#servos1-position').is(":checked") ? 1 : 0), rampup: ($('#servos1-rampup').is(":checked") ? 1 : 0)};
        data.servos2  = {speed: ($('#servos2-position').is(":checked") ? 1 : 0), rampup: ($('#servos2-rampup').is(":checked") ? 1 : 0)};
        data.servos3  = {speed: ($('#servos3-position').is(":checked") ? 1 : 0), rampup: ($('#servos3-rampup').is(":checked") ? 1 : 0)};
        
        data.pwm1     = {speed: ($('#pwm1-value').is(":checked") ? 1 : 0), rampup: ($('#pwm1-rampup').is(":checked") ? 1 : 0)};
        data.pwm2     = {speed: ($('#pwm2-value').is(":checked") ? 1 : 0), rampup: ($('#pwm2-rampup').is(":checked") ? 1 : 0)};
        data.pwm3     = {speed: ($('#pwm3-value').is(":checked") ? 1 : 0), rampup: ($('#pwm3-rampup').is(":checked") ? 1 : 0)};
        
        if( rowindex != -1)
        {
            sessionPreferences[rowindex] = {col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Number (slider)', 'data' : data};
        
        }
        else
        {
            sessionPreferences.push({col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Number (slider)', 'data' : data});
        
        }
        
         
        
         
    }
     
     
    if( type == 'Display')
    {
        
        var data = {}; 
        data.inputsource = $('#inputsource').val();
        data.applyspeed  = $('#applyspeed').is(":checked") ? 1 : 0;
        data.scallinga   = $('#scalling-a').val();
        data.scallingb   = $('#scalling-b').val();
        data.scallingc   = $('#scalling-c').val();



        if( rowindex != -1)
        {
            sessionPreferences[rowindex] = {col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Display', 'data' : data};
        
        }
        else
        {
            sessionPreferences.push({col: 1, row: 1, size_x: 2, size_y:1, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Display', 'data' : data});
        
        }
        
        
         
         
    }
     
     
    if( type == 'Display (webcam)')
    {
        
        var data = {};
        data.inputsource = $('#inputsource').val();
        data.resolution   = $('#resolution').val();
        data.fps  = $('#fps').val();
        data.quality  = $('#quality').val();
	data.port  = $('#port').val();

        
        if( rowindex != -1)
        {
            sessionPreferences[rowindex] = {col: 1, row: 1, size_x: 4, size_y:3, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Display (webcam)', 'data' : data};
        
        }
        else
        {
            sessionPreferences.push({col: 1, row: 1, size_x: 4, size_y:3, id: 'rowid'+ sessionPreferences.length+ Math.random(), title: $('#input-label').val() ,type : 'Display (webcam)', 'data' : data});
        
        }
        
         
          
    } 
     
    
    savePreferenceData('controls', sessionPreferences);
    
    
    window.location = window.location; 
     
 }
 
 
$(document).ready(function() {
    
    
        sessionPreferences = getPreferenceData('controls');
         
    
    
        $.ajaxSetup({cache:false});
    
	
	//open popup
	$('.addItem').click(function(){
		
                
                $.get('form', function(data){
                
                    $('.popup').html(data);
                    
                    
                    $('body').append('<span class="overlay"></span>');
                    $('.popup').animate({
                            top:'50px'	
                    }, 1000)

                
                });
                
                
                
                
                
	});
	
	 
	
	$(document).keyup(function(e) {
		if( e.keyCode == 27)
                {
                    removePoup();
                }
                
	});
	
	
	

	//menu
	$('a.menubarHandler').click(function(){
		$('nav.top_menu').slideToggle();	
	});
	
        
       
         
	
});

 



function fillBoxesNonEditable()
{
    
    
    if( Array.isArray(sessionPreferences) == true)
    {

        for (var i = 0; i < sessionPreferences.length; i++) 
        {
            
            var row = sessionPreferences[i];
 
            if( row.type == 'Button')
            {
                
                var list = '<li data-row="'+ i +'" data-col="1" data-sizex="1" data-sizey="1">'+
                                    '<label>'+ row.title +'</label>'+
                                    '<a class="blank leftarrow"><strong>'+ row.data.buttonlabel +'</strong></a>'+
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            
            if( row.type == 'Number')
            {
                
                var list = '<li data-row="'+ i +'" data-col="1" data-sizex="2" data-sizey="1">'+
                                '<div class="increment">'+
                                    '<label>'+ row.title +'</label>'+
                                    '<input type="text" value="0"><a class="valup"></a><a class="valdown"></a>'+
                                '</div>'+
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            if( row.type == 'Number (slider)')
            {
                
                var list = '<li data-row="'+ i +'" data-col="1" data-sizex="2" data-sizey="1">'+                                
                                    '<label>'+ row.title +'</label>'+
                                    '<input type="range">'+                                
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            
            if( row.type == 'Display')
            {
               
                var list = '<li data-row="'+ i +'" data-col="1" data-sizex="2" data-sizey="1">'+
                                    '<label>'+ row.title +'</label>'+
                                    '<div class="shadow">95</div>'+
                            '</li>';


                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            
            
            if( row.type == 'Display (webcam)')
            {
                
                var list = '<li data-row="'+ i +'" data-col="1" data-sizex="4" data-sizey="4">'+
                                '<figcaption>'+ row.title +'</figcaption>'+
                                '<figure>'+
                                    '<img src="images/camimagerear.jpg" alt="">'+
                                    '<div class="cam-controls">'+
                                        '<a class="video"></a> <a class="image"></a>'+
                                    '</div>'+
                                '</figure>'+
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            
            
            
            
        }


    }
    
    
}





function fillBoxesEditable()
{
    
    
    if( Array.isArray(sessionPreferences) == true)
    {

        for (var i = 0; i < sessionPreferences.length; i++) 
        {
            
            var row = sessionPreferences[i];


            if( row.type == 'Button')
            {
                
                var list = '<li data-row="1" data-col="1" data-sizex="1" data-sizey="1">'+
                            '<label>'+ row.title +'</label>'+
                            '<span class="icons outline"></span>'+
                            '<a href="javascript:void(0)" onclick="editControl(\''+ row.id +'\')" class="icons edit"></a>'+
                        '</li>';
               
               
               gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     
               
 

            }
            
            
            
            if( row.type == 'Number')
            {
                
                var list = '<li data-row="1" data-col="2" data-sizex="2" data-sizey="1">'+
                                '<div class="increment">'+
                                    '<label>'+ row.title +'</label>'+
                                    '<span class="icons updown"></span>'+
                                    '<a href="javascript:void(0)" onclick="editControl(\''+ row.id +'\')" class="icons edit"></a>'+
                                '</div>'+
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     

            }
            
            
            if( row.type == 'Number (slider)')
            {
                
                var list = '<li data-row="1" data-col="3" data-sizex="2" data-sizey="1">'+
                                '<label>'+ row.title +'</label>'+
                                '<span class="icons range"></span>'+
                                '<a href="javascript:void(0)" onclick="editControl(\''+ row.id +'\')" class="icons edit"></a>'+
                           '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     

            }
            
            
            
            if( row.type == 'Display')
            {
                
                var list = '<li data-row="1" data-col="4" data-sizex="2" data-sizey="1">'+
                                '<label>'+ row.title +'</label>'+
                                '<span class="icons display"></span>'+
                                '<a href="javascript:void(0)" onclick="editControl(\''+ row.id +'\')" class="icons edit"></a>'+
                            '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     

            }
            
            
            
            
            if( row.type == 'Display (webcam)')
            {
                
                var list = '<li data-row="1" data-col="1" data-sizex="4" data-sizey="3">'+
                            '<figcaption>'+ row.title +'</figcaption>'+
                            '<span class="icons camera"></span>'+
                            '<a href="javascript:void(0)" onclick="editControl(\''+ row.id +'\')" class="icons edit"></a>'+
                           '</li>';

                gridster1.add_widget(list, row.size_x, row.size_y, row.col, row.row);     

            }
            
            
            
            
            
            
        }


    }
    
    
}

$(document).ready(function(){
    
   $('.arrow, .blank, .rotate').mousedown(function(){
       
       $(this).addClass('active').siblings().removeClass('active');
   }); 
   $('.arrow, .blank, .rotate').mouseup(function(){
       
       $(this).removeClass('active').siblings().removeClass('active');
   });
   
  
});