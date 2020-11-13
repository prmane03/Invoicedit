$(function(){
    indx = $("#tbody").children().length;
    //add row to table
    $('#addrow').click(function(){
        $('#tbody').append('<tr id="row'+(++indx)+'"><td>'+(indx)+'.</td><td><input type="text" class="databox description"></td><td><input type="number" class="databox qty"></td><td><input type="number" class="databox price"></td><td class="total"></td></tr>');
        });
    //delete row form table
    $('#delrow').click(function(){
        if(indx>1){
            indx--;
            $('tbody tr:last').remove();
            var total_amount = 0;
            $('#tbody').children().each(function(){
                r = $(this);
                var t =(r).find(".total").text();
                if (t !== NaN && t !== "") {
                    total_amount += parseFloat(t);
                }
            });
            $("#total_amount").text(total_amount);
        }
    });
    //on change event
    $("table").on("change", "input", function(){
      var row = $(this).closest("tr");
      var qty = parseFloat(row.find(".qty").val());
      var price = parseFloat(row.find(".price").val());
      var total = qty * price;
      row.find(".total").text(isNaN(total) ? "" : total);
      //Update All total
      var total_amount = 0;
      $('#tbody').children().each(function(){
          r = $(this);
          var t =(r).find(".total").text();
          if (t !== NaN && t !== "") {
            total_amount += parseFloat(t);
          }
      });
      $("#total_amount").text(total_amount);
    });
    
    
    
    // To send data to flask for saving in db
    $("#save").click(function(){
        var desclist=[];
        var qtylist=[];
        var totallist=[];
        var pricelist=[];
        var invnum =$('#invoice_num').val();
        var usrnm = $('#usrnm').val();
        var provider_name=$('#provider_name').val();
        var provider_phone=$('#provider_phone').val();
        var provider_address=$('#provider_address').val();
        var customer_name=$('#customer_name').val();
        var customer_phone=$('#customer_phone').val();
        var customer_address=$('#customer_address').val();
        var date= $('#date').val();
        alert(date);
        alert(typeof(date));
        
        alert("mobile lengrh"+provider_phone.length+" ; "+customer_phone);
        
        if(provider_name==NaN || provider_address==NaN || customer_address==NaN || customer_name==NaN || provider_name=="" || provider_address=="" || customer_address=="" || customer_name==""){
            alert("Enter All customer and provider details");
        }
        else if(customer_phone.length==10 && provider_phone.length==10)
            {
            if(invnum!="" || invnum!=NaN)
            {
                alert(invnum+" "+usrnm);
                $("#tbody").children().each(function(){
                  r = $(this);
                  var desc= r.find('.description').val();
                  var qty = r.find('.qty').val();
                  var price= r.find('.price').val();
                  var total= r.find('.total').text();
                  alert("vals "+desc+" "+total);
                  if(total !=NaN && total!="" && desc!='')
                  {
                      alert('inside if');
            
                      desclist.push(desc);
                      qtylist.push(qty);
                      pricelist.push(price);
                      totallist.push(total);
                      alert(desclist);
                      alert(totallist);
                  }
                  
                  
                }); //end of for each
                var dict= {
                          description:desclist,
                          quantity:qtylist,
                          price:pricelist,
                          total:totallist
                      };
                var datalist = JSON.stringify(dict);
                $.getJSON('/save',
                {dict:datalist,
                invnum:invnum,
                usrnm:usrnm,
                provider_name:provider_name,
                provider_phone:provider_phone,
                provider_address:provider_address,
                customer_name:customer_name,
                customer_phone:customer_phone,
                customer_address:customer_address,
                date:date},
                function(data) {alert(data.result)});
              }
              else{
                  alert('invoice is must');
              }
            }
            else{
                alert('phone no. should be 10 Digit long');
            }
        
    });  


})